import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const CanalDetails = () => {
  const { canalName } = useParams();
  const navigate = useNavigate();
  const { language } = useLanguage();

  // Définir les actifs pour chaque canal
  const canalsData = {
    crypto: {
      name: { fr: 'CRYPTO', en: 'CRYPTO' },
      description: { 
        fr: 'Trading de cryptomonnaies sur les paires majeures',
        en: 'Cryptocurrency trading on major pairs'
      },
      assets: ['BTCUSD', 'ETHUSD', 'BNBUSD', 'SOLUSD', 'ADAUSD']
    },
    gold: {
      name: { fr: 'GOLD', en: 'GOLD' },
      description: { 
        fr: 'Trading de l\'or et métaux précieux',
        en: 'Gold and precious metals trading'
      },
      assets: ['XAUUSD', 'XAGUSD', 'GOLD']
    },
    forex: {
      name: { fr: 'FOREX', en: 'FOREX' },
      description: { 
        fr: 'Trading des paires de devises majeures et exotiques',
        en: 'Major and exotic currency pairs trading'
      },
      assets: ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'NZDUSD', 'USDCHF', 'EURGBP', 'EURJPY']
    },
    indices: {
      name: { fr: 'INDICES', en: 'INDICES' },
      description: { 
        fr: 'Trading des indices boursiers mondiaux',
        en: 'Global stock indices trading'
      },
      assets: ['US30', 'US500', 'NAS100', 'GER40', 'UK100', 'JPN225']
    },
    petrole: {
      name: { fr: 'PÉTROLE & GAZ', en: 'OIL & GAS' },
      description: { 
        fr: 'Trading des matières premières énergétiques',
        en: 'Energy commodities trading'
      },
      assets: ['WTI', 'BRENT', 'NATGAS']
    },
    actions: {
      name: { fr: 'ACTIONS', en: 'STOCKS' },
      description: { 
        fr: 'Trading des actions des grandes entreprises',
        en: 'Major companies stock trading'
      },
      assets: ['AAPL', 'TSLA', 'AMZN', 'GOOGL', 'MSFT', 'META', 'NVDA', 'NFLX']
    }
  };

  const canal = canalsData[canalName?.toLowerCase()];

  if (!canal) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#1E1540] via-black to-[#1E1540] flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-4">Canal non trouvé</h1>
          <button
            onClick={() => navigate('/')}
            className="text-pink-400 hover:text-pink-300"
          >
            Retour à l'accueil
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1E1540] via-black to-[#1E1540] pt-24 pb-16">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Bouton retour */}
        <button
          onClick={() => navigate('/')}
          className="flex items-center space-x-2 text-pink-400 hover:text-pink-300 mb-8 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>{language === 'fr' ? 'Retour à l\'accueil' : 'Back to home'}</span>
        </button>

        {/* En-tête du canal */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-500 via-purple-500 to-pink-500 bg-clip-text text-transparent mb-4">
            {canal.name[language]}
          </h1>
          <p className="text-white/70 text-lg">
            {canal.description[language]}
          </p>
        </div>

        {/* Liste des actifs */}
        <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-lg rounded-2xl p-8 border border-purple-500/30">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            {language === 'fr' ? 'Liste des actifs tradés' : 'List of traded assets'}
          </h2>
          
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {canal.assets.map((asset, index) => (
              <div
                key={index}
                className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-xl p-6 text-center border border-purple-500/30 hover:border-pink-500/50 transition-all duration-300 hover:scale-105"
              >
                <p className="text-white font-bold text-xl">{asset}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Info supplémentaire */}
        <div className="mt-8 text-center">
          <p className="text-white/60 text-sm">
            {language === 'fr' 
              ? 'Ces actifs sont disponibles sur notre canal Telegram VIP'
              : 'These assets are available on our VIP Telegram channel'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default CanalDetails;
