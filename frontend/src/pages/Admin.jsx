import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { adminAPI } from '../api/client';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { toast } from '../hooks/use-toast';
import { CheckCircle, XCircle, Clock, Users, ShoppingCart, DollarSign } from 'lucide-react';

const Admin = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [kycRequests, setKycRequests] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [rejectionReason, setRejectionReason] = useState('');
  const [selectedUserId, setSelectedUserId] = useState(null);

  useEffect(() => {
    if (!user || user.role !== 'admin') {
      navigate('/');
      toast({
        title: 'Accès refusé',
        description: 'Vous devez être administrateur',
        variant: 'destructive'
      });
      return;
    }

    loadData();
  }, [user, navigate]);

  const loadData = async () => {
    try {
      const [requestsRes, statsRes] = await Promise.all([
        adminAPI.getKycRequests(),
        adminAPI.getStats()
      ]);
      
      setKycRequests(requestsRes.data);
      setStats(statsRes.data);
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible de charger les données',
        variant: 'destructive'
      });
    } finally {
      setLoading(false);
    }
  };

  const handleApprove = async (userId) => {
    try {
      await adminAPI.approveKyc(userId);
      toast({
        title: 'KYC approuvé !',
        description: 'L\'utilisateur a reçu un email de confirmation'
      });
      loadData();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: error.response?.data?.detail || 'Une erreur est survenue',
        variant: 'destructive'
      });
    }
  };

  const handleReject = async () => {
    if (!rejectionReason.trim()) {
      toast({
        title: 'Erreur',
        description: 'Veuillez indiquer une raison',
        variant: 'destructive'
      });
      return;
    }

    try {
      await adminAPI.rejectKyc(selectedUserId, rejectionReason);
      toast({
        title: 'KYC rejeté',
        description: 'L\'utilisateur a été notifié'
      });
      setRejectionReason('');
      setSelectedUserId(null);
      loadData();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: error.response?.data?.detail || 'Une erreur est survenue',
        variant: 'destructive'
      });
    }
  };

  if (loading) {
    return (
      <div className=\"min-h-screen bg-[#1E1540] pt-28 pb-20 px-4 flex items-center justify-center\">
        <div className=\"text-white text-xl\">Chargement...</div>
      </div>
    );
  }

  return (
    <div className=\"min-h-screen bg-[#1E1540] pt-28 pb-20 px-4\">
      <div className=\"max-w-7xl mx-auto\">
        {/* Header */}
        <h1 className=\"text-4xl font-bold mb-8\">
          <span className=\"text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400\">
            Panel Admin
          </span>
        </h1>

        {/* Stats */}
        {stats && (
          <div className=\"grid md:grid-cols-4 gap-6 mb-12\">
            <div className=\"bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30\">
              <div className=\"flex items-center space-x-4\">
                <div className=\"w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center\">
                  <Users className=\"w-6 h-6 text-blue-400\" />
                </div>
                <div>
                  <p className=\"text-white/70 text-sm\">Utilisateurs</p>
                  <p className=\"text-2xl font-bold text-white\">{stats.totalUsers}</p>
                </div>
              </div>
            </div>

            <div className=\"bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30\">
              <div className=\"flex items-center space-x-4\">
                <div className=\"w-12 h-12 bg-yellow-500/20 rounded-full flex items-center justify-center\">
                  <Clock className=\"w-6 h-6 text-yellow-400\" />
                </div>
                <div>
                  <p className=\"text-white/70 text-sm\">KYC en attente</p>
                  <p className=\"text-2xl font-bold text-white\">{stats.pendingKyc}</p>
                </div>
              </div>
            </div>

            <div className=\"bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30\">
              <div className=\"flex items-center space-x-4\">
                <div className=\"w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center\">
                  <ShoppingCart className=\"w-6 h-6 text-green-400\" />
                </div>
                <div>
                  <p className=\"text-white/70 text-sm\">Achats</p>
                  <p className=\"text-2xl font-bold text-white\">{stats.totalPurchases}</p>
                </div>
              </div>
            </div>

            <div className=\"bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30\">
              <div className=\"flex items-center space-x-4\">
                <div className=\"w-12 h-12 bg-pink-500/20 rounded-full flex items-center justify-center\">
                  <DollarSign className=\"w-6 h-6 text-pink-400\" />
                </div>
                <div>
                  <p className=\"text-white/70 text-sm\">Revenu total</p>
                  <p className=\"text-2xl font-bold text-white\">{stats.totalRevenue.toFixed(2)}€</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* KYC Requests */}
        <div className=\"bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30\">
          <h2 className=\"text-2xl font-bold text-white mb-6\">Demandes KYC en attente</h2>

          {kycRequests.length === 0 ? (
            <div className=\"text-center py-12\">
              <CheckCircle className=\"w-16 h-16 text-green-400 mx-auto mb-4\" />
              <p className=\"text-white/70\">Aucune demande KYC en attente</p>
            </div>
          ) : (
            <div className=\"space-y-6\">
              {kycRequests.map((request) => (
                <div
                  key={request.user.id}
                  className=\"bg-[#1E1540]/50 rounded-2xl p-6 border border-purple-500/20\"
                >
                  <div className=\"flex flex-col md:flex-row justify-between items-start md:items-center gap-4\">
                    <div className=\"flex-1\">
                      <h3 className=\"text-xl font-bold text-white mb-2\">
                        {request.user.firstName} {request.user.lastName}
                      </h3>
                      <div className=\"grid md:grid-cols-2 gap-2 text-white/70\">
                        <p><strong>Email:</strong> {request.user.email}</p>
                        <p><strong>Pays:</strong> {request.user.country}</p>
                        <p><strong>Téléphone:</strong> {request.user.phone}</p>
                        <p>
                          <strong>Soumis le:</strong>{' '}
                          {new Date(request.user.kycSubmittedAt).toLocaleDateString('fr-FR')}
                        </p>
                      </div>
                      
                      <div className=\"mt-4\">
                        <p className=\"text-white/70 text-sm mb-2\">
                          <strong>Documents:</strong>
                        </p>
                        <div className=\"flex flex-wrap gap-2\">
                          {request.documents.map((doc, idx) => (
                            <span
                              key={idx}
                              className=\"bg-purple-500/20 text-purple-300 px-3 py-1 rounded-full text-sm\"
                            >
                              {doc.documentType}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div className=\"flex flex-col gap-2\">
                      <Button
                        onClick={() => handleApprove(request.user.id)}
                        className=\"bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white\"
                      >
                        <CheckCircle className=\"w-4 h-4 mr-2\" />
                        Approuver
                      </Button>
                      <Button
                        onClick={() => setSelectedUserId(request.user.id)}
                        variant=\"outline\"
                        className=\"border-red-500 text-red-500 hover:bg-red-500 hover:text-white\"
                      >
                        <XCircle className=\"w-4 h-4 mr-2\" />
                        Rejeter
                      </Button>
                    </div>
                  </div>

                  {/* Rejection Form */}
                  {selectedUserId === request.user.id && (
                    <div className=\"mt-4 pt-4 border-t border-purple-500/30\">
                      <label className=\"block text-white/80 mb-2 text-sm\">
                        Raison du rejet *
                      </label>
                      <Textarea
                        value={rejectionReason}
                        onChange={(e) => setRejectionReason(e.target.value)}
                        className=\"bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-red-500 mb-4\"
                        placeholder=\"Documents illisibles, informations incorrectes, etc.\"
                        rows={3}
                      />
                      <div className=\"flex gap-2\">
                        <Button
                          onClick={handleReject}
                          className=\"bg-red-500 hover:bg-red-600 text-white\"
                        >
                          Confirmer le rejet
                        </Button>
                        <Button
                          onClick={() => {
                            setSelectedUserId(null);
                            setRejectionReason('');
                          }}
                          variant=\"outline\"
                          className=\"border-white/30 text-white hover:bg-white/10\"
                        >
                          Annuler
                        </Button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Admin;