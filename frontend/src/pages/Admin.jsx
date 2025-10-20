import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { adminAPI } from '../api/client';
import { Button } from '../components/ui/button';
import { Textarea } from '../components/ui/textarea';
import { toast } from '../hooks/use-toast';
import { CheckCircle, XCircle, Clock, Users, ShoppingCart, DollarSign, ArrowLeft, Star } from 'lucide-react';

const Admin = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [kycRequests, setKycRequests] = useState([]);
  const [pendingTestimonials, setPendingTestimonials] = useState([]);
  const [allTestimonials, setAllTestimonials] = useState([]);
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
      const [requestsRes, statsRes, testimonialsRes, allTestimonialsRes] = await Promise.all([
        adminAPI.getKycRequests(),
        adminAPI.getStats(),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/testimonials/pending`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        }).then(res => res.json()),
        fetch(`${process.env.REACT_APP_BACKEND_URL}/api/testimonials/approved`, {
          headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        }).then(res => res.json())
      ]);
      
      setKycRequests(requestsRes.data);
      setStats(statsRes.data);
      setPendingTestimonials(testimonialsRes);
      setAllTestimonials(allTestimonialsRes);
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

  const handleApproveTestimonial = async (testimonialId) => {
    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/testimonials/approve/${testimonialId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      toast({
        title: '✓ Témoignage approuvé',
        description: 'Le témoignage est maintenant visible publiquement'
      });
      loadData();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible d\'approuver le témoignage',
        variant: 'destructive'
      });
    }
  };

  const handleRejectTestimonial = async (testimonialId) => {
    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/testimonials/reject/${testimonialId}`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      toast({
        title: '✓ Témoignage rejeté',
        description: 'Le témoignage a été rejeté'
      });
      loadData();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible de rejeter le témoignage',
        variant: 'destructive'
      });
    }
  };

  const handleDeleteTestimonial = async (testimonialId) => {
    if (!window.confirm('Êtes-vous sûr de vouloir supprimer ce témoignage ?')) {
      return;
    }

    try {
      await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/admin/testimonials/delete/${testimonialId}`, {
        method: 'DELETE',
        headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
      });
      toast({
        title: '✓ Témoignage supprimé',
        description: 'Le témoignage a été supprimé définitivement'
      });
      loadData();
    } catch (error) {
      toast({
        title: 'Erreur',
        description: 'Impossible de supprimer le témoignage',
        variant: 'destructive'
      });
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
      <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4 flex items-center justify-center">
        <div className="text-white text-xl">Chargement...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Back Button */}
        <Button
          onClick={() => navigate('/')}
          variant="ghost"
          className="mb-6 text-pink-400 hover:text-pink-300 hover:bg-pink-500/10"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Retour à l'accueil
        </Button>

        {/* Header */}
        <h1 className="text-4xl font-bold mb-8">
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
            Panel Admin
          </span>
        </h1>

        {/* Stats */}
        {stats && (
          <div className="grid md:grid-cols-4 gap-6 mb-12">
            <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-blue-500/20 rounded-full flex items-center justify-center">
                  <Users className="w-6 h-6 text-blue-400" />
                </div>
                <div>
                  <p className="text-white/70 text-sm">Utilisateurs</p>
                  <p className="text-2xl font-bold text-white">{stats.totalUsers}</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-yellow-500/20 rounded-full flex items-center justify-center">
                  <Clock className="w-6 h-6 text-yellow-400" />
                </div>
                <div>
                  <p className="text-white/70 text-sm">KYC en attente</p>
                  <p className="text-2xl font-bold text-white">{stats.pendingKyc}</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center">
                  <ShoppingCart className="w-6 h-6 text-green-400" />
                </div>
                <div>
                  <p className="text-white/70 text-sm">Achats</p>
                  <p className="text-2xl font-bold text-white">{stats.totalPurchases}</p>
                </div>
              </div>
            </div>

            <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30">
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-pink-500/20 rounded-full flex items-center justify-center">
                  <DollarSign className="w-6 h-6 text-pink-400" />
                </div>
                <div>
                  <p className="text-white/70 text-sm">Revenu total</p>
                  <p className="text-2xl font-bold text-white">{stats.totalRevenue.toFixed(2)}€</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* KYC Requests */}
        <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
          <h2 className="text-2xl font-bold text-white mb-6">Demandes KYC en attente</h2>

          {kycRequests.length === 0 ? (
            <div className="text-center py-12">
              <CheckCircle className="w-16 h-16 text-green-400 mx-auto mb-4" />
              <p className="text-white/70">Aucune demande KYC en attente</p>
            </div>
          ) : (
            <div className="space-y-6">
              {kycRequests.map((request) => (
                <div
                  key={request.user.id}
                  className="bg-[#1E1540]/50 rounded-2xl p-6 border border-purple-500/20"
                >
                  <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
                    <div className="flex-1">
                      <h3 className="text-xl font-bold text-white mb-2">
                        {request.user.firstName} {request.user.lastName}
                      </h3>
                      <div className="grid md:grid-cols-2 gap-2 text-white/70">
                        <p><strong>Email:</strong> {request.user.email}</p>
                        <p><strong>Pays:</strong> {request.user.country}</p>
                        <p><strong>Téléphone:</strong> {request.user.phone}</p>
                        <p>
                          <strong>Soumis le:</strong>{' '}
                          {new Date(request.user.kycSubmittedAt).toLocaleDateString('fr-FR')}
                        </p>
                      </div>
                      
                      <div className="mt-4">
                        <p className="text-white/70 text-sm mb-3">
                          <strong>Documents KYC :</strong>
                        </p>
                        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                          {request.documents.map((doc, idx) => {
                            const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
                            const docUrl = `${BACKEND_URL}/api/kyc/document/${doc.id}`;
                            const docLabel = doc.documentType === 'passport' ? 'Passeport' :
                                           doc.documentType === 'idCard' ? 'Carte d\'identité' :
                                           'Justificatif de domicile';
                            
                            return (
                              <div key={idx} className="bg-purple-500/10 rounded-lg p-3">
                                <p className="text-purple-300 text-xs mb-2 font-semibold">{docLabel}</p>
                                {doc.filename.toLowerCase().endsWith('.pdf') ? (
                                  <div className="bg-white/5 rounded p-4 text-center">
                                    <p className="text-white/60 text-xs mb-2">📄 PDF</p>
                                    <a
                                      href={docUrl}
                                      target="_blank"
                                      rel="noopener noreferrer"
                                      className="text-pink-400 hover:text-pink-300 text-sm underline"
                                    >
                                      Ouvrir
                                    </a>
                                  </div>
                                ) : (
                                  <a href={docUrl} target="_blank" rel="noopener noreferrer">
                                    <img
                                      src={docUrl}
                                      alt={docLabel}
                                      className="w-full h-32 object-cover rounded cursor-pointer hover:opacity-80 transition"
                                    />
                                  </a>
                                )}
                              </div>
                            );
                          })}
                        </div>
                      </div>
                    </div>

                    <div className="flex flex-col gap-2">
                      <Button
                        onClick={() => handleApprove(request.user.id)}
                        className="bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white"
                      >
                        <CheckCircle className="w-4 h-4 mr-2" />
                        Approuver
                      </Button>
                      <Button
                        onClick={() => setSelectedUserId(request.user.id)}
                        variant="outline"
                        className="border-red-500 text-red-500 hover:bg-red-500 hover:text-white"
                      >
                        <XCircle className="w-4 h-4 mr-2" />
                        Rejeter
                      </Button>
                    </div>
                  </div>

                  {/* Rejection Form */}
                  {selectedUserId === request.user.id && (
                    <div className="mt-4 pt-4 border-t border-purple-500/30">
                      <label className="block text-white/80 mb-2 text-sm">
                        Raison du rejet *
                      </label>
                      <Textarea
                        value={rejectionReason}
                        onChange={(e) => setRejectionReason(e.target.value)}
                        className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-red-500 mb-4"
                        placeholder="Documents illisibles, informations incorrectes, etc."
                        rows={3}
                      />
                      <div className="flex gap-2">
                        <Button
                          onClick={handleReject}
                          className="bg-red-500 hover:bg-red-600 text-white"
                        >
                          Confirmer le rejet
                        </Button>
                        <Button
                          onClick={() => {
                            setSelectedUserId(null);
                            setRejectionReason('');
                          }}
                          variant="outline"
                          className="border-white/30 text-white hover:bg-white/10"
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

        {/* Pending Testimonials */}
        <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30 mt-8">
          <h2 className="text-2xl font-bold text-white mb-6">Témoignages en attente de validation</h2>
          
          {pendingTestimonials.length === 0 ? (
            <div className="text-center py-12 text-white/70">
              <p>Aucun témoignage en attente</p>
            </div>
          ) : (
            <div className="space-y-4">
              {pendingTestimonials.map((testimonial) => (
                <div
                  key={testimonial.id}
                  className="bg-purple-500/10 rounded-xl p-6 border border-purple-500/30"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-bold text-white">{testimonial.userName}</h3>
                      <p className="text-pink-400 text-sm">{testimonial.country}</p>
                    </div>
                    <div className="flex space-x-1">
                      {[...Array(5)].map((_, index) => (
                        <Star
                          key={index}
                          className={`w-5 h-5 ${
                            index < testimonial.rating
                              ? 'text-yellow-400 fill-yellow-400'
                              : 'text-gray-600'
                          }`}
                        />
                      ))}
                    </div>
                  </div>

                  <p className="text-white/80 mb-4 italic">"{testimonial.comment}"</p>

                  <div className="flex space-x-3">
                    <Button
                      onClick={() => handleApproveTestimonial(testimonial.id)}
                      className="bg-green-500 hover:bg-green-600 text-white"
                    >
                      <CheckCircle className="w-4 h-4 mr-2" />
                      Approuver
                    </Button>
                    <Button
                      onClick={() => handleRejectTestimonial(testimonial.id)}
                      variant="destructive"
                      className="bg-red-500 hover:bg-red-600"
                    >
                      <XCircle className="w-4 h-4 mr-2" />
                      Rejeter
                    </Button>
                  </div>
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