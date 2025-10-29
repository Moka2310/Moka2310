import React, { useState, useEffect } from 'react';
import { useLanguage } from '../contexts/LanguageContext';
import { BookOpen, DollarSign, Download, TrendingUp, AlertCircle, CheckCircle2, Shield } from 'lucide-react';
import { conseilsTranslations } from '../conseilsTranslations';

const t = (lang, key) => {
  const keys = key.split('.');
  let value = conseilsTranslations[lang];
  for (const k of keys) {
    value = value?.[k];
  }
  return value || key;
};

const Conseils = () => {
  const { language } = useLanguage();
  const [activeTab, setActiveTab] = useState('capital');
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  useEffect(() => {
    loadContent();
  }, []);

  const loadContent = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/conseils/content`);
      const data = await response.json();
      setContent(data);
      setLoading(false);
    } catch (error) {
      console.error('Erreur chargement conseils:', error);
      setLoading(false);
    }
  };

  if (loading || !content) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#1a0a2e] to-[#2B1F5C] flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  const capitalManagement = content.capitalManagement || [];
  const installationSteps = content.installationSteps || [];
  const tradingTips = content.tradingTips || [];
  const faq = content.faq || [];

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1a0a2e] to-[#2B1F5C] text-white py-20 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl md:text-5xl font-bold mb-4 bg-gradient-to-r from-pink-400 to-purple-400 bg-clip-text text-transparent">
            {t(language, 'conseils.title')}
          </h1>
          <p className="text-xl text-purple-200">
            {t(language, 'conseils.subtitle')}
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
            {t(language, 'conseils.tabs.capital')}
          </button>
          <button
            onClick={() => setActiveTab('installation')}
            className={`px-6 py-3 rounded-xl font-semibold transition ${
              activeTab === 'installation'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : 'bg-white/10 text-purple-200 hover:bg-white/20'
            }`}
          >
            {t(language, 'conseils.tabs.installation')}
          </button>
          <button
            onClick={() => setActiveTab('conseils')}
            className={`px-6 py-3 rounded-xl font-semibold transition ${
              activeTab === 'conseils'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : 'bg-white/10 text-purple-200 hover:bg-white/20'
            }`}
          >
            {t(language, 'conseils.tabs.tips')}
          </button>
          <button
            onClick={() => setActiveTab('faq')}
            className={`px-6 py-3 rounded-xl font-semibold transition ${
              activeTab === 'faq'
                ? 'bg-gradient-to-r from-pink-500 to-purple-600 text-white'
                : 'bg-white/10 text-purple-200 hover:bg-white/20'
            }`}
          >
            {t(language, 'conseils.tabs.faq')}
          </button>
        </div>

        {/* Content */}
        <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-3xl p-8 border border-purple-500/30">
          
          {/* Gestion du Capital */}
          {activeTab === 'capital' && (
            <div>
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <DollarSign className="w-8 h-8 text-green-400" />
                {t(language, 'conseils.capital.title')}
              </h2>
              <p className="text-purple-200 mb-8">
                {t(language, 'conseils.capital.subtitle')}
                <span className="block mt-2 text-yellow-300 font-semibold">
                  {t(language, 'conseils.capital.warning')}
                </span>
              </p>

              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead>
                    <tr className="bg-purple-900/50">
                      <th className="px-4 py-3 text-left">{t(language, 'conseils.capital.table.capital')}</th>
                      <th className="px-4 py-3 text-center">{t(language, 'conseils.capital.table.forex')}</th>
                      <th className="px-4 py-3 text-center">{t(language, 'conseils.capital.table.crypto')}</th>
                      <th className="px-4 py-3 text-center">{t(language, 'conseils.capital.table.gold')}</th>
                      <th className="px-4 py-3 text-center">{t(language, 'conseils.capital.table.indices')}</th>
                      <th className="px-4 py-3 text-center">{t(language, 'conseils.capital.table.actions')}</th>
                      <th className="px-4 py-3 text-right">{t(language, 'conseils.capital.table.risk')}</th>
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
                  {t(language, 'conseils.capital.important.title')}
                </h3>
                <ul className="space-y-2 text-purple-200">
                  {t(language, 'conseils.capital.important.points').map((point, i) => (
                    <li key={i}>• {point}</li>
                  ))}
                </ul>
              </div>
            </div>
          )}

          {/* Installation */}
          {activeTab === 'installation' && (
            <div>
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <BookOpen className="w-8 h-8 text-blue-400" />
                {t(language, 'conseils.installation.title')}
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
                      <h3 className="text-xl font-bold text-white mb-2">{step.titre}</h3>
                      <p className="text-purple-200">{step.description}</p>
                    </div>
                  </div>
                ))}
              </div>

              <div className="mt-8 bg-blue-500/10 border border-blue-500/30 rounded-xl p-6">
                <h3 className="text-xl font-bold text-blue-300 mb-3">{t(language, 'conseils.installation.note.title')}</h3>
                <p className="text-purple-200">
                  {t(language, 'conseils.installation.note.description')}
                </p>
              </div>
            </div>
          )}

          {/* Conseils */}
          {activeTab === 'conseils' && (
            <div>
              <h2 className="text-3xl font-bold mb-6 flex items-center gap-3">
                <TrendingUp className="w-8 h-8 text-green-400" />
                {t(language, 'conseils.tips.title')}
              </h2>
              
              <div className="grid md:grid-cols-2 gap-6">
                {tradingTips.map((tip, index) => (
                  <div key={index} className="bg-purple-900/30 rounded-xl p-6 border border-purple-500/20 hover:border-purple-400/50 transition">
                    <h3 className="text-lg font-bold text-white mb-3">{tip.titre}</h3>
                    <p className="text-purple-200 text-sm">{tip.description}</p>
                  </div>
                ))}
              </div>

              <div className="mt-8 bg-red-500/10 border border-red-500/30 rounded-xl p-6">
                <h3 className="text-xl font-bold text-red-300 mb-3 flex items-center gap-2">
                  <AlertCircle className="w-6 h-6" />
                  {t(language, 'conseils.tips.warning.title')}
                </h3>
                <p className="text-purple-200">
                  {t(language, 'conseils.tips.warning.description')}
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
