import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const CanalDetails = () => {
  const { canalName } = useParams();
  const navigate = useNavigate();
  const { language } = useLanguage();

  // Scroll to top when page loads
  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [canalName]);

  // Définir les actifs pour chaque canal
  const canalsData = {
    crypto: {
      name: { fr: 'CRYPTO', en: 'CRYPTO' },
      description: { 
        fr: 'Trading de cryptomonnaies',
        en: 'Cryptocurrency trading'
      },
      assets: ['BTCUSD']
    },
    gold: {
      name: { fr: 'GOLD', en: 'GOLD' },
      description: { 
        fr: 'Trading de l\'or et métaux précieux',
        en: 'Gold and precious metals trading'
      },
      assets: ['XAUUSD', 'XAUEUR', 'XAGUSD', 'XAGEUR']
    },
    forex: {
      name: { fr: 'FOREX', en: 'FOREX' },
      description: { 
        fr: 'Trading des paires de devises',
        en: 'Currency pairs trading'
      },
      assets: ['USDJPY', 'USDCAD', 'USDCHF', 'GBPJPY', 'GBPUSD', 'GBPAUD', 'GBPCAD', 'GBPNZD', 'GBPCHF', 'EURUSD', 'EURAUD', 'EURJPY', 'EURNZD', 'EURCAD', 'AUDJPY', 'AUDCHF', 'AUDUSD', 'AUDCAD', 'NZDUSD', 'CADJPY', 'NZDJPY', 'NZDCHF', 'NZDCAD']
    },
    indices: {
      name: { fr: 'INDICES', en: 'INDICES' },
      description: { 
        fr: 'Trading des indices boursiers',
        en: 'Stock indices trading'
      },
      assets: ['NAS100', 'UK100', 'FRA40', 'HK50', 'US500']
    },
    commodites: {
      name: { fr: 'COMMODITÉS', en: 'COMMODITIES' },
      description: { 
        fr: 'Trading des matières premières',
        en: 'Commodities trading'
      },
      assets: ['SUGARRAW', 'SOYBEAN', 'XTIUSD', 'XPTUSD', 'XPDUSD', 'WHEAT', 'CORN']
    },
    actions: {
      name: { fr: 'ACTIONS', en: 'STOCKS' },
      description: { 
        fr: 'Trading des actions',
        en: 'Stock trading'
      },
      assets: ['AAPL', 'AAL', 'ADBE', 'AMD', 'AMZN', 'EA', 'EBAY', 'META', 'GOOG', 'MSFT', 'NFLX', 'NVDA', 'PEP', 'TSLA']
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
          onClick={() => {
            navigate('/');
            setTimeout(() => {
              document.getElementById('canaux')?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
          }}
          className="flex items-center space-x-2 text-pink-400 hover:text-pink-300 mb-8 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>{language === 'fr' ? 'Retour aux canaux' : 'Back to channels'}</span>
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
