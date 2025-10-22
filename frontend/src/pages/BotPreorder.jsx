import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { Button } from '../components/ui/button';
import { Bot, Check, ArrowLeft, Shield, Download, Zap } from 'lucide-react';
import axios from 'axios';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';
import { toast } from '../hooks/use-toast';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY || 'pk_live_51SGsdR0kb9a0ErqL0Ul6Fyd03yLqWwT1jKamQwdnImNQc0XGtHrop19FaVmb0vQdQstUQifpG6lTaZNrtq2GlwLT007HPABALk');

const BotPreorderForm = () => {
  const navigate = useNavigate();
  const stripe = useStripe();
  const elements = useElements();
  const { language } = useLanguage();
  
  const [loading, setLoading] = useState(false);
  const [processingPayment, setProcessingPayment] = useState(false);
  const [existingPreorder, setExistingPreorder] = useState(null);

  useEffect(() => {
    // Vérifier si l'utilisateur a déjà précommandé
    const checkExistingPreorder = async () => {
      try {
        const token = localStorage.getItem('tradalife_token');
        if (!token) {
          navigate('/login');
          return;
        }

        const response = await axios.get(`${API}/bot-preorders/my-preorders`, {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (response.data && response.data.length > 0) {
          const activePreorder = response.data.find(p => 
            p.status === 'pending_payment' || p.status === 'paid'
          );
          if (activePreorder) {
            setExistingPreorder(activePreorder);
          }
        }
      } catch (error) {
        console.error('Error checking preorder:', error);
      }
    };

    checkExistingPreorder();
  }, [navigate]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!stripe || !elements) {
      return;
    }

    if (existingPreorder) {
      toast({
        title: language === 'fr' ? '⚠️ Précommande existante' : '⚠️ Existing preorder',
        description: t(language, 'home.bot.alreadyPreordered'),
        variant: 'destructive'
      });
      return;
    }

    setLoading(true);
    setProcessingPayment(true);

    try {
      const token = localStorage.getItem('tradalife_token');
      if (!token) {
        navigate('/login');
        return;
      }

      // Créer un payment method
      const cardElement = elements.getElement(CardElement);
      const { error, paymentMethod } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
      });

      if (error) {
        throw new Error(error.message);
      }

      // Créer la précommande
      const response = await axios.post(
        `${API}/bot-preorders/create`,
        { paymentMethod: 'stripe' },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      const { preorderId } = response.data;

      // Créer un payment intent (simulation - devrait être géré côté backend)
      // Pour l'instant, on confirme juste la précommande
      await axios.post(
        `${API}/bot-preorders/confirm-payment/${preorderId}`,
        { payment_intent_id: paymentMethod.id },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast({
        title: language === 'fr' ? '🎉 Précommande réussie!' : '🎉 Pre-order successful!',
        description: language === 'fr' 
          ? 'Vous recevrez le bot par email dès sa sortie!' 
          : 'You will receive the bot by email upon release!',
        duration: 5000
      });

      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);

    } catch (error) {
      console.error('Preorder error:', error);
      toast({
        title: language === 'fr' ? '❌ Erreur' : '❌ Error',
        description: error.response?.data?.detail || error.message || (language === 'fr' ? 'Une erreur est survenue' : 'An error occurred'),
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
      setProcessingPayment(false);
    }
  };

  if (existingPreorder) {
    return (
      <div className="min-h-screen bg-[#1E1540] pt-24 pb-16 px-4">
        <div className="max-w-2xl mx-auto text-center">
          <Bot className="w-24 h-24 text-pink-400 mx-auto mb-6" />
          <h1 className="text-3xl font-bold text-white mb-4">
            {language === 'fr' ? '✅ Précommande confirmée' : '✅ Pre-order confirmed'}
          </h1>
          <p className="text-white/70 mb-6">
            {language === 'fr' 
              ? 'Vous avez déjà précommandé le bot. Vous recevrez un email dès qu\'il sera disponible!'
              : 'You have already pre-ordered the bot. You will receive an email as soon as it\'s available!'}
          </p>
          <Button onClick={() => navigate('/dashboard')} className="bg-gradient-to-r from-pink-500 to-purple-600">
            {language === 'fr' ? 'Retour au Dashboard' : 'Back to Dashboard'}
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1E1540] pt-24 pb-16 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Back Button */}
        <Button
          onClick={() => navigate(-1)}
          variant="ghost"
          className="mb-6 text-pink-400 hover:text-pink-300 hover:bg-pink-500/10"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          {language === 'fr' ? 'Retour' : 'Back'}
        </Button>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Left Side - Features */}
          <div className="space-y-6">
            <div>
              <div className="inline-block bg-gradient-to-r from-green-400 to-emerald-500 text-white text-xs font-bold px-4 py-1.5 rounded-full mb-4">
                ⚡ {language === 'fr' ? 'PRÉCOMMANDE' : 'PRE-ORDER'}
              </div>
              <h1 className="text-4xl font-bold mb-4">
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                  {t(language, 'home.bot.title')}
                </span>
              </h1>
              <p className="text-white/70 text-lg">
                {t(language, 'home.bot.subtitle')}
              </p>
            </div>

            {/* Price */}
            <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
              <div className="flex items-baseline gap-2 mb-2">
                <span className="text-5xl font-bold text-white">{t(language, 'home.bot.price')}</span>
                <span className="text-white/60 text-xl">{language === 'fr' ? 'paiement unique' : 'one-time'}</span>
              </div>
              <p className="text-white/60">{language === 'fr' ? 'Accès à vie' : 'Lifetime access'}</p>
            </div>

            {/* Features List */}
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white mb-4">
                {language === 'fr' ? 'Ce que vous obtenez :' : 'What you get:'}
              </h3>
              
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Check className="w-5 h-5 text-green-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'home.bot.features.instantCopy')}</h4>
                  <p className="text-white/60 text-sm">
                    {language === 'fr' ? 'Exécution immédiate des trades' : 'Immediate trade execution'}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Zap className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'home.bot.features.customizableLots')}</h4>
                  <p className="text-white/60 text-sm">
                    {language === 'fr' ? 'Ajustez selon votre capital' : 'Adjust according to your capital'}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-yellow-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Shield className="w-5 h-5 text-yellow-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'home.bot.features.riskManagement')}</h4>
                  <p className="text-white/60 text-sm">
                    {language === 'fr' ? 'Stop loss et take profit automatiques' : 'Automatic stop loss and take profit'}
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-purple-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Download className="w-5 h-5 text-purple-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">
                    {language === 'fr' ? 'Livraison instantanée' : 'Instant delivery'}
                  </h4>
                  <p className="text-white/60 text-sm">
                    {language === 'fr' ? 'Dès la sortie du bot' : 'Upon bot release'}
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Payment Form */}
          <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
            <h2 className="text-2xl font-bold text-white mb-6">
              {language === 'fr' ? 'Informations de paiement' : 'Payment information'}
            </h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Card Element */}
              <div>
                <label className="block text-white/80 mb-2 text-sm font-medium">
                  {language === 'fr' ? 'Carte de crédit' : 'Credit card'} *
                </label>
                <div className="bg-white/10 border border-purple-500/30 rounded-lg p-4">
                  <CardElement
                    options={{
                      style: {
                        base: {
                          fontSize: '16px',
                          color: '#ffffff',
                          '::placeholder': {
                            color: '#ffffff80',
                          },
                        },
                        invalid: {
                          color: '#ef4444',
                        },
                      },
                    }}
                  />
                </div>
                <p className="text-white/50 text-xs mt-1">
                  {language === 'fr' ? 'Paiements sécurisés par Stripe' : 'Secured payments by Stripe'}
                </p>
              </div>

              {/* Info Box */}
              <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                <p className="text-blue-300 text-sm">
                  <strong>ℹ️ {language === 'fr' ? 'Informations importantes' : 'Important information'}:</strong>
                </p>
                <ul className="text-white/70 text-sm mt-2 space-y-1 list-disc list-inside">
                  <li>{language === 'fr' ? 'Paiement unique de 300$ CAD' : 'One-time payment of 300$ CAD'}</li>
                  <li>{language === 'fr' ? 'Livraison par email dès la sortie' : 'Delivery by email upon release'}</li>
                  <li>{language === 'fr' ? 'Accès à vie au bot' : 'Lifetime access to the bot'}</li>
                  <li>{language === 'fr' ? 'Support technique inclus' : 'Technical support included'}</li>
                </ul>
              </div>

              {/* Submit Button */}
              <Button
                type="submit"
                disabled={!stripe || loading || processingPayment}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white py-6 text-lg font-bold"
              >
                {processingPayment ? (
                  <span className="flex items-center gap-2">
                    <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                    {language === 'fr' ? 'Traitement en cours...' : 'Processing...'}
                  </span>
                ) : (
                  <span className="flex items-center gap-2">
                    <Check className="w-5 h-5" />
                    {language === 'fr' ? 'Précommander - 300$ CAD' : 'Pre-order - 300$ CAD'}
                  </span>
                )}
              </Button>

              <p className="text-white/50 text-xs text-center">
                {language === 'fr' 
                  ? 'En précommandant, vous acceptez nos conditions d\'utilisation et notre politique de confidentialité.'
                  : 'By pre-ordering, you agree to our terms of service and privacy policy.'}
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

const BotPreorder = () => {
  return (
    <Elements stripe={stripePromise}>
      <BotPreorderForm />
    </Elements>
  );
};

export default BotPreorder;
