import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { formationsAPI } from '../api/client';
import { ShoppingCart, Clock, BarChart3, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/button';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { t, translations } from '../translations';
import { toast } from '../hooks/use-toast';

const Boutique = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { language } = useLanguage();
  const [formations, setFormations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadFormations = async () => {
      try {
        const response = await formationsAPI.getAll();
        setFormations(response.data);
      } catch (error) {
        console.error('Failed to load formations:', error);
        toast({
          title: t(language, 'common.error'),
          description: 'Impossible de charger les formations',
          variant: 'destructive'
        });
      } finally {
        setLoading(false);
      }
    };

    loadFormations();
  }, [language]);

  const handlePurchase = (formation) => {
    if (!user) {
      navigate('/login', { state: { returnTo: '/boutique', formationId: formation.id } });
      return;
    }

    // Check KYC status - must have submitted documents (pending or approved)
    if (!user.kycStatus || user.kycStatus === 'rejected') {
      toast({
        title: language === 'fr' ? '⚠️ Documents KYC requis' : '⚠️ KYC documents required',
        description: language === 'fr' 
          ? 'Vous devez soumettre vos documents KYC avant de pouvoir acheter. Rendez-vous dans votre Dashboard.'
          : 'You must submit your KYC documents before purchasing. Go to your Dashboard.',
        variant: 'destructive',
        duration: 5000
      });
      
      // Redirect to dashboard KYC tab
      setTimeout(() => {
        navigate('/dashboard?tab=kyc');
      }, 1500);
      return;
    }

    // Can purchase if pending or approved
    navigate('/checkout', { state: { formation } });
  };
  
  // Get translated formation info
  const getFormationTitle = (formation) => {
    const translationKey = `formations.${formation.title}.title`;
    return translations[language]?.formations?.[formation.title]?.title || formation.title;
  };
  
  const getFormationDescription = (formation) => {
    return translations[language]?.formations?.[formation.title]?.description || formation.description;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4 flex items-center justify-center">
        <div className="text-white text-xl">{t(language, 'common.loading')}</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <Button
          onClick={() => navigate('/')}
          variant="ghost"
          className="mb-6 text-pink-400 hover:text-pink-300 hover:bg-pink-500/10"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          {language === 'fr' ? 'Retour à l\'accueil' : 'Back to home'}
        </Button>

        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
              {t(language, 'shop.title')}
            </span>
          </h1>
          <p className="text-white/70 text-lg max-w-2xl mx-auto">
            {t(language, 'shop.subtitle')}
          </p>
        </div>

        {/* Formations Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
          {formations.map((formation) => (
            <div
              key={formation.id}
              className="group bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl overflow-hidden border border-purple-500/30 hover:border-pink-500/50 transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-pink-500/20"
            >
              {/* Image */}
              <div className="relative h-56 overflow-hidden">
                <img
                  src={formation.image}
                  alt={getFormationTitle(formation)}
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-[#1E1540] via-transparent to-transparent"></div>
                <div className="absolute top-4 right-4 bg-pink-500 text-white px-4 py-2 rounded-full font-bold">
                  {formation.price} CAD
                </div>
              </div>

              {/* Content */}
              <div className="p-6">
                <h3 className="text-2xl font-bold text-white mb-3">{getFormationTitle(formation)}</h3>
                <div className="text-white/90 mb-4 whitespace-pre-line leading-relaxed text-sm">
                  {getFormationDescription(formation)}
                </div>

                {/* Info Tags */}
                <div className="flex flex-wrap gap-2 mb-6">
                  <div className="flex items-center space-x-2 bg-purple-500/20 px-3 py-1 rounded-full">
                    <Clock className="w-4 h-4 text-pink-400" />
                    <span className="text-white/80 text-sm">{formation.duration}</span>
                  </div>
                  <div className="flex items-center space-x-2 bg-purple-500/20 px-3 py-1 rounded-full">
                    <BarChart3 className="w-4 h-4 text-pink-400" />
                    <span className="text-white/80 text-sm">{formation.level}</span>
                  </div>
                  <div className="bg-purple-500/20 px-3 py-1 rounded-full">
                    <span className="text-white/80 text-sm">{formation.videoCount} {language === 'fr' ? 'vidéos' : 'videos'}</span>
                  </div>
                </div>

                {/* Buy Button */}
                <Button
                  onClick={() => handlePurchase(formation)}
                  className={`w-full py-6 rounded-full font-semibold text-lg group ${
                    user?.kycStatus === 'approved' || user?.kycStatus === 'pending'
                      ? 'bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white'
                      : 'bg-yellow-500/20 border-2 border-yellow-500 text-yellow-300 hover:bg-yellow-500/30'
                  }`}
                >
                  <ShoppingCart className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
                  {user?.kycStatus === 'approved' || user?.kycStatus === 'pending'
                    ? t(language, 'shop.buy')
                    : (language === 'fr' ? 'Documents KYC requis' : 'KYC documents required')
                  }
                </Button>
                
                {/* KYC Warning */}
                {user && user.kycStatus !== 'approved' && user.kycStatus !== 'pending' && (
                  <p className="text-yellow-400 text-xs mt-2 text-center">
                    {language === 'fr' 
                      ? '⚠️ Soumettez vos documents KYC dans le Dashboard'
                      : '⚠️ Submit your KYC documents in Dashboard'
                    }
                  </p>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Benefits Section */}
        <div className="mt-20 bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-3xl p-8 md:p-12 border border-purple-500/30">
          <h2 className="text-3xl font-bold text-center text-white mb-8">
            {t(language, 'shop.includes')}
          </h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{language === 'fr' ? 'Vidéos HD' : 'HD Videos'}</h3>
              <p className="text-white/70">{t(language, 'shop.benefits.videos')}</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{language === 'fr' ? 'Canaux Telegram VIP' : 'VIP Telegram Channels'}</h3>
              <p className="text-white/70">{t(language, 'shop.benefits.telegram')}</p>
            </div>
            <div className="text-center">
              <div className="w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 5.636l-3.536 3.536m0 5.656l3.536 3.536M9.172 9.172L5.636 5.636m3.536 9.192l-3.536 3.536M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-5 0a4 4 0 11-8 0 4 4 0 018 0z" />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">{t(language, 'shop.benefits.support')}</h3>
              <p className="text-white/70">{language === 'fr' ? 'Équipe disponible pour répondre à toutes vos questions' : 'Team available to answer all your questions'}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Boutique;