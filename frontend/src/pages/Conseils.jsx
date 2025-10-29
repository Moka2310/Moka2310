import React, { useState } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { BookOpen, DollarSign, Download, TrendingUp, AlertCircle, CheckCircle2, Shield } from 'lucide-react';

const Conseils = () => {
  const { language } = useLanguage();
  const [activeTab, setActiveTab] = useState('capital');

  const capitalManagement = [
    {
      capital: '500$ - 1,000$',
      forex: '0.01',
      crypto: '0.01',
      gold: '0.01',
      indices: '0.01',
      actions: '0.01',
      risque: 'Très faible',
      color: 'from-green-500 to-emerald-600'
    },
    {
      capital: '1,000$ - 2,500$',
      forex: '0.02',
      crypto: '0.01',
      gold: '0.02',
      indices: '0.02',
      actions: '0.02',
      risque: 'Faible',
      color: 'from-blue-500 to-cyan-600'
    },
    {
      capital: '2,500$ - 5,000$',
      forex: '0.05',
      crypto: '0.02',
      gold: '0.03',
      indices: '0.03',
      actions: '0.03',
      risque: 'Modéré',
      color: 'from-yellow-500 to-orange-600'
    },
    {
      capital: '5,000$ - 10,000$',
      forex: '0.10',
      crypto: '0.05',
      gold: '0.08',
      indices: '0.08',
      actions: '0.08',
      risque: 'Équilibré',
      color: 'from-purple-500 to-pink-600'
    },
    {
      capital: '10,000$+',
      forex: '0.20',
      crypto: '0.10',
      gold: '0.15',
      indices: '0.15',
      actions: '0.15',
      risque: 'Agressif',
      color: 'from-red-500 to-rose-600'
    }
  ];

  const installationSteps = [
    {
      numero: '1',
      titre: 'Achat du TRADABOT',
      description: 'Commandez le TRADABOT sur la page d\'accueil pour 300$ CAD (paiement unique).',
      icon: <DollarSign className="w-6 h-6" />
    },
    {
      numero: '2',
      titre: 'Accès à l\'interface',
      description: 'Une fois le paiement validé, accédez à /tradabot-web depuis votre tableau de bord.',
      icon: <CheckCircle2 className="w-6 h-6" />
    },
    {
      numero: '3',
      titre: 'Télécharger le connecteur',
      description: 'Cliquez sur "📥 Télécharger le Connecteur" et sauvegardez le fichier ZIP.',
      icon: <Download className="w-6 h-6" />
    },
    {
      numero: '4',
      titre: 'Extraire et installer',
      description: 'Dézippez le fichier, exécutez TRADABOT_CONNECTOR.exe sur votre ordinateur Windows.',
      icon: <BookOpen className="w-6 h-6" />
    },
    {
      numero: '5',
      titre: 'Configuration MT4',
      description: 'Dans l\'onglet Configuration, entrez vos identifiants MT4 (login, password, serveur).',
      icon: <Shield className="w-6 h-6" />
    },
    {
      numero: '6',
      titre: 'Choisir les lots',
      description: 'Configurez les lots selon votre capital (voir tableau ci-dessous).',
      icon: <TrendingUp className="w-6 h-6" />
    },
    {
      numero: '7',
      titre: 'Activer les canaux',
      description: 'Sélectionnez les canaux Telegram que vous souhaitez copier (Forex, Crypto, Gold, etc.).',
      icon: <CheckCircle2 className="w-6 h-6" />
    },
    {
      numero: '8',
      titre: 'Lancer le bot',
      description: 'Cliquez sur "▶ DÉMARRER LE BOT" et laissez le connecteur tourner en arrière-plan.',
      icon: <CheckCircle2 className="w-6 h-6" />
    }
  ];

  const tradingTips = [
    {
      titre: 'Ne jamais risquer plus de 2% par trade',
      description: 'La règle d\'or du money management. Même avec des signaux de qualité, le risque doit être maîtrisé.',
      icon: <AlertCircle className="w-5 h-5 text-yellow-400" />
    },
    {
      titre: 'Utilisez un compte RÉEL (pas DEMO)',
      description: 'Les clients doivent obligatoirement connecter un compte réel pour une exécution optimale des ordres.',
      icon: <Shield className="w-5 h-5 text-blue-400" />
    },
    {
      titre: 'Laissez le connecteur actif 24/7',
      description: 'Pour ne manquer aucun signal, gardez votre ordinateur allumé avec le connecteur en marche.',
      icon: <TrendingUp className="w-5 h-5 text-green-400" />
    },
    {
      titre: 'Activez le Breakeven automatique',
      description: 'Cette option sécurise vos trades en déplaçant le stop-loss au point d\'entrée une fois en profit.',
      icon: <CheckCircle2 className="w-5 h-5 text-purple-400" />
    },
    {
      titre: 'Diversifiez les canaux',
      description: 'N\'activez pas tous les canaux si vous avez un petit capital. Commencez par Forex et Gold.',
      icon: <BookOpen className="w-5 h-5 text-pink-400" />
    },
    {
      titre: 'Surveillez votre marge',
      description: 'Assurez-vous d\'avoir suffisamment de marge disponible pour que tous les trades puissent s\'ouvrir.',
      icon: <AlertCircle className="w-5 h-5 text-red-400" />
    }
  ];

  const faq = [
    {
      question: 'Quel broker est recommandé ?',
      reponse: 'Nous recommandons ICMarkets, Exness, XM ou Global Prime pour leurs spreads compétitifs et leur exécution rapide.'
    },
    {
      question: 'Puis-je utiliser plusieurs brokers ?',
      reponse: 'Oui, mais vous devrez configurer un connecteur par broker. Un seul compte TRADABOT peut gérer plusieurs MT4.'
    },
    {
      question: 'Que se passe-t-il si je perds la connexion ?',
      reponse: 'Le connecteur se reconnecte automatiquement. Les signaux manqués pendant la coupure ne seront pas exécutés.'
    },
    {
      question: 'Combien de trades par jour en moyenne ?',
      reponse: 'Entre 3 et 8 trades par jour selon les canaux activés. Les jours de forte volatilité peuvent générer plus de signaux.'
    },
    {
      question: 'Le bot fonctionne-t-il sur Mac/Linux ?',
      reponse: 'Le connecteur est actuellement Windows uniquement. Vous pouvez utiliser une VM Windows ou Wine sur Mac/Linux.'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a0a2e] to-[#2B1F5C] text-white py-20 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
            📚 Conseils & Guide TRADABOT
          </h1>
          <p className="text-xl text-purple-200">
            Tout ce que vous devez savoir pour utiliser TRADABOT efficacement
          </p>
        </div>

        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-8 justify-center">
          <button
            onClick={() => setActiveTab('capital')}
            className={`px-6 py-3 rounded-xl font-semibold transition ${
              activeTab === 'capital'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : 'bg-white/10 text-purple-200 hover:bg-white/20'
            }`}
          >
            💰 Gestion du Capital
          </button>
          <button
            onClick={() => setActiveTab('installation')}
            className={`px-6 py-3 rounded-xl font-semibold transition ${
              activeTab === 'installation'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : 'bg-white/10 text-purple-200 hover:bg-white/20'
            }`}
          >
            🔧 Installation
          </button>
          <button
            onClick={() => setActiveTab('conseils')}
            className={`px-6 py-3 rounded-xl font-semibold transition ${
              activeTab === 'conseils'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : 'bg-white/10 text-purple-200 hover:bg-white/20'
            }`}
          >
            💡 Conseils de Trading
          </button>
          <button
            onClick={() => setActiveTab('faq')}
            className={`px-6 py-3 rounded-xl font-semibold transition ${
              activeTab === 'faq'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : 'bg-white/10 text-purple-200 hover:bg-white/20'
            }`}
          >
            ❓ FAQ
          </button>
        </div>

        {/* Content */}
        <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-3xl p-8 border border-purple-500/30">
          
          {/* Gestion du Capital */}
          {activeTab === 'capital' && (
            <div>
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <DollarSign className="w-8 h-8 text-green-400" />
                Tableau de Gestion des Lots
              </h2>
              <p className="text-purple-200 mb-8">
                Ajustez vos lots selon votre capital pour respecter une gestion de risque optimale.
                <span className="block mt-2 text-yellow-300 font-semibold">
                  ⚠️ Ces valeurs sont des recommandations. Adaptez selon votre tolérance au risque.
                </span>
              </p>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-purple-900/50">
                      <th className="px-4 py-3 text-left">Capital</th>
                      <th className="px-4 py-3 text-center">Forex</th>
                      <th className="px-4 py-3 text-center">Crypto</th>
                      <th className="px-4 py-3 text-center">Gold</th>
                      <th className="px-4 py-3 text-center">Indices</th>
                      <th className="px-4 py-3 text-center">Actions</th>
                      <th className="px-4 py-3 text-right">Niveau de Risque</th>
                    </tr>
                  </thead>
                  <tbody>
                    {capitalManagement.map((row, index) => (
                      <tr key={index} className="border-b border-purple-500/20 hover:bg-purple-500/10 transition">
                        <td className="px-4 py-4 font-bold text-purple-200">{row.capital}</td>
                        <td className="px-4 py-4 text-center font-mono text-green-300">{row.forex}</td>
                        <td className="px-4 py-4 text-center font-mono text-blue-300">{row.crypto}</td>
                        <td className="px-4 py-4 text-center font-mono text-yellow-300">{row.gold}</td>
                        <td className="px-4 py-4 text-center font-mono text-pink-300">{row.indices}</td>
                        <td className="px-4 py-4 text-center font-mono text-orange-300">{row.actions}</td>
                        <td className="px-4 py-4 text-right">
                          <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold bg-gradient-to-r ${row.color} text-white`}>
                            {row.risque}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="mt-8 bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-6">
                <h3 className="text-xl font-bold text-yellow-300 mb-3 flex items-center gap-2">
                  <AlertCircle className="w-6 h-6" />
                  Important
                </h3>
                <ul className="space-y-2 text-purple-200">
                  <li>• Commencez toujours par le niveau de risque le plus faible</li>
                  <li>• Augmentez progressivement les lots après 2-3 semaines de résultats positifs</li>
                  <li>• Ne risquez JAMAIS plus de 5% de votre capital total sur une journée</li>
                  <li>• Gardez toujours une marge de sécurité d'au moins 30% disponible</li>
                </ul>
              </div>
            </div>
          )}

          {/* Installation */}
          {activeTab === 'installation' && (
            <div>
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <BookOpen className="w-8 h-8 text-blue-400" />
                Guide d'Installation Pas à Pas
              </h2>
              
              <div className="space-y-6">
                {installationSteps.map((step, index) => (
                  <div key={index} className="flex gap-4 bg-purple-900/30 rounded-xl p-6 border border-purple-500/20 hover:border-purple-400/50 transition">
                    <div className="flex-shrink-0">
                      <div className="w-12 h-12 rounded-full bg-gradient-to-r from-pink-500 to-purple-600 flex items-center justify-center font-bold text-xl">
                        {step.numero}
                      </div>
                    </div>
                    <div className="flex-1">
                      <div className="flex items-center gap-2 mb-2">
                        <div className="text-purple-400">{step.icon}</div>
                        <h3 className="text-xl font-bold text-white">{step.titre}</h3>
                      </div>
                      <p className="text-purple-200">{step.description}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 bg-blue-500/10 border border-blue-500/30 rounded-xl p-6">
                <h3 className="text-xl font-bold text-blue-300 mb-3">📝 Note Technique</h3>
                <p className="text-purple-200">
                  Le connecteur doit rester en exécution pendant les heures de trading. Nous recommandons d'utiliser 
                  un VPS Windows si vous ne pouvez pas garder votre ordinateur allumé 24/7.
                </p>
              </div>
            </div>
          )}

          {/* Conseils */}
          {activeTab === 'conseils' && (
            <div>
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <TrendingUp className="w-8 h-8 text-green-400" />
                Conseils de Trading Essentiels
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                {tradingTips.map((tip, index) => (
                  <div key={index} className="bg-purple-900/30 rounded-xl p-6 border border-purple-500/20 hover:border-purple-400/50 transition">
                    <div className="flex items-start gap-3 mb-3">
                      {tip.icon}
                      <h3 className="text-lg font-bold text-white">{tip.titre}</h3>
                    </div>
                    <p className="text-purple-200 text-sm">{tip.description}</p>
                  </div>
                ))}
              </div>

              <div className="mt-8 bg-red-500/10 border border-red-500/30 rounded-xl p-6">
                <h3 className="text-xl font-bold text-red-300 mb-3 flex items-center gap-2">
                  <AlertCircle className="w-6 h-6" />
                  Avertissement
                </h3>
                <p className="text-purple-200">
                  Le trading comporte des risques. Même avec des signaux de qualité, des pertes sont possibles. 
                  N'investissez que de l'argent que vous pouvez vous permettre de perdre. Les performances passées 
                  ne garantissent pas les résultats futurs.
                </p>
              </div>
            </div>
          )}

          {/* FAQ */}
          {activeTab === 'faq' && (
            <div>
              <h2 className="text-3xl font-bold mb-6">❓ Questions Fréquentes</h2>
              
              <div className="space-y-4">
                {faq.map((item, index) => (
                  <div key={index} className="bg-purple-900/30 rounded-xl p-6 border border-purple-500/20">
                    <h3 className="text-xl font-bold text-purple-200 mb-3">{item.question}</h3>
                    <p className="text-purple-300">{item.reponse}</p>
                  </div>
                ))}
              </div>

              <div className="mt-8 bg-purple-500/10 border border-purple-500/30 rounded-xl p-6 text-center">
                <h3 className="text-xl font-bold text-purple-200 mb-3">Besoin d'aide ?</h3>
                <p className="text-purple-300 mb-4">
                  Rejoignez notre canal Telegram de support pour obtenir de l'aide en temps réel
                </p>
                <button className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-3 rounded-full font-bold transition">
                  💬 Rejoindre le Support
                </button>
              </div>
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default Conseils;
