import React, { useState, useEffect } from 'react';
import { Activity, Settings, TrendingUp, List, AlertCircle, CheckCircle, Play, Square } from 'lucide-react';

const TradabotWeb = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [botStatus, setBotStatus] = useState('stopped'); // stopped, running, error
  const [config, setConfig] = useState({
    mt4Login: '',
    mt4Password: '',
    mt4Server: '',
    channels: {
      forex: false,
      crypto: false,
      gold: false,
      indices: false,
      actions: false,
      commodites: false
    },
    lots: {
      forex: 0.01,
      crypto: 0.01,
      gold: 0.01,
      indices: 0.01,
      actions: 0.01,
      commodites: 0.01
    },
    breakevenEnabled: true
  });
  const [signals, setSignals] = useState([]);
  const [trades, setTrades] = useState([]);
  const [connectorStatus, setConnectorStatus] = useState('disconnected'); // disconnected, connected

  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  // Charger la configuration au démarrage
  useEffect(() => {
    loadConfig();
    loadSignals();
    loadTrades();
    checkConnectorStatus();
    
    // Rafraîchir toutes les 10 secondes
    const interval = setInterval(() => {
      loadSignals();
      loadTrades();
      checkConnectorStatus();
    }, 10000);
    
    return () => clearInterval(interval);
  }, []);

  const loadConfig = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await fetch(`${BACKEND_URL}/api/tradabot-web/config`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setConfig(data);
      }
    } catch (error) {
      console.error('Erreur chargement config:', error);
    }
  };

  const saveConfig = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await fetch(`${BACKEND_URL}/api/tradabot-web/config`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
      });
      
      if (response.ok) {
        alert('✅ Configuration sauvegardée!');
      } else {
        alert('❌ Erreur lors de la sauvegarde');
      }
    } catch (error) {
      console.error('Erreur sauvegarde:', error);
      alert('❌ Erreur réseau');
    }
  };

  const loadSignals = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await fetch(`${BACKEND_URL}/api/tradabot-web/signals?limit=20`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setSignals(data);
      }
    } catch (error) {
      console.error('Erreur chargement signaux:', error);
    }
  };

  const loadTrades = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await fetch(`${BACKEND_URL}/api/tradabot-web/trades?limit=20`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setTrades(data);
      }
    } catch (error) {
      console.error('Erreur chargement trades:', error);
    }
  };

  const checkConnectorStatus = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await fetch(`${BACKEND_URL}/api/tradabot-web/connector-status`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (response.ok) {
        const data = await response.json();
        setConnectorStatus(data.status);
        setBotStatus(data.botStatus || 'stopped');
      }
    } catch (error) {
      setConnectorStatus('disconnected');
    }
  };

  const downloadConnector = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await fetch(`${BACKEND_URL}/api/tradabot-web/download-connector`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'TRADABOT_CONNECTOR.zip';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        alert('✅ Téléchargement démarré!');
      } else {
        alert('❌ Erreur lors du téléchargement');
      }
    } catch (error) {
      console.error('Erreur téléchargement:', error);
      alert('❌ Erreur réseau');
    }
  };

  const toggleBot = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const newStatus = botStatus === 'running' ? 'stopped' : 'running';
      
      const response = await fetch(`${BACKEND_URL}/api/tradabot-web/toggle-bot`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ status: newStatus })
      });
      
      if (response.ok) {
        setBotStatus(newStatus);
      }
    } catch (error) {
      console.error('Erreur toggle bot:', error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#0a0118] via-[#16001e] to-[#1a0a2e] text-white p-6">
      <div className="max-w-7xl mx-auto">
        
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 bg-gradient-to-r from-pink-400 via-purple-500 to-violet-600 bg-clip-text text-transparent">
            🤖 TRADABOT
          </h1>
          <p className="text-white/60">Trading automatique - Signaux Telegram → MT4</p>
        </div>

        {/* Status Bar */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 backdrop-blur-sm rounded-2xl p-4 border border-purple-500/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-300 text-sm">Connecteur</p>
                <p className="text-xl font-bold">
                  {connectorStatus === 'connected' ? '🟢 Connecté' : '🔴 Déconnecté'}
                </p>
              </div>
              <Activity className={`w-8 h-8 ${connectorStatus === 'connected' ? 'text-green-400' : 'text-red-400'}`} />
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 backdrop-blur-sm rounded-2xl p-4 border border-purple-500/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-300 text-sm">Bot Status</p>
                <p className="text-xl font-bold">
                  {botStatus === 'running' ? '✅ Actif' : '⏸️ Arrêté'}
                </p>
              </div>
              <TrendingUp className={`w-8 h-8 ${botStatus === 'running' ? 'text-green-400' : 'text-gray-400'}`} />
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 backdrop-blur-sm rounded-2xl p-4 border border-purple-500/30">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-300 text-sm">Signaux (24h)</p>
                <p className="text-xl font-bold">{signals.length}</p>
              </div>
              <List className="w-8 h-8 text-pink-400" />
            </div>
          </div>
        </div>

        {/* Alert si connecteur non connecté */}
        {connectorStatus === 'disconnected' && (
          <div className="bg-gradient-to-r from-yellow-500/10 to-orange-500/10 border border-yellow-500/30 rounded-2xl p-4 mb-6 backdrop-blur-sm">
            <div className="flex items-start">
              <AlertCircle className="w-6 h-6 text-yellow-400 mr-3 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="font-bold text-yellow-400 mb-2">Connecteur non détecté</p>
                <p className="text-white/80 text-sm mb-3">
                  Pour utiliser TRADABOT, vous devez installer le petit connecteur MT4 (2 MB).
                </p>
                <button 
                  onClick={downloadConnector}
                  className="bg-gradient-to-r from-yellow-500 to-orange-500 hover:from-yellow-600 hover:to-orange-600 text-white px-4 py-2 rounded-lg font-bold text-sm transition shadow-lg"
                >
                  📥 Télécharger le Connecteur
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Tabs */}
        <div className="flex space-x-2 mb-6 overflow-x-auto pb-2">
          {[
            { id: 'dashboard', label: '📊 Dashboard', icon: Activity },
            { id: 'config', label: '⚙️ Configuration', icon: Settings },
            { id: 'signals', label: '📡 Signaux', icon: List },
            { id: 'trades', label: '💰 Trades', icon: TrendingUp }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-4 py-2 rounded-lg font-semibold whitespace-nowrap transition ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-pink-500 via-purple-500 to-violet-600 text-white shadow-lg'
                  : 'bg-purple-900/20 text-purple-300 hover:bg-purple-900/40 border border-purple-500/20'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 backdrop-blur-sm rounded-3xl p-6 border border-purple-500/30 min-h-[500px]">
          
          {/* Dashboard Tab */}
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold mb-4">Tableau de bord</h2>
              
              {/* Contrôle du bot */}
              <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/30">
                <h3 className="text-xl font-bold mb-4">Contrôle du Bot</h3>
                <button
                  onClick={toggleBot}
                  disabled={connectorStatus === 'disconnected'}
                  className={`w-full py-4 rounded-xl font-bold text-lg transition flex items-center justify-center shadow-lg ${
                    botStatus === 'running'
                      ? 'bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700'
                      : 'bg-gradient-to-r from-pink-500 via-purple-500 to-violet-600 hover:from-pink-600 hover:via-purple-600 hover:to-violet-700 disabled:from-gray-600 disabled:to-gray-700 disabled:cursor-not-allowed'
                  }`}
                >
                  {botStatus === 'running' ? (
                    <>
                      <Square className="w-6 h-6 mr-2" />
                      ARRÊTER LE BOT
                    </>
                  ) : (
                    <>
                      <Play className="w-6 h-6 mr-2" />
                      DÉMARRER LE BOT
                    </>
                  )}
                </button>
                {connectorStatus === 'disconnected' && (
                  <p className="text-yellow-400 text-sm mt-2 text-center">
                    Installez d'abord le connecteur pour démarrer le bot
                  </p>
                )}
              </div>

              {/* Stats rapides */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div className="bg-gradient-to-br from-blue-900/20 to-purple-900/20 backdrop-blur-sm rounded-xl p-4 border border-blue-500/30 text-center">
                  <p className="text-blue-300 text-sm mb-1">Signaux reçus</p>
                  <p className="text-3xl font-bold text-blue-400">{signals.length}</p>
                </div>
                <div className="bg-gradient-to-br from-green-900/20 to-emerald-900/20 backdrop-blur-sm rounded-xl p-4 border border-green-500/30 text-center">
                  <p className="text-green-300 text-sm mb-1">Trades ouverts</p>
                  <p className="text-3xl font-bold text-green-400">{trades.filter(t => t.status === 'open').length}</p>
                </div>
                <div className="bg-gradient-to-br from-purple-900/20 to-pink-900/20 backdrop-blur-sm rounded-xl p-4 border border-purple-500/30 text-center">
                  <p className="text-purple-300 text-sm mb-1">Trades fermés</p>
                  <p className="text-3xl font-bold text-purple-400">{trades.filter(t => t.status === 'closed').length}</p>
                </div>
                <div className="bg-gradient-to-br from-pink-900/20 to-rose-900/20 backdrop-blur-sm rounded-xl p-4 border border-pink-500/30 text-center">
                  <p className="text-pink-300 text-sm mb-1">Profit total</p>
                  <p className="text-3xl font-bold text-pink-400">$0.00</p>
                </div>
              </div>
            </div>
          )}

          {/* Configuration Tab */}
          {activeTab === 'config' && (
            <div className="space-y-6">
              <h2 className="text-2xl font-bold mb-4">Configuration</h2>
              
              {/* MT4 Config */}
              <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/30">
                <h3 className="text-xl font-bold mb-4">🎯 Configuration MT4/MT5</h3>
                <div className="space-y-4">
                  <div>
                    <label className="block text-purple-300 text-sm mb-2">Login MT4</label>
                    <input
                      type="text"
                      value={config.mt4Login}
                      onChange={(e) => setConfig({...config, mt4Login: e.target.value})}
                      placeholder="Ex: 12345678"
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded-lg px-4 py-2 text-white placeholder-purple-400/50 focus:border-purple-400 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-2">Password MT4</label>
                    <input
                      type="password"
                      value={config.mt4Password}
                      onChange={(e) => setConfig({...config, mt4Password: e.target.value})}
                      placeholder="Votre mot de passe MT4"
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded-lg px-4 py-2 text-white placeholder-purple-400/50 focus:border-purple-400 focus:outline-none"
                    />
                  </div>
                  <div>
                    <label className="block text-purple-300 text-sm mb-2">Serveur</label>
                    <input
                      type="text"
                      value={config.mt4Server}
                      onChange={(e) => setConfig({...config, mt4Server: e.target.value})}
                      placeholder="Ex: XM.COM-Real"
                      className="w-full bg-purple-900/20 border border-purple-500/30 rounded-lg px-4 py-2 text-white placeholder-purple-400/50 focus:border-purple-400 focus:outline-none"
                    />
                  </div>
                </div>
              </div>

              {/* Canaux */}
              <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/30">
                <h3 className="text-xl font-bold mb-4">📡 Canaux Telegram</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {Object.keys(config.channels).map(channel => (
                    <label key={channel} className="flex items-center space-x-3 cursor-pointer hover:bg-purple-500/10 p-2 rounded-lg transition">
                      <input
                        type="checkbox"
                        checked={config.channels[channel]}
                        onChange={(e) => setConfig({
                          ...config,
                          channels: {...config.channels, [channel]: e.target.checked}
                        })}
                        className="w-5 h-5 text-purple-500 bg-purple-900/20 border-purple-500/30 rounded focus:ring-purple-500"
                      />
                      <span className="capitalize text-purple-200">{channel}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* Lots */}
              <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/30">
                <h3 className="text-xl font-bold mb-4">💰 Configuration des Lots</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {Object.keys(config.lots).map(category => (
                    <div key={category}>
                      <label className="block text-purple-300 text-sm mb-2 capitalize">{category}</label>
                      <input
                        type="number"
                        step="0.01"
                        value={config.lots[category]}
                        onChange={(e) => setConfig({
                          ...config,
                          lots: {...config.lots, [category]: parseFloat(e.target.value)}
                        })}
                        className="w-full bg-purple-900/20 border border-purple-500/30 rounded-lg px-4 py-2 text-white focus:border-purple-400 focus:outline-none"
                      />
                    </div>
                  ))}
                </div>
              </div>

              {/* Breakeven */}
              <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-2xl p-6 border border-purple-500/30">
                <label className="flex items-center space-x-3 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={config.breakevenEnabled}
                    onChange={(e) => setConfig({...config, breakevenEnabled: e.target.checked})}
                    className="w-5 h-5 text-purple-500 bg-purple-900/20 border-purple-500/30 rounded focus:ring-purple-500"
                  />
                  <span className="text-lg">🔒 Activer le Breakeven automatique</span>
                </label>
              </div>

              <button
                onClick={saveConfig}
                className="w-full bg-gradient-to-r from-pink-500 via-purple-500 to-violet-600 hover:from-pink-600 hover:via-purple-600 hover:to-violet-700 py-3 rounded-xl font-bold transition shadow-lg"
              >
                💾 Sauvegarder la Configuration
              </button>
            </div>
          )}

          {/* Signals Tab */}
          {activeTab === 'signals' && (
            <div>
              <h2 className="text-2xl font-bold mb-4">📡 Signaux Reçus</h2>
              {signals.length === 0 ? (
                <p className="text-purple-300 text-center py-8">Aucun signal reçu pour le moment</p>
              ) : (
                <div className="space-y-3">
                  {signals.map((signal, index) => (
                    <div key={index} className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-xl p-4 border border-purple-500/30 hover:border-purple-400/50 transition">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-bold text-lg">
                            {signal.type === 'BUY' ? '🟢' : '🔴'} {signal.type} {signal.symbol}
                          </p>
                          <p className="text-purple-300 text-sm">
                            Entry: {signal.entry} | SL: {signal.sl} | TP: {signal.tp1}
                          </p>
                        </div>
                        <span className="text-purple-400 text-sm">{signal.timestamp}</span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Trades Tab */}
          {activeTab === 'trades' && (
            <div>
              <h2 className="text-2xl font-bold mb-4">💰 Historique des Trades</h2>
              {trades.length === 0 ? (
                <p className="text-purple-300 text-center py-8">Aucun trade pour le moment</p>
              ) : (
                <div className="space-y-3">
                  {trades.map((trade, index) => (
                    <div key={index} className="bg-gradient-to-r from-purple-900/30 to-pink-900/30 backdrop-blur-sm rounded-xl p-4 border border-purple-500/30 hover:border-purple-400/50 transition">
                      <div className="flex items-start justify-between">
                        <div>
                          <p className="font-bold text-lg">
                            {trade.type === 'BUY' ? '🟢' : '🔴'} {trade.type} {trade.symbol}
                          </p>
                          <p className="text-purple-300 text-sm">
                            Lot: {trade.lot} | Entry: {trade.entry} | Status: {trade.status}
                          </p>
                        </div>
                        <span className={`font-bold ${trade.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                          {trade.profit >= 0 ? '+' : ''}{trade.profit} $
                        </span>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default TradabotWeb;
