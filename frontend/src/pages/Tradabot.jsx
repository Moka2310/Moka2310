import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { 
  Bot, 
  Settings, 
  TrendingUp, 
  Activity,
  Lock,
  CheckCircle,
  XCircle,
  AlertCircle,
  Save,
  Eye,
  EyeOff
} from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Tradabot = () => {
  const navigate = useNavigate();
  const { user } = useAuth();
  const { language } = useLanguage();
  
  const [hasAccess, setHasAccess] = useState(false);
  const [loading, setLoading] = useState(true);
  const [config, setConfig] = useState(null);
  const [showPassword, setShowPassword] = useState(false);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    window.scrollTo(0, 0);
    checkAccess();
  }, []);

  const checkAccess = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      if (!token) {
        navigate('/login');
        return;
      }

      const response = await axios.get(`${API}/tradabot/access`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });

      if (response.data.hasAccess) {
        setHasAccess(true);
        loadConfig();
      } else {
        setHasAccess(false);
        setLoading(false);
      }
    } catch (error) {
      console.error('Error checking access:', error);
      setHasAccess(false);
      setLoading(false);
    }
  };

  const loadConfig = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      const response = await axios.get(`${API}/tradabot/config`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      
      setConfig(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error loading config:', error);
      setLoading(false);
    }
  };

  const handleSaveConfig = async () => {
    try {
      setSaving(true);
      const token = localStorage.getItem('tradalife_token');
      
      await axios.post(`${API}/tradabot/config`, config, {
        headers: { 
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });

      alert(language === 'fr' ? '✅ Configuration sauvegardée!' : '✅ Configuration saved!');
      setSaving(false);
    } catch (error) {
      console.error('Error saving config:', error);
      alert(language === 'fr' ? '❌ Erreur lors de la sauvegarde' : '❌ Error saving configuration');
      setSaving(false);
    }
  };

  const updateConfig = (field, value) => {
    setConfig(prev => ({ ...prev, [field]: value }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4 flex items-center justify-center">
        <div className="text-white text-xl">
          {language === 'fr' ? 'Chargement...' : 'Loading...'}
        </div>
      </div>
    );
  }

  if (!hasAccess) {
    return (
      <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4">
        <div className="max-w-4xl mx-auto">
          {/* No Access Message */}
          <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-3xl p-8 border border-purple-500/30 text-center">
            <Lock className="w-20 h-20 text-pink-400 mx-auto mb-6" />
            <h1 className="text-3xl font-bold text-white mb-4">
              {language === 'fr' ? 'Accès TRADABOT Réservé' : 'TRADABOT Access Reserved'}
            </h1>
            <p className="text-white/80 text-lg mb-8">
              {language === 'fr' 
                ? 'Vous devez acheter TRADABOT pour accéder à cette fonctionnalité.'
                : 'You need to purchase TRADABOT to access this feature.'}
            </p>
            <Button
              onClick={() => navigate('/bot-preorder')}
              className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-6 text-lg rounded-full"
            >
              {language === 'fr' ? '🤖 Acheter TRADABOT - 300$ CAD' : '🤖 Buy TRADABOT - 300$ CAD'}
            </Button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-4 mb-4">
            <Bot className="w-16 h-16 text-pink-400" />
            <h1 className="text-4xl md:text-5xl font-bold">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                TRADABOT
              </span>
            </h1>
          </div>
          <p className="text-white/80 text-lg">
            {language === 'fr' 
              ? 'Configuration de votre bot de copie trading MT4'
              : 'Configure your MT4 copy trading bot'}
          </p>
        </div>

        {/* Configuration Form */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* MT4 Connection */}
          <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-3xl p-6 border border-purple-500/30">
            <div className="flex items-center gap-3 mb-6">
              <Settings className="w-6 h-6 text-pink-400" />
              <h2 className="text-2xl font-bold text-white">
                {language === 'fr' ? 'Connexion MT4' : 'MT4 Connection'}
              </h2>
            </div>

            <div className="space-y-4">
              <div>
                <label className="text-white/80 text-sm mb-2 block">
                  {language === 'fr' ? 'Login MT4' : 'MT4 Login'}
                </label>
                <Input
                  type="text"
                  value={config?.mt4Login || ''}
                  onChange={(e) => updateConfig('mt4Login', e.target.value)}
                  placeholder="12345678"
                  className="bg-white/10 border-white/20 text-white"
                />
              </div>

              <div>
                <label className="text-white/80 text-sm mb-2 block">
                  {language === 'fr' ? 'Serveur' : 'Server'}
                </label>
                <Input
                  type="text"
                  value={config?.mt4Server || ''}
                  onChange={(e) => updateConfig('mt4Server', e.target.value)}
                  placeholder="GlobalPrime-Demo / FusionMarkets-Demo"
                  className="bg-white/10 border-white/20 text-white"
                />
              </div>

              <div>
                <label className="text-white/80 text-sm mb-2 block">
                  {language === 'fr' ? 'Mot de passe' : 'Password'}
                </label>
                <div className="relative">
                  <Input
                    type={showPassword ? 'text' : 'password'}
                    value={config?.mt4Password || ''}
                    onChange={(e) => updateConfig('mt4Password', e.target.value)}
                    placeholder="••••••••"
                    className="bg-white/10 border-white/20 text-white pr-12"
                  />
                  <button
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-1/2 -translate-y-1/2 text-white/60 hover:text-white"
                  >
                    {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
                  </button>
                </div>
              </div>
            </div>
          </div>

          {/* Lot Configuration */}
          <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-3xl p-6 border border-purple-500/30">
            <div className="flex items-center gap-3 mb-6">
              <TrendingUp className="w-6 h-6 text-pink-400" />
              <h2 className="text-2xl font-bold text-white">
                {language === 'fr' ? 'Taille des Lots' : 'Lot Sizes'}
              </h2>
            </div>

            <div className="space-y-3">
              {[
                { key: 'lotForex', label: 'Forex' },
                { key: 'lotCrypto', label: 'Crypto' },
                { key: 'lotGold', label: 'Gold' },
                { key: 'lotIndices', label: 'Indices' },
                { key: 'lotActions', label: language === 'fr' ? 'Actions' : 'Stocks' },
                { key: 'lotCommodites', label: language === 'fr' ? 'Commodités' : 'Commodities' }
              ].map(({ key, label }) => (
                <div key={key} className="flex items-center justify-between">
                  <label className="text-white/80 text-sm">{label}</label>
                  <Input
                    type="number"
                    step="0.01"
                    min="0.01"
                    value={config?.[key] || 0.01}
                    onChange={(e) => updateConfig(key, parseFloat(e.target.value))}
                    className="bg-white/10 border-white/20 text-white w-24 text-center"
                  />
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Channel Selection */}
        <div className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-3xl p-6 border border-purple-500/30 mb-8">
          <div className="flex items-center gap-3 mb-6">
            <Activity className="w-6 h-6 text-pink-400" />
            <h2 className="text-2xl font-bold text-white">
              {language === 'fr' ? 'Canaux Telegram à Surveiller' : 'Telegram Channels to Monitor'}
            </h2>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {[
              { key: 'channelForexEnabled', label: 'Forex' },
              { key: 'channelCryptoEnabled', label: 'Crypto' },
              { key: 'channelGoldEnabled', label: 'Gold' },
              { key: 'channelIndicesEnabled', label: 'Indices' },
              { key: 'channelActionsEnabled', label: language === 'fr' ? 'Actions' : 'Stocks' },
              { key: 'channelCommoditesEnabled', label: language === 'fr' ? 'Commodités' : 'Commodities' }
            ].map(({ key, label }) => (
              <label key={key} className="flex items-center gap-3 p-4 bg-white/5 rounded-xl cursor-pointer hover:bg-white/10 transition-colors">
                <input
                  type="checkbox"
                  checked={config?.[key] || false}
                  onChange={(e) => updateConfig(key, e.target.checked)}
                  className="w-5 h-5 rounded"
                />
                <span className="text-white font-medium">{label}</span>
                {config?.[key] && <CheckCircle className="w-5 h-5 text-green-400 ml-auto" />}
              </label>
            ))}
          </div>
        </div>

        {/* Save Button */}
        <div className="flex justify-center">
          <Button
            onClick={handleSaveConfig}
            disabled={saving}
            className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-12 py-6 text-lg rounded-full flex items-center gap-3"
          >
            <Save className="w-5 h-5" />
            {saving 
              ? (language === 'fr' ? 'Sauvegarde...' : 'Saving...') 
              : (language === 'fr' ? 'Sauvegarder la Configuration' : 'Save Configuration')}
          </Button>
        </div>

        {/* Info Box */}
        <div className="mt-8 bg-blue-500/10 border border-blue-500/30 rounded-2xl p-6">
          <div className="flex items-start gap-3">
            <AlertCircle className="w-6 h-6 text-blue-400 flex-shrink-0 mt-1" />
            <div className="text-white/80 text-sm">
              <p className="font-bold text-white mb-2">
                {language === 'fr' ? 'ℹ️ Information Importante' : 'ℹ️ Important Information'}
              </p>
              <p>
                {language === 'fr' 
                  ? 'Le bot TRADABOT copiera automatiquement les signaux de trading des canaux Telegram sélectionnés vers votre compte MT4. Assurez-vous que vos identifiants sont corrects avant de sauvegarder.'
                  : 'TRADABOT will automatically copy trading signals from selected Telegram channels to your MT4 account. Make sure your credentials are correct before saving.'}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Tradabot;
