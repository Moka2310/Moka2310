import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { t, translations } from '../translations';
import { purchasesAPI } from '../api/client';
import { toast } from '../hooks/use-toast';
import { CreditCard, Loader2, ArrowLeft } from 'lucide-react';

const Checkout = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { user, updateUser } = useAuth();
  const { language } = useLanguage();
  const [paymentMethod, setPaymentMethod] = useState('stripe');
  const [processing, setProcessing] = useState(false);
  const [noRefundAccepted, setNoRefundAccepted] = useState(false);

  const formation = location.state?.formation;

  if (!formation) {
    navigate('/boutique');
    return null;
  }
  
  // Get translated formation info
  const getFormationTitle = () => {
    return translations[language]?.formations?.[formation.title]?.title || formation.title;
  };
  
  const getFormationDescription = () => {
    return translations[language]?.formations?.[formation.title]?.description || formation.description;
  };

  const handlePayment = async () => {
    // Check no-refund policy acceptance
    if (!noRefundAccepted) {
      toast({
        title: language === 'fr' ? 'Confirmation requise' : 'Confirmation required',
        description: language === 'fr' ? 'Veuillez accepter la politique de non-remboursement' : 'Please accept the no-refund policy',
        variant: 'destructive'
      });
      return;
    }

    setProcessing(true);
    
    try {
      // Create purchase
      const purchaseResponse = await purchasesAPI.create(formation.id, paymentMethod);
      const { purchaseId } = purchaseResponse.data;
      
      // Simulate payment processing (in production, integrate with Stripe/PayPal)
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Confirm purchase
      await purchasesAPI.confirm(purchaseId);
      
      toast({
        title: t(language, 'checkout.success'),
        description: t(language, 'checkout.successMessage')
      });
      
      setProcessing(false);
      navigate('/dashboard');
    } catch (error) {
      setProcessing(false);
      toast({
        title: t(language, 'checkout.error'),
        description: error.response?.data?.detail || t(language, 'checkout.errorMessage'),
        variant: 'destructive'
      });
    }
  };

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Back Button */}
        <Button
          onClick={() => navigate(-1)}
          variant="ghost"
          className="mb-6 text-pink-400 hover:text-pink-300 hover:bg-pink-500/10"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          {language === 'fr' ? 'Retour' : 'Back'}
        </Button>

        <h1 className="text-4xl font-bold mb-12 text-center">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
            {t(language, 'checkout.title')}
          </span>
        </h1>

        <div className="grid md:grid-cols-2 gap-8">
          {/* Formation Summary */}
          <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
            <h2 className="text-2xl font-bold text-white mb-6">{t(language, 'checkout.summary')}</h2>
            <div className="space-y-4">
              <div className="aspect-video rounded-xl overflow-hidden">
                <img
                  src={formation.image}
                  alt={getFormationTitle()}
                  className="w-full h-full object-cover"
                />
              </div>
              <h3 className="text-xl font-bold text-white">{getFormationTitle()}</h3>
              <p className="text-white/70">{getFormationDescription()}</p>
              <div className="flex items-center justify-between pt-4 border-t border-purple-500/30">
                <span className="text-white/70">{t(language, 'checkout.price')}</span>
                <span className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                  {formation.price}€
                </span>
              </div>

              {/* Cancel Order Button */}
              <div className="pt-4">
                <Button
                  onClick={() => navigate('/boutique')}
                  variant="outline"
                  className="w-full border-red-500/50 text-red-400 hover:bg-red-500/20 hover:border-red-500"
                >
                  {language === 'fr' ? '✕ Annuler cette commande' : '✕ Cancel this order'}
                </Button>
              </div>
            </div>
          </div>

          {/* Payment Method */}
          <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
            <h2 className="text-2xl font-bold text-white mb-6">{t(language, 'checkout.paymentMethod')}</h2>
            
            <div className="space-y-4 mb-8">
              <button
                onClick={() => setPaymentMethod('stripe')}
                className={`w-full p-4 rounded-xl border-2 transition-all ${
                  paymentMethod === 'stripe'
                    ? 'border-pink-500 bg-pink-500/10'
                    : 'border-purple-500/30 bg-white/5'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <CreditCard className="w-6 h-6 text-pink-400" />
                  <span className="text-white font-semibold">{t(language, 'checkout.card')}</span>
                </div>
              </button>

              <button
                onClick={() => setPaymentMethod('paypal')}
                className={`w-full p-4 rounded-xl border-2 transition-all ${
                  paymentMethod === 'paypal'
                    ? 'border-pink-500 bg-pink-500/10'
                    : 'border-purple-500/30 bg-white/5'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <svg className="w-6 h-6" viewBox="0 0 24 24" fill="#00457C">
                    <path d="M7.076 21.337H2.47a.641.641 0 0 1-.633-.74L4.944.901C5.026.382 5.474 0 5.998 0h7.46c2.57 0 4.578.543 5.69 1.81 1.01 1.15 1.304 2.42 1.012 4.287-.023.143-.047.288-.077.437-.983 5.05-4.349 6.797-8.647 6.797h-2.19c-.524 0-.968.382-1.05.9l-1.12 7.106zm14.146-14.42a3.35 3.35 0 0 0-.607-.541c-.013.076-.026.175-.041.254-.93 4.778-4.005 7.201-9.138 7.201h-2.19a.563.563 0 0 0-.556.479l-1.187 7.527h-.506l-.24 1.516a.56.56 0 0 0 .554.647h3.882c.46 0 .85-.334.922-.788.06-.26.76-4.852.816-5.09a.932.932 0 0 1 .923-.788h.58c3.76 0 6.705-1.528 7.565-5.946.36-1.847.174-3.388-.777-4.471z"/>
                  </svg>
                  <span className="text-white font-semibold">{t(language, 'checkout.paypal')}</span>
                </div>
              </button>
            </div>

            <div className="bg-purple-500/20 rounded-xl p-4 mb-6">
              <p className="text-white/80 text-sm">
                <strong className="text-white">{t(language, 'checkout.note')}</strong> {t(language, 'checkout.noteText')}
              </p>
            </div>

            {/* No Refund Policy Checkbox */}
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4 mb-6">
              <div className="flex items-start space-x-3">
                <input
                  type="checkbox"
                  id="noRefund"
                  checked={noRefundAccepted}
                  onChange={(e) => setNoRefundAccepted(e.target.checked)}
                  className="mt-1 w-4 h-4 text-pink-500 bg-transparent border-2 border-yellow-500/50 rounded focus:ring-pink-500 focus:ring-2"
                />
                <label htmlFor="noRefund" className="text-white/90 text-sm leading-relaxed font-medium">
                  ⚠️ {language === 'fr' 
                    ? 'Je comprends et j\'accepte qu\'aucun remboursement ne sera possible après l\'achat de cette formation. La vente est définitive et je m\'engage à respecter cette politique.'
                    : 'I understand and accept that no refund will be possible after purchasing this course. The sale is final and I commit to respecting this policy.'
                  }
                </label>
              </div>
            </div>

            <div className="space-y-3">
              <Button
                onClick={handlePayment}
                disabled={processing}
                className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white py-6 rounded-full font-semibold text-lg"
              >
                {processing ? (
                  <>
                    <Loader2 className="w-5 h-5 mr-2 animate-spin" />
                    {t(language, 'checkout.processing')}
                  </>
                ) : (
                  `${t(language, 'checkout.pay')} ${formation.price}€`
                )}
              </Button>

              <Button
                onClick={() => navigate('/boutique')}
                disabled={processing}
                variant="outline"
                className="w-full border-2 border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white py-6 rounded-full font-semibold text-lg"
              >
                {language === 'fr' ? 'Annuler' : 'Cancel'}
              </Button>
            </div>

            <p className="text-white/50 text-xs text-center mt-4">
              {t(language, 'checkout.secure')}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Checkout;