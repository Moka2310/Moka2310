import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'https://mt4-dropdown.preview.emergentagent.com';

const TradabotDemo = () => {
  const navigate = useNavigate();
  const { user, token } = useAuth();
  const [activeTab, setActiveTab] = useState('dashboard');
  const [botRunning, setBotRunning] = useState(false);
  const [signals, setSignals] = useState([]);
  const [positions, setPositions] = useState([]);
  const [logs, setLogs] = useState(['[SYSTÈME] TRADABOT initialisé - Mode Démo']);
  const [account, setAccount] = useState({
    balance: 10000,
    equity: 10000,
    profit: 0
  });

  const [config, setConfig] = useState({
    channelForexEnabled: true,
    channelCryptoEnabled: true,
    channelGoldEnabled: true,
    channelIndicesEnabled: true,
    channelActionsEnabled: true,
    channelCommoditesEnabled: true,
    lotForex: 0.01,
    lotCrypto: 0.01,
    lotGold: 0.01
  });

  const [mt4Config, setMt4Config] = useState({
    login: '',
    password: '',
    server: '',
    platform: 'MT4'
  });

  const [mt4Connected, setMt4Connected] = useState(false);

  useEffect(() => {
    if (!user) {
      navigate('/login');
    } else {
      addLog('✅ Connecté avec: ' + user.email);
      checkAccess();
      loadLiveSignals(); // Charger les vrais signaux
      
      // Rafraîchir les signaux toutes les 5 secondes
      const interval = setInterval(loadLiveSignals, 5000);
      return () => clearInterval(interval);
    }
  }, [user, navigate]);

  const loadLiveSignals = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/tradabot/signals/live?limit=20`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        if (data.signals && data.signals.length > 0) {
          // Mettre à jour seulement s'il y a de nouveaux signaux
          setSignals(data.signals);
        }
      }
    } catch (error) {
      // Erreur silencieuse pour ne pas spammer les logs
    }
  };

  const checkAccess = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/tradabot/access`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      const data = await response.json();
      if (data.hasAccess) {
        addLog('✅ Accès TRADABOT vérifié');
        loadConfig();
      } else {
        addLog('❌ Pas d\'accès TRADABOT');
        alert('Vous n\'avez pas accès à TRADABOT');
        navigate('/');
      }
    } catch (error) {
      addLog('❌ Erreur vérification accès: ' + error.message);
    }
  };

  const loadConfig = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/tradabot/config`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      if (response.ok) {
        const data = await response.json();
        setConfig(data);
        addLog('✅ Configuration chargée');
      }
    } catch (error) {
      addLog('⚠️ Configuration par défaut utilisée');
    }
  };

  const saveConfig = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/tradabot/config`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(config)
      });
      if (response.ok) {
        addLog('✅ Configuration sauvegardée');
        alert('Configuration sauvegardée!');
      }
    } catch (error) {
      addLog('❌ Erreur sauvegarde: ' + error.message);
    }
  };

  const addLog = (message) => {
    const time = new Date().toLocaleTimeString();
    setLogs(prev => [...prev, `[${time}] ${message}`]);
  };

  const startBot = async () => {
    if (!mt4Connected) {
      alert('⚠️ Connectez d\'abord votre compte MT4/MT5!');
      setActiveTab('config');
      return;
    }

    try {
      const response = await fetch(`${BACKEND_URL}/api/tradabot/bot/start`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      if (response.ok) {
        setBotRunning(true);
        addLog('🚀 Bot démarré - Surveillance RÉELLE des canaux Telegram');
        addLog('📡 En attente des signaux...');
      } else {
        const error = await response.json();
        addLog('❌ Erreur démarrage: ' + error.detail);
        alert('Erreur: ' + error.detail);
      }
    } catch (error) {
      addLog('❌ Erreur: ' + error.message);
      alert('Erreur: ' + error.message);
    }
  };

  const stopBot = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/tradabot/bot/stop`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (response.ok) {
        setBotRunning(false);
        addLog('⏹️ Bot arrêté');
      }
    } catch (error) {
      addLog('❌ Erreur: ' + error.message);
    }
  };

  const connectMT4 = async () => {
    if (!mt4Config.login || !mt4Config.server) {
      alert('⚠️ Veuillez remplir le Login et le Serveur');
      return;
    }

    addLog('🔄 Connexion à MT4...');
    addLog(`   Login: ${mt4Config.login}`);
    addLog(`   Server: ${mt4Config.server}`);
    addLog(`   Platform: ${mt4Config.platform}`);

    try {
      const response = await fetch(`${BACKEND_URL}/api/tradabot/mt4/connect`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          login: parseInt(mt4Config.login),
          password: mt4Config.password,
          server: mt4Config.server,
          platform: mt4Config.platform
        })
      });

      const data = await response.json();

      if (response.ok) {
        setMt4Connected(true);
        addLog('✅ Configuration MT4 sauvegardée avec succès!');
        addLog('ℹ️ ' + (data.note || ''));
        alert('✅ Configuration MT4 sauvegardée!\n\n' + 
              'Vous pouvez maintenant démarrer le bot.\n\n' +
              'Note: L\'exécution automatique des trades nécessite\n' +
              'l\'application desktop Windows avec MT4/MT5 installé.');
      } else {
        addLog('❌ Erreur: ' + data.detail);
        alert('❌ Erreur de connexion:\n\n' + data.detail);
      }
    } catch (error) {
      addLog('❌ Erreur réseau: ' + error.message);
      alert('❌ Erreur de connexion:\n\n' + error.message + '\n\nVérifiez votre connexion internet.');
    }
  };

  const addDemoSignal = (type, symbol, entry, sl, tp) => {
    const signal = {
      id: Date.now(),
      type,
      symbol,
      entry,
      sl,
      tp,
      time: new Date().toLocaleTimeString(),
      channel: 'Demo'
    };
    setSignals(prev => [signal, ...prev]);
    addLog(`📡 Signal reçu: ${type} ${symbol} @ ${entry}`);
    
    // Exécuter le trade après 1 seconde
    setTimeout(() => executeTrade(signal), 1000);
  };

  const executeTrade = (signal) => {
    const ticket = Math.floor(Math.random() * 1000000);
    const position = {
      ticket,
      symbol: signal.symbol,
      type: signal.type,
      entry: signal.entry,
      sl: signal.sl,
      tp: signal.tp,
      lot: config.lotForex,
      profit: 0,
      time: new Date().toLocaleTimeString()
    };
    setPositions(prev => [position, ...prev]);
    addLog(`✅ Trade exécuté: ${signal.type} ${signal.symbol} | Ticket: ${ticket}`);
  };

  if (!user) {
    return <div className="min-h-screen bg-[#1E1540] flex items-center justify-center">
      <p className="text-white">Chargement...</p>
    </div>;
  }

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8 bg-gradient-to-r from-blue-600/20 to-purple-600/20 rounded-3xl p-8 border border-blue-500/30">
          <h1 className="text-5xl font-bold mb-2">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-400">
              🤖 TRADABOT
            </span>
            <span className="ml-4 text-sm bg-gradient-to-r from-orange-500 to-red-500 px-4 py-1 rounded-full">
              MODE DÉMO
            </span>
          </h1>
          <p className="text-white/80">Version Web - Trading Automatisé</p>
        </div>

        {/* Status Bar */}
        <div className="bg-white/5 rounded-2xl p-6 mb-6 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className={`w-3 h-3 rounded-full ${botRunning ? 'bg-green-500 animate-pulse' : 'bg-gray-500'}`}></div>
            <span className="text-white">{botRunning ? '🟢 Bot Actif' : '⚫ Bot Arrêté'}</span>
          </div>
          <div className="text-white/80">
            👤 {user.email}
          </div>
        </div>

        {/* Tabs */}
        <div className="flex gap-2 mb-6 overflow-x-auto pb-2">
          {[
            { id: 'dashboard', icon: '📊', label: 'Dashboard' },
            { id: 'config', icon: '⚙️', label: 'Configuration' },
            { id: 'signals', icon: '📡', label: 'Signaux' },
            { id: 'positions', icon: '💼', label: 'Positions' },
            { id: 'logs', icon: '📋', label: 'Logs' }
          ].map(tab => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`px-6 py-3 rounded-xl font-semibold transition-all whitespace-nowrap ${
                activeTab === tab.id
                  ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                  : 'bg-white/5 text-white/70 hover:bg-white/10'
              }`}
            >
              {tab.icon} {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Content */}
        <div className="space-y-6">
          {/* Dashboard */}
          {activeTab === 'dashboard' && (
            <div className="space-y-6">
              <div className="bg-blue-500/20 border border-blue-500/30 rounded-2xl p-6">
                <p className="text-white">ℹ️ <strong>MODE RÉEL</strong> - Connectez votre compte MT4/MT5 démo GlobalPrime dans Configuration</p>
                <p className="text-white/70 text-sm mt-2">Les signaux Telegram sont reçus en temps réel des 6 canaux VIP</p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="bg-white/5 rounded-2xl p-6 text-center">
                  <p className="text-white/60 text-sm mb-2">Balance</p>
                  <p className="text-4xl font-bold text-green-400">${account.balance.toFixed(2)}</p>
                </div>
                <div className="bg-white/5 rounded-2xl p-6 text-center">
                  <p className="text-white/60 text-sm mb-2">Équité</p>
                  <p className="text-4xl font-bold text-blue-400">${account.equity.toFixed(2)}</p>
                </div>
                <div className="bg-white/5 rounded-2xl p-6 text-center">
                  <p className="text-white/60 text-sm mb-2">Profit</p>
                  <p className={`text-4xl font-bold ${account.profit >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                    ${account.profit.toFixed(2)}
                  </p>
                </div>
              </div>

              <div className="bg-white/5 rounded-2xl p-6">
                <h3 className="text-white text-xl font-bold mb-4">Contrôles</h3>
                {!botRunning ? (
                  <button
                    onClick={startBot}
                    className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-8 py-4 rounded-xl font-bold text-lg transition-all"
                  >
                    ▶️ DÉMARRER LE BOT
                  </button>
                ) : (
                  <button
                    onClick={stopBot}
                    className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-8 py-4 rounded-xl font-bold text-lg transition-all"
                  >
                    ⏹️ ARRÊTER LE BOT
                  </button>
                )}
              </div>
            </div>
          )}

          {/* Configuration */}
          {activeTab === 'config' && (
            <div className="space-y-6">
              {/* MT4/MT5 Configuration */}
              <div className="bg-white/5 rounded-2xl p-6">
                <h3 className="text-white text-xl font-bold mb-6">
                  🎯 Connexion MT4/MT5 {mt4Connected && <span className="text-green-400 text-sm ml-2">✅ Connecté</span>}
                </h3>
                
                {/* Aide pour trouver les infos */}
                <div className="bg-blue-500/20 border border-blue-500/30 rounded-lg p-4 mb-6">
                  <p className="text-white/90 text-sm mb-2">
                    <strong>💡 Comment trouver tes informations MT4?</strong>
                  </p>
                  <ol className="text-white/70 text-sm space-y-1 ml-4">
                    <li>1️⃣ Ouvre MetaTrader 4 ou 5</li>
                    <li>2️⃣ Menu → <strong>Outils → Options → Serveur</strong></li>
                    <li>3️⃣ Tu verras ton <strong>Login</strong> et le nom du <strong>Serveur</strong></li>
                    <li>4️⃣ Sélectionne le serveur dans la liste ci-dessous</li>
                  </ol>
                </div>
                
                <div className="space-y-4">
                  <div>
                    <label className="text-white/70 text-sm mb-2 block">Login (numéro de compte)</label>
                    <input
                      type="number"
                      value={mt4Config.login}
                      onChange={(e) => setMt4Config({...mt4Config, login: e.target.value})}
                      placeholder="123456"
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="text-white/70 text-sm mb-2 block">Mot de passe</label>
                    <input
                      type="password"
                      value={mt4Config.password}
                      onChange={(e) => setMt4Config({...mt4Config, password: e.target.value})}
                      placeholder="••••••••"
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="text-white/70 text-sm mb-2 block">Serveur</label>
                    <select
                      value={mt4Config.server}
                      onChange={(e) => setMt4Config({...mt4Config, server: e.target.value})}
                      className="w-full border border-white/20 rounded-lg px-4 py-2 text-white"
                      style={{
                        backgroundColor: '#5B21B6',
                        color: 'white',
                        fontWeight: '500'
                      }}
                    >
                      <option value="" style={{backgroundColor: '#5B21B6', color: 'white'}}>-- Sélectionner un serveur --</option>
                      
                      <optgroup label="🌟 GlobalPrime (Recommandé)" style={{backgroundColor: '#4C1D95', color: 'white'}}>
                        <option value="GlobalPrime-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>GlobalPrime-Demo (Compte Démo)</option>
                        <option value="GlobalPrime-Live" style={{backgroundColor: '#5B21B6', color: 'white'}}>GlobalPrime-Live (Compte Réel)</option>
                        <option value="GlobalPrime-Live2" style={{backgroundColor: '#5B21B6', color: 'white'}}>GlobalPrime-Live2</option>
                        <option value="GlobalPrime-Live3" style={{backgroundColor: '#5B21B6', color: 'white'}}>GlobalPrime-Live3</option>
                        <option value="GlobalPrimeForex-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>GlobalPrimeForex-Demo</option>
                        <option value="GlobalPrimeForex-Live" style={{backgroundColor: '#5B21B6', color: 'white'}}>GlobalPrimeForex-Live</option>
                      </optgroup>
                      
                      <optgroup label="🏦 Autres Brokers Populaires" style={{backgroundColor: '#4C1D95', color: 'white'}}>
                        <option value="ICMarkets-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>ICMarkets-Demo</option>
                        <option value="ICMarkets-Live" style={{backgroundColor: '#5B21B6', color: 'white'}}>ICMarkets-Live</option>
                        <option value="XM-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>XM-Demo</option>
                        <option value="XM-Real" style={{backgroundColor: '#5B21B6', color: 'white'}}>XM-Real</option>
                        <option value="Pepperstone-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>Pepperstone-Demo</option>
                        <option value="Pepperstone-Live" style={{backgroundColor: '#5B21B6', color: 'white'}}>Pepperstone-Live</option>
                        <option value="FXTM-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>FXTM-Demo</option>
                        <option value="FXTM-Real" style={{backgroundColor: '#5B21B6', color: 'white'}}>FXTM-Real</option>
                        <option value="FBS-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>FBS-Demo</option>
                        <option value="FBS-Real" style={{backgroundColor: '#5B21B6', color: 'white'}}>FBS-Real</option>
                        <option value="Exness-Demo" style={{backgroundColor: '#5B21B6', color: 'white'}}>Exness-Demo</option>
                        <option value="Exness-Real" style={{backgroundColor: '#5B21B6', color: 'white'}}>Exness-Real</option>
                      </optgroup>
                      
                      <optgroup label="✏️ Autre" style={{backgroundColor: '#4C1D95', color: 'white'}}>
                        <option value="custom" style={{backgroundColor: '#5B21B6', color: 'white'}}>Autre serveur (je vais le taper)</option>
                      </optgroup>
                    </select>
                    
                    {mt4Config.server === 'custom' && (
                      <input
                        type="text"
                        placeholder="Nom exact du serveur"
                        onChange={(e) => setMt4Config({...mt4Config, server: e.target.value, customServer: true})}
                        className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white mt-2"
                      />
                    )}
                  </div>
                  <div>
                    <label className="text-white/70 text-sm mb-2 block">Plateforme</label>
                    <select
                      value={mt4Config.platform}
                      onChange={(e) => setMt4Config({...mt4Config, platform: e.target.value})}
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                    >
                      <option value="MT4">MetaTrader 4</option>
                      <option value="MT5">MetaTrader 5</option>
                    </select>
                  </div>
                  <button
                    onClick={connectMT4}
                    className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white px-6 py-3 rounded-xl font-bold transition-all"
                  >
                    {mt4Connected ? '🔄 Mettre à jour MT4' : '🔗 Connecter MT4'}
                  </button>
                </div>
              </div>

              <div className="bg-white/5 rounded-2xl p-6">
                <h3 className="text-white text-xl font-bold mb-6">📡 Canaux Telegram</h3>
                <div className="space-y-4">
                  {[
                    { key: 'channelForexEnabled', label: '📊 Forex', id: -1002425540174 },
                    { key: 'channelCryptoEnabled', label: '💰 Crypto', id: -1002279973041 },
                    { key: 'channelGoldEnabled', label: '🥇 Gold', id: -1002355600472 },
                    { key: 'channelIndicesEnabled', label: '📈 Indices', id: -1002339785500 },
                    { key: 'channelActionsEnabled', label: '📊 Actions', id: -1002376632406 },
                    { key: 'channelCommoditesEnabled', label: '🛢️ Commodités', id: -1002368060694 }
                  ].map(channel => (
                    <div key={channel.key} className="flex items-center justify-between bg-white/5 p-4 rounded-xl">
                      <span className="text-white">{channel.label} <span className="text-white/40 text-sm">({channel.id})</span></span>
                      <label className="relative inline-flex items-center cursor-pointer">
                        <input
                          type="checkbox"
                          checked={config[channel.key]}
                          onChange={(e) => setConfig({...config, [channel.key]: e.target.checked})}
                          className="sr-only peer"
                        />
                        <div className="w-14 h-7 bg-gray-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[4px] after:bg-white after:rounded-full after:h-6 after:w-6 after:transition-all peer-checked:bg-green-500"></div>
                      </label>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-white/5 rounded-2xl p-6">
                <h3 className="text-white text-xl font-bold mb-6">💰 Configuration des Lots</h3>
                <div className="space-y-4">
                  <div>
                    <label className="text-white/70 text-sm mb-2 block">Forex (lot)</label>
                    <input
                      type="number"
                      value={config.lotForex}
                      onChange={(e) => setConfig({...config, lotForex: parseFloat(e.target.value)})}
                      step="0.01"
                      min="0.01"
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="text-white/70 text-sm mb-2 block">Crypto (lot)</label>
                    <input
                      type="number"
                      value={config.lotCrypto}
                      onChange={(e) => setConfig({...config, lotCrypto: parseFloat(e.target.value)})}
                      step="0.01"
                      min="0.01"
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                    />
                  </div>
                  <div>
                    <label className="text-white/70 text-sm mb-2 block">Gold (lot)</label>
                    <input
                      type="number"
                      value={config.lotGold}
                      onChange={(e) => setConfig({...config, lotGold: parseFloat(e.target.value)})}
                      step="0.01"
                      min="0.01"
                      className="w-full bg-white/10 border border-white/20 rounded-lg px-4 py-2 text-white"
                    />
                  </div>
                </div>
                <button
                  onClick={saveConfig}
                  className="mt-6 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-6 py-3 rounded-xl font-bold transition-all"
                >
                  💾 Sauvegarder Configuration
                </button>
              </div>
            </div>
          )}

          {/* Signaux */}
          {activeTab === 'signals' && (
            <div className="space-y-6">
              {/* Info sur le format */}
              <div className="bg-blue-500/20 border border-blue-500/30 rounded-2xl p-6">
                <h4 className="text-white font-bold mb-3">📋 Format des Signaux Telegram Détectés</h4>
                <div className="text-white/80 text-sm space-y-2">
                  <p><strong>Le bot détecte automatiquement:</strong></p>
                  <ul className="list-disc list-inside space-y-1 text-white/70">
                    <li>BUY/SELL (ou ACHAT/VENTE)</li>
                    <li>Symbole: EURUSD, XAUUSD, BTCUSD, US30, etc.</li>
                    <li>Prix d'entrée: @ ou ENTRY</li>
                    <li>Stop Loss: SL</li>
                    <li>Take Profit: TP, TP1, TP2, TP3</li>
                    <li>Breakeven: BREAKEVEN ou BE</li>
                  </ul>
                  <p className="text-green-400 mt-3">✅ <strong>Les émojis sont automatiquement ignorés!</strong></p>
                  <p className="text-white/60 text-xs">Exemple: 🔥 BUY EURUSD @ 1.0850 ⚡ TP: 1.0900 🎯 SL: 1.0820</p>
                </div>
              </div>

              <div className="bg-white/5 rounded-2xl p-6">
                <h3 className="text-white text-xl font-bold mb-6">📡 Signaux Reçus (Temps Réel)</h3>
                <div className="space-y-4 max-h-96 overflow-y-auto">
                {signals.length === 0 ? (
                  <p className="text-white/40 text-center py-8">En attente de signaux des canaux Telegram...</p>
                ) : (
                  signals.map((signal, index) => (
                    <div
                      key={signal.id || index}
                      className={`p-4 rounded-xl border-l-4 ${
                        signal.type === 'BUY' ? 'bg-green-500/10 border-green-500' : 'bg-red-500/10 border-red-500'
                      }`}
                    >
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-white font-bold">{signal.type} {signal.symbol}</span>
                        <div className="text-right">
                          <div className="text-white/60 text-sm">{new Date(signal.timestamp || signal.createdAt).toLocaleTimeString()}</div>
                          <div className="text-white/40 text-xs">{signal.channel}</div>
                        </div>
                      </div>
                      <div className="text-white/80 text-sm">
                        {signal.entryPrice && `Entry: ${signal.entryPrice} | `}
                        {signal.stopLoss && `SL: ${signal.stopLoss} | `}
                        {signal.takeProfit1 && `TP: ${signal.takeProfit1}`}
                        {signal.breakeven && <span className="ml-2 text-yellow-400">⚡ BREAKEVEN</span>}
                      </div>
                    </div>
                  ))
                )}
                </div>
              </div>
            </div>
          )}

          {/* Positions */}
          {activeTab === 'positions' && (
            <div className="bg-white/5 rounded-2xl p-6">
              <h3 className="text-white text-xl font-bold mb-6">💼 Positions Ouvertes (Simulation)</h3>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {positions.length === 0 ? (
                  <p className="text-white/40 text-center py-8">Aucune position ouverte</p>
                ) : (
                  positions.map(pos => (
                    <div key={pos.ticket} className="bg-white/5 p-4 rounded-xl border-l-4 border-green-500">
                      <div className="flex justify-between items-start mb-2">
                        <span className="text-white font-bold">#{pos.ticket} - {pos.type} {pos.symbol}</span>
                        <span className="text-green-400 font-bold">+{pos.profit.toFixed(2)} $</span>
                      </div>
                      <div className="text-white/60 text-sm">
                        Lot: {pos.lot} | Entry: {pos.entry} | SL: {pos.sl} | TP: {pos.tp}
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* Logs */}
          {activeTab === 'logs' && (
            <div className="bg-black rounded-2xl p-6">
              <h3 className="text-white text-xl font-bold mb-6">📋 Logs d'Activité</h3>
              <div className="font-mono text-sm text-green-400 space-y-1 max-h-96 overflow-y-auto">
                {logs.map((log, index) => (
                  <div key={index}>{log}</div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TradabotDemo;
