import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { toast } from '../hooks/use-toast';
import { Check, X, Clock, ExternalLink, CreditCard, Zap } from 'lucide-react';
import axios from 'axios';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const SubscriptionSection = ({ user }) => {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const [subscription, setSubscription] = useState(null);
  const [loading, setLoading] = useState(true);
  const [inviteLinks, setInviteLinks] = useState(null);
  const [actionLoading, setActionLoading] = useState(false);

  useEffect(() => {
    loadSubscription();
  }, []);

  const loadSubscription = async () => {
    try {
      const response = await axios.get(`${API}/subscriptions/status`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setSubscription(response.data);
    } catch (error) {
      if (error.response?.status !== 404) {
        console.error('Error loading subscription:', error);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleGetInviteLink = async () => {
    setActionLoading(true);
    try {
      const response = await axios.get(`${API}/subscriptions/invite-links`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      setInviteLinks(response.data.inviteLinks);
      toast({
        title: '✓ Liens générés',
        description: 'Vos liens d\'invitation Telegram sont prêts !',
      });
    } catch (error) {
      toast({
        title: 'Erreur',
        description: error.response?.data?.detail || 'Impossible de générer les liens',
        variant: 'destructive'
      });
    } finally {
      setActionLoading(false);
    }
  };

  const handleCancelSubscription = async () => {
    if (!window.confirm('Êtes-vous sûr de vouloir annuler votre abonnement ? Vous garderez l\'accès jusqu\'à la fin de la période en cours.')) {
      return;
    }

    setActionLoading(true);
    try {
      await axios.post(`${API}/subscriptions/cancel`, {}, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      toast({
        title: '✓ Abonnement annulé',
        description: 'Vous conserverez l\'accès jusqu\'à la fin de votre période.',
      });
      
      loadSubscription();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: error.response?.data?.detail || 'Erreur lors de l\'annulation',
        variant: 'destructive'
      });
    } finally {
      setActionLoading(false);
    }
  };

  const handleReactivateSubscription = async () => {
    setActionLoading(true);
    try {
      await axios.post(`${API}/subscriptions/reactivate`, {}, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      
      toast({
        title: '✓ Abonnement réactivé',
        description: 'Votre abonnement continuera automatiquement.',
      });
      
      loadSubscription();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: error.response?.data?.detail || 'Erreur lors de la réactivation',
        variant: 'destructive'
      });
    } finally {
      setActionLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('fr-FR', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  const getStatusBadge = (status) => {
    const badges = {
      'active': { icon: Check, color: 'bg-green-500/20 text-green-400 border-green-500/30', text: 'Actif' },
      'past_due': { icon: Clock, color: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30', text: 'Paiement en attente' },
      'canceled': { icon: X, color: 'bg-red-500/20 text-red-400 border-red-500/30', text: 'Annulé' },
      'incomplete': { icon: Clock, color: 'bg-blue-500/20 text-blue-400 border-blue-500/30', text: 'En attente' },
    };

    const badge = badges[status] || badges['incomplete'];
    const Icon = badge.icon;

    return (
      <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm border ${badge.color}`}>
        <Icon className="w-4 h-4" />
        {badge.text}
      </span>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="w-8 h-8 border-4 border-purple-500/30 border-t-purple-500 rounded-full animate-spin" />
      </div>
    );
  }

  // Pas d'abonnement
  if (!subscription) {
    return (
      <div className="text-center py-12">
        <div className="w-20 h-20 bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-full flex items-center justify-center mx-auto mb-6">
          <Zap className="w-10 h-10 text-pink-400" />
        </div>
        <h3 className="text-2xl font-bold text-white mb-4">
          {t(language, 'subscription.dashboard.noSubscription')}
        </h3>
        <p className="text-white/60 mb-6 max-w-md mx-auto">
          {t(language, 'subscription.dashboard.noSubscriptionText')}
        </p>
        <Button
          onClick={() => navigate('/subscription')}
          className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-6 text-lg"
        >
          {t(language, 'subscription.subscribe')}
        </Button>
      </div>
    );
  }

  // Abonnement actif
  return (
    <div className="space-y-6">
      {/* Status Card */}
      <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 sm:p-8 border border-purple-500/30">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h3 className="text-2xl font-bold text-white mb-2">
              Abonnement Signaux de Trading
            </h3>
            {getStatusBadge(subscription.status)}
          </div>
          <div className="text-right">
            <div className="text-3xl font-bold text-white">150$ CAD</div>
            <div className="text-white/60 text-sm">par mois</div>
          </div>
        </div>

        {/* Info */}
        <div className="grid sm:grid-cols-2 gap-4 mb-6">
          <div className="bg-white/5 rounded-lg p-4">
            <div className="text-white/60 text-sm mb-1">Prochain renouvellement</div>
            <div className="text-white font-semibold">
              {formatDate(subscription.currentPeriodEnd)}
            </div>
          </div>

          {subscription.cancelAtPeriodEnd && (
            <div className="bg-yellow-500/10 rounded-lg p-4 border border-yellow-500/30">
              <div className="text-yellow-400 text-sm font-semibold mb-1">
                ⚠️ Annulation prévue
              </div>
              <div className="text-white/80 text-sm">
                Accès jusqu'au {formatDate(subscription.currentPeriodEnd)}
              </div>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="space-y-3">
          {subscription.status === 'active' && !subscription.cancelAtPeriodEnd && (
            <>
              <Button
                onClick={handleGetInviteLink}
                disabled={actionLoading}
                className="w-full bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white"
              >
                <ExternalLink className="w-4 h-4 mr-2" />
                Obtenir les liens Telegram
              </Button>

              {inviteLinks && (
                <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4 space-y-3">
                  <p className="text-green-400 text-sm font-semibold mb-3">
                    ✓ Vos liens d'invitation personnels :
                  </p>
                  
                  {Object.entries(inviteLinks).map(([channelName, link]) => (
                    link ? (
                      <div key={channelName} className="bg-white/5 rounded-lg p-3">
                        <p className="text-white font-semibold text-sm mb-1">
                          📢 Canal {channelName}
                        </p>
                        <a
                          href={link}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="text-blue-400 hover:text-blue-300 underline text-xs break-all"
                        >
                          {link}
                        </a>
                      </div>
                    ) : (
                      <div key={channelName} className="bg-red-500/10 rounded-lg p-3">
                        <p className="text-red-400 text-sm">
                          ⚠️ {channelName}: Lien non disponible
                        </p>
                      </div>
                    )
                  ))}
                  
                  <p className="text-white/60 text-xs mt-3">
                    💡 Cliquez sur chaque lien pour rejoindre les canaux
                  </p>
                </div>
              )}

              <Button
                onClick={handleCancelSubscription}
                disabled={actionLoading}
                variant="outline"
                className="w-full border-red-500/30 text-red-400 hover:bg-red-500/10"
              >
                Annuler l'abonnement
              </Button>
            </>
          )}

          {subscription.cancelAtPeriodEnd && (
            <Button
              onClick={handleReactivateSubscription}
              disabled={actionLoading}
              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white"
            >
              Réactiver l'abonnement
            </Button>
          )}

          {subscription.status === 'past_due' && (
            <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-4">
              <p className="text-yellow-400 font-semibold mb-2">
                ⚠️ Paiement requis
              </p>
              <p className="text-white/80 text-sm mb-3">
                Votre dernier paiement a échoué. Veuillez mettre à jour votre méthode de paiement.
              </p>
              <Button
                onClick={() => navigate('/subscription')}
                className="w-full bg-yellow-500 hover:bg-yellow-600 text-white"
              >
                <CreditCard className="w-4 h-4 mr-2" />
                Mettre à jour le paiement
              </Button>
            </div>
          )}
        </div>
      </div>

      {/* Features Reminder */}
      <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-2xl p-6 border border-purple-500/30">
        <h4 className="text-lg font-bold text-white mb-4">✨ Votre abonnement inclut :</h4>
        <ul className="space-y-2 text-white/70">
          <li className="flex items-center gap-2">
            <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
            Signaux en temps réel sur tous les marchés
          </li>
          <li className="flex items-center gap-2">
            <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
            Accès aux canaux Telegram privés
          </li>
          <li className="flex items-center gap-2">
            <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
            Analyses de marché professionnelles
          </li>
          <li className="flex items-center gap-2">
            <Check className="w-4 h-4 text-green-400 flex-shrink-0" />
            Support 24/7
          </li>
        </ul>
      </div>
    </div>
  );
};

export default SubscriptionSection;
