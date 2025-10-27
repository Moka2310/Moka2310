import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Copy, Check, Gift, Users } from 'lucide-react';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const Referral = () => {
  const navigate = useNavigate();
  const [referralData, setReferralData] = useState(null);
  const [referrals, setReferrals] = useState([]);
  const [copied, setCopied] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    window.scrollTo(0, 0);
    loadReferralData();
  }, []);

  const loadReferralData = async () => {
    try {
      const token = localStorage.getItem('tradalife_token');
      if (!token) {
        navigate('/login');
        return;
      }

      // Charger le code de parrainage
      const codeResponse = await axios.get(`${BACKEND_URL}/api/referrals/my-code`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReferralData(codeResponse.data);

      // Charger la liste des parrainages
      const referralsResponse = await axios.get(`${BACKEND_URL}/api/referrals/my-referrals`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setReferrals(referralsResponse.data);

    } catch (error) {
      console.error('Error loading referral data:', error);
      if (error.response?.status === 401) {
        navigate('/login');
      }
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = () => {
    if (referralData?.referralLink) {
      navigator.clipboard.writeText(referralData.referralLink);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#0A0118] via-[#1a0b2e] to-[#16213E] pt-32 px-4 flex items-center justify-center">
        <div className="text-white text-xl">Chargement...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0A0118] via-[#1a0b2e] to-[#16213E] pt-32 px-4 pb-20">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Gift className="w-12 h-12 text-pink-400" />
            <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 to-purple-600 bg-clip-text text-transparent">
              Programme de Parrainage
            </h1>
          </div>
          <p className="text-white/70 text-lg">
            Gagnez 200$ CAD pour chaque personne que vous parrainez!
          </p>
        </div>

        {/* Lien de Parrainage */}
        <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30 mb-8">
          <h2 className="text-2xl font-bold text-white mb-4 flex items-center gap-2">
            <Users className="w-6 h-6 text-pink-400" />
            Votre Lien d'Invitation
          </h2>
          
          <div className="bg-white/10 rounded-xl p-4 mb-4">
            <p className="text-white/60 text-sm mb-2">Partagez ce lien avec vos amis:</p>
            <div className="flex gap-2">
              <input
                type="text"
                value={referralData?.referralLink || ''}
                readOnly
                className="flex-1 bg-white/5 border border-purple-500/30 rounded-lg px-4 py-3 text-white"
              />
              <button
                onClick={copyToClipboard}
                className="bg-gradient-to-r from-pink-500 to-purple-600 text-white px-6 py-3 rounded-lg hover:from-pink-600 hover:to-purple-700 transition-all flex items-center gap-2"
              >
                {copied ? <Check className="w-5 h-5" /> : <Copy className="w-5 h-5" />}
                {copied ? 'Copié!' : 'Copier'}
              </button>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-4 mt-6">
            <div className="bg-green-500/10 border border-green-500/30 rounded-xl p-4">
              <div className="text-green-400 text-3xl font-bold">{referralData?.stats?.total || 0}</div>
              <div className="text-white/70 text-sm">Total Invitations</div>
            </div>
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4">
              <div className="text-yellow-400 text-3xl font-bold">{referralData?.stats?.pending || 0}</div>
              <div className="text-white/70 text-sm">En Attente</div>
            </div>
            <div className="bg-blue-500/10 border border-blue-500/30 rounded-xl p-4">
              <div className="text-blue-400 text-3xl font-bold">{referralData?.stats?.completed || 0}</div>
              <div className="text-white/70 text-sm">Complétés</div>
            </div>
          </div>
        </div>

        {/* Comment ça marche */}
        <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30 mb-8">
          <h2 className="text-2xl font-bold text-white mb-6">Comment ça marche?</h2>
          <div className="space-y-4">
            <div className="flex gap-4">
              <div className="bg-pink-500/20 w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-pink-400 font-bold">1</span>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Partagez votre lien</h3>
                <p className="text-white/70">Envoyez votre lien d'invitation à vos amis par email, SMS ou réseaux sociaux</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="bg-purple-500/20 w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-purple-400 font-bold">2</span>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Votre ami s'inscrit</h3>
                <p className="text-white/70">Il crée son compte via votre lien unique</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="bg-blue-500/20 w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-blue-400 font-bold">3</span>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Il fait son premier achat</h3>
                <p className="text-white/70">Formation, Bot ou Abonnement mensuel</p>
              </div>
            </div>
            <div className="flex gap-4">
              <div className="bg-green-500/20 w-12 h-12 rounded-full flex items-center justify-center flex-shrink-0">
                <span className="text-green-400 font-bold">4</span>
              </div>
              <div>
                <h3 className="text-white font-semibold mb-1">Vous recevez 200$ CAD!</h3>
                <p className="text-white/70">Nous vous contactons pour vous verser votre récompense</p>
              </div>
            </div>
          </div>
        </div>

        {/* Liste des Parrainages */}
        {referrals.length > 0 && (
          <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
            <h2 className="text-2xl font-bold text-white mb-6">Mes Parrainages</h2>
            <div className="space-y-3">
              {referrals.map((referral) => (
                <div key={referral.id} className="bg-white/5 rounded-xl p-4 flex items-center justify-between">
                  <div>
                    <div className="text-white font-semibold">{referral.referredUserEmail || 'Utilisateur inscrit'}</div>
                    <div className="text-white/60 text-sm">
                      {referral.status === 'pending' && '⏳ En attente du premier achat'}
                      {referral.status === 'completed' && `✅ Achat effectué (${referral.purchaseType}: ${referral.purchaseAmount}$ CAD)`}
                      {referral.status === 'rewarded' && '🎉 Récompense versée!'}
                    </div>
                  </div>
                  <div className={`px-4 py-2 rounded-full text-sm font-medium ${
                    referral.status === 'pending' ? 'bg-yellow-500/20 text-yellow-400' :
                    referral.status === 'completed' ? 'bg-green-500/20 text-green-400' :
                    'bg-blue-500/20 text-blue-400'
                  }`}>
                    {referral.status === 'pending' && 'En attente'}
                    {referral.status === 'completed' && 'Validé'}
                    {referral.status === 'rewarded' && 'Payé'}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Referral;
