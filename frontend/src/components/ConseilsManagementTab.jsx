import React, { useState, useEffect } from 'react';
import { Save, Plus, Trash2, Edit2 } from 'lucide-react';

const ConseilsManagementTab = ({ language }) => {
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [activeSection, setActiveSection] = useState('capital');

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

  const saveContent = async () => {
    setSaving(true);
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await fetch(`${BACKEND_URL}/api/conseils/content`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(content)
      });

      if (response.ok) {
        alert('✅ Conseils mis à jour avec succès!');
      } else {
        alert('❌ Erreur lors de la mise à jour');
      }
    } catch (error) {
      console.error('Erreur sauvegarde:', error);
      alert('❌ Erreur réseau');
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-white">📚 Gestion des Conseils</h2>
        <button
          onClick={saveContent}
          disabled={saving}
          className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-6 py-2 rounded-lg font-bold flex items-center gap-2 disabled:opacity-50"
        >
          <Save className="w-5 h-5" />
          {saving ? 'Sauvegarde...' : 'Sauvegarder tout'}
        </button>
      </div>

      {/* Section Tabs */}
      <div className="flex gap-2 flex-wrap">
        <button
          onClick={() => setActiveSection('capital')}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            activeSection === 'capital'
              ? 'bg-purple-600 text-white'
              : 'bg-white/10 text-purple-200 hover:bg-white/20'
          }`}
        >
          💰 Gestion du Capital
        </button>
        <button
          onClick={() => setActiveSection('installation')}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            activeSection === 'installation'
              ? 'bg-purple-600 text-white'
              : 'bg-white/10 text-purple-200 hover:bg-white/20'
          }`}
        >
          🔧 Installation
        </button>
        <button
          onClick={() => setActiveSection('tips')}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            activeSection === 'tips'
              ? 'bg-purple-600 text-white'
              : 'bg-white/10 text-purple-200 hover:bg-white/20'
          }`}
        >
          💡 Conseils
        </button>
        <button
          onClick={() => setActiveSection('faq')}
          className={`px-4 py-2 rounded-lg font-semibold transition ${
            activeSection === 'faq'
              ? 'bg-purple-600 text-white'
              : 'bg-white/10 text-purple-200 hover:bg-white/20'
          }`}
        >
          ❓ FAQ
        </button>
      </div>

      {/* Content Editor */}
      <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/30">
        
        {/* Gestion du Capital */}
        {activeSection === 'capital' && content?.capitalManagement && (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Tableau de Gestion du Capital</h3>
            {content.capitalManagement.map((row, index) => (
              <div key={index} className="bg-purple-900/30 rounded-xl p-4 space-y-3">
                <div className="grid grid-cols-3 gap-3">
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Capital</label>
                    <input
                      type="text"
                      value={row.capital}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.capitalManagement[index].capital = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Forex</label>
                    <input
                      type="text"
                      value={row.forex}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.capitalManagement[index].forex = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Crypto</label>
                    <input
                      type="text"
                      value={row.crypto}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.capitalManagement[index].crypto = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-4 gap-3">
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Gold</label>
                    <input
                      type="text"
                      value={row.gold}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.capitalManagement[index].gold = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Indices</label>
                    <input
                      type="text"
                      value={row.indices}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.capitalManagement[index].indices = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Actions</label>
                    <input
                      type="text"
                      value={row.actions}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.capitalManagement[index].actions = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Niveau de Risque</label>
                    <input
                      type="text"
                      value={row.risque}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.capitalManagement[index].risque = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Installation */}
        {activeSection === 'installation' && content?.installationSteps && (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Étapes d'Installation</h3>
            {content.installationSteps.map((step, index) => (
              <div key={index} className="bg-purple-900/30 rounded-xl p-4 space-y-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Numéro</label>
                    <input
                      type="text"
                      value={step.numero}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.installationSteps[index].numero = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-1">Titre</label>
                    <input
                      type="text"
                      value={step.titre}
                      onChange={(e) => {
                        const newContent = {...content};
                        newContent.installationSteps[index].titre = e.target.value;
                        setContent(newContent);
                      }}
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                    />
                  </div>
                </div>
                <div>
                  <label className="block text-purple-300 text-sm mb-1">Description</label>
                  <textarea
                    value={step.description}
                    onChange={(e) => {
                      const newContent = {...content};
                      newContent.installationSteps[index].description = e.target.value;
                      setContent(newContent);
                    }}
                    rows={3}
                    className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Conseils de Trading */}
        {activeSection === 'tips' && content?.tradingTips && (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">Conseils de Trading</h3>
            {content.tradingTips.map((tip, index) => (
              <div key={index} className="bg-purple-900/30 rounded-xl p-4 space-y-3">
                <div>
                  <label className="block text-purple-300 text-sm mb-1">Titre</label>
                  <input
                    type="text"
                    value={tip.titre}
                    onChange={(e) => {
                      const newContent = {...content};
                      newContent.tradingTips[index].titre = e.target.value;
                      setContent(newContent);
                    }}
                    className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                  />
                </div>
                <div>
                  <label className="block text-purple-300 text-sm mb-1">Description</label>
                  <textarea
                    value={tip.description}
                    onChange={(e) => {
                      const newContent = {...content};
                      newContent.tradingTips[index].description = e.target.value;
                      setContent(newContent);
                    }}
                    rows={3}
                    className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                  />
                </div>
              </div>
            ))}
          </div>
        )}

        {/* FAQ */}
        {activeSection === 'faq' && content?.faq && (
          <div className="space-y-4">
            <h3 className="text-xl font-bold text-white mb-4">FAQ</h3>
            {content.faq.map((item, index) => (
              <div key={index} className="bg-purple-900/30 rounded-xl p-4 space-y-3">
                <div>
                  <label className="block text-purple-300 text-sm mb-1">Question</label>
                  <input
                    type="text"
                    value={item.question}
                    onChange={(e) => {
                      const newContent = {...content};
                      newContent.faq[index].question = e.target.value;
                      setContent(newContent);
                    }}
                    className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                  />
                </div>
                <div>
                  <label className="block text-purple-300 text-sm mb-1">Réponse</label>
                  <textarea
                    value={item.reponse}
                    onChange={(e) => {
                      const newContent = {...content};
                      newContent.faq[index].reponse = e.target.value;
                      setContent(newContent);
                    }}
                    rows={3}
                    className="w-full bg-purple-900/20 border border-purple-500/30 rounded px-3 py-2 text-white"
                  />
                </div>
              </div>
            ))}
          </div>
        )}

      </div>
    </div>
  );
};

export default ConseilsManagementTab;
