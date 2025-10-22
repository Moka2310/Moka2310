import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { loadStripe } from '@stripe/stripe-js';
import { Elements, CardElement, useStripe, useElements } from '@stripe/react-stripe-js';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Check, Zap, TrendingUp, Shield, Clock, Users, ArrowLeft } from 'lucide-react';
import axios from 'axios';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

// Clé publique Stripe
const stripePromise = loadStripe(process.env.REACT_APP_STRIPE_PUBLISHABLE_KEY || 'pk_live_51SGsdR0kb9a0ErqLuEcBJWWUXLHQV2XlNrh14IVdN0C2yT2yd9mxZF6UO0Z9OBb1MpxhKwZUyBN0kPgDtXhEhTB700P6s8VLQ2');

const SubscriptionForm = () => {
  const navigate = useNavigate();
  const stripe = useStripe();
  const elements = useElements();
  const { language } = useLanguage();
  
  const [telegramUsername, setTelegramUsername] = useState('');
  const [loading, setLoading] = useState(false);
  const [processingPayment, setProcessingPayment] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!stripe || !elements) {
      return;
    }

    if (!telegramUsername || !telegramUsername.startsWith('@')) {
      alert(t(language, 'subscription.form.invalidUsername'));
      return;
    }

    setLoading(true);
    setProcessingPayment(true);

    try {
      // Créer un payment method
      const cardElement = elements.getElement(CardElement);
      const { error, paymentMethod } = await stripe.createPaymentMethod({
        type: 'card',
        card: cardElement,
      });

      if (error) {
        throw new Error(error.message);
      }

      // Créer l'abonnement
      const response = await axios.post(
        `${API}/subscriptions/create`,
        {
          telegramUsername: telegramUsername,
          paymentMethodId: paymentMethod.id
        },
        {
          headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
          }
        }
      );

      const { clientSecret, subscriptionId, status } = response.data;

      // Confirmer le paiement
      if (status === 'incomplete') {
        const { error: confirmError } = await stripe.confirmCardPayment(clientSecret);
        
        if (confirmError) {
          throw new Error(confirmError.message);
        }
      }

      alert('🎉 Abonnement activé ! Redirection vers votre Dashboard...');

      setTimeout(() => {
        navigate('/dashboard');
      }, 2000);

    } catch (error) {
      console.error('Subscription error:', error);
      alert(error.response?.data?.detail || error.message || 'Une erreur est survenue');
    } finally {
      setLoading(false);
      setProcessingPayment(false);
    }
  };

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
          Retour
        </Button>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Left Side - Features */}
          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-bold mb-4">
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                  {t(language, 'subscription.title')}
                </span>
              </h1>
              <p className="text-white/70 text-lg">
                {t(language, 'subscription.subtitle')}
              </p>
            </div>

            {/* Price */}
            <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
              <div className="flex items-baseline gap-2 mb-2">
                <span className="text-5xl font-bold text-white">{t(language, 'subscription.price')}</span>
                <span className="text-white/60 text-xl">/ {t(language, 'subscription.perMonth')}</span>
              </div>
              <p className="text-white/60">{t(language, 'subscription.autoRenewal')}</p>
            </div>

            {/* Features List */}
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white mb-4">{t(language, 'subscription.features.title')}</h3>
              
              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <TrendingUp className="w-5 h-5 text-green-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'subscription.features.realTimeSignals')}</h4>
                  <p className="text-white/60 text-sm">{t(language, 'subscription.features.allChannels')}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-blue-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Users className="w-5 h-5 text-blue-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'subscription.features.telegramChannels')}</h4>
                  <p className="text-white/60 text-sm">{language === 'fr' ? 'Rejoignez notre communauté exclusive' : 'Join our exclusive community'}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-yellow-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Zap className="w-5 h-5 text-yellow-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'subscription.features.instantNotifications')}</h4>
                  <p className="text-white/60 text-sm">{language === 'fr' ? 'Ne ratez aucune opportunité' : 'Don\'t miss any opportunity'}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-purple-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Shield className="w-5 h-5 text-purple-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'subscription.features.support247')}</h4>
                  <p className="text-white/60 text-sm">{language === 'fr' ? 'Assistance disponible à tout moment' : 'Support available anytime'}</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <div className="w-10 h-10 bg-pink-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                  <Clock className="w-5 h-5 text-pink-400" />
                </div>
                <div>
                  <h4 className="text-white font-semibold">{t(language, 'subscription.features.cancelAnytime')}</h4>
                  <p className="text-white/60 text-sm">{language === 'fr' ? 'Annulez à tout moment depuis votre Dashboard' : 'Cancel anytime from your Dashboard'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Right Side - Payment Form */}
          <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
            <h2 className="text-2xl font-bold text-white mb-6">{language === 'fr' ? 'Informations de paiement' : 'Payment information'}</h2>
            
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Telegram Username */}
              <div>
                <label className="block text-white/80 mb-2 text-sm font-medium">
                  {t(language, 'subscription.form.telegramUsername')} *
                </label>
                <Input
                  type="text"
                  value={telegramUsername}
                  onChange={(e) => setTelegramUsername(e.target.value)}
                  placeholder={t(language, 'subscription.form.telegramPlaceholder')}
                  className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50"
                  required
                />
                <p className="text-white/50 text-xs mt-1">
                  {t(language, 'subscription.form.telegramHelp')}
                </p>
              </div>

              {/* Card Element */}
              <div>
                <label className="block text-white/80 mb-2 text-sm font-medium">
                  {t(language, 'subscription.form.creditCard')} *
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
                  {t(language, 'subscription.form.securedByStripe')}
                </p>
              </div>

              {/* Info Box */}
              <div className="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4">
                <p className="text-blue-300 text-sm">
                  <strong>ℹ️ {t(language, 'subscription.form.importantInfo')}</strong>
                </p>
                <ul className="text-white/70 text-sm mt-2 space-y-1 list-disc list-inside">
                  <li>{t(language, 'subscription.form.firstPayment')}</li>
                  <li>{t(language, 'subscription.form.autoRenewalInfo')}</li>
                  <li>{t(language, 'subscription.form.cancelInfo')}</li>
                  <li>{t(language, 'subscription.form.immediateAccess')}</li>
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
                    {t(language, 'subscription.subscribeButton')}
                  </span>
                )}
              </Button>

              <p className="text-white/50 text-xs text-center">
                {t(language, 'subscription.form.terms')}
              </p>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
};

const Subscription = () => {
  return (
    <Elements stripe={stripePromise}>
      <SubscriptionForm />
    </Elements>
  );
};

export default Subscription;
