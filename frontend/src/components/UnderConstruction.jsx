import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Construction, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { useLanguage } from '../contexts/LanguageContext';

const UnderConstruction = ({ page = "paiements" }) => {
  const navigate = useNavigate();
  const { language } = useLanguage();

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4 flex items-center justify-center">
      <div className="max-w-2xl mx-auto text-center">
        {/* Back Button */}
        <Button
          onClick={() => navigate('/')}
          variant="ghost"
          className="mb-8 text-pink-400 hover:text-pink-300 hover:bg-pink-500/10"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          {language === 'fr' ? 'Retour à l\'accueil' : 'Back to home'}
        </Button>

        {/* Icon */}
        <div className="mb-8 flex justify-center">
          <div className="relative">
            <div className="absolute inset-0 bg-gradient-to-r from-pink-500 to-purple-600 rounded-full blur-3xl opacity-50 animate-pulse"></div>
            <div className="relative bg-gradient-to-br from-pink-500 to-purple-600 rounded-full p-8">
              <Construction className="w-20 h-20 text-white" />
            </div>
          </div>
        </div>

        {/* Title */}
        <h1 className="text-4xl md:text-5xl font-bold mb-6">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
            {language === 'fr' ? '🚧 En Construction 🚧' : '🚧 Under Construction 🚧'}
          </span>
        </h1>

        {/* Message */}
        <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-3xl p-8 border border-purple-500/30 mb-8">
          <p className="text-white/90 text-lg mb-4">
            {language === 'fr' 
              ? "Nous finalisons actuellement les systèmes de paiement pour vous offrir la meilleure expérience possible."
              : "We are currently finalizing the payment systems to offer you the best possible experience."}
          </p>
          <p className="text-white/70 text-base">
            {language === 'fr'
              ? "Cette section sera bientôt disponible. Merci de votre patience!"
              : "This section will be available soon. Thank you for your patience!"}
          </p>
        </div>

        {/* Features Coming Soon */}
        <div className="bg-white/5 backdrop-blur-sm rounded-2xl p-6 border border-white/10 mb-8">
          <h3 className="text-xl font-bold text-white mb-4">
            {language === 'fr' ? '🎯 Bientôt disponible :' : '🎯 Coming Soon:'}
          </h3>
          <div className="grid md:grid-cols-2 gap-4 text-left">
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <span className="text-green-400 text-sm">✓</span>
              </div>
              <span className="text-white/80 text-sm">
                {language === 'fr' ? 'Paiements par carte bancaire (Stripe)' : 'Credit card payments (Stripe)'}
              </span>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <span className="text-green-400 text-sm">✓</span>
              </div>
              <span className="text-white/80 text-sm">
                {language === 'fr' ? 'Paiements PayPal' : 'PayPal payments'}
              </span>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <span className="text-green-400 text-sm">✓</span>
              </div>
              <span className="text-white/80 text-sm">
                {language === 'fr' ? 'Sécurité 3D Secure' : '3D Secure security'}
              </span>
            </div>
            <div className="flex items-start space-x-3">
              <div className="w-6 h-6 bg-green-500/20 rounded-full flex items-center justify-center flex-shrink-0 mt-1">
                <span className="text-green-400 text-sm">✓</span>
              </div>
              <span className="text-white/80 text-sm">
                {language === 'fr' ? 'Confirmations instantanées' : 'Instant confirmations'}
              </span>
            </div>
          </div>
        </div>

        {/* Contact Info */}
        <div className="text-white/60 text-sm">
          <p>
            {language === 'fr'
              ? "Pour toute question, contactez-nous à"
              : "For any questions, contact us at"}
            {' '}
            <a href="mailto:support@tradalife.com" className="text-pink-400 hover:text-pink-300 underline">
              support@tradalife.com
            </a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default UnderConstruction;
