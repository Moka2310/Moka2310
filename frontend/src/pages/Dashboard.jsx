import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { t, translations } from '../translations';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { toast } from '../hooks/use-toast';
import { purchasesAPI, formationsAPI, kycAPI } from '../api/client';
import { 
  User, 
  LogOut, 
  Upload, 
  CheckCircle, 
  Clock, 
  XCircle, 
  Download,
  ExternalLink,
  Video,
  ArrowLeft,
  Settings,
  Trash2,
  Star
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../components/ui/dialog';

const Dashboard = () => {
  const { user, logout, updateUser } = useAuth();
  const { language } = useLanguage();
  const navigate = useNavigate();
  const [kycData, setKycData] = useState({
    firstName: user?.firstName || '',
    lastName: user?.lastName || '',
    country: user?.country || '',
    phone: user?.phone || ''
  });
  const [documents, setDocuments] = useState({
    passport: null,
    idCard: null,
    proofOfResidence: null
  });
  const [consentChecked, setConsentChecked] = useState(false);
  const [purchases, setPurchases] = useState([]);
  const [purchasedFormations, setPurchasedFormations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showDeleteDialog, setShowDeleteDialog] = useState(false);
  const [deleteConfirmation, setDeleteConfirmation] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);
  const [testimonialData, setTestimonialData] = useState({
    rating: 5,
    comment: '',
    country: user?.country || ''
  });
  const [myTestimonial, setMyTestimonial] = useState(null);
  const [testimonialLoading, setTestimonialLoading] = useState(false);

  useEffect(() => {
    const loadData = async () => {
      try {
        // Load user purchases
        const purchasesResponse = await purchasesAPI.getMyPurchases();
        const userPurchases = purchasesResponse.data;
        setPurchases(userPurchases);

        // Load formations for purchased items
        const formationsResponse = await formationsAPI.getAll();
        const allFormations = formationsResponse.data;
        
        const purchased = userPurchases
          .filter(p => p.status === 'completed')
          .map(p => allFormations.find(f => f.id === p.formationId))
          .filter(Boolean);
        
        setPurchasedFormations(purchased);
      } catch (error) {
        console.error('Failed to load data:', error);
      } finally {
        setLoading(false);
      }
    };

    if (user) {
      loadData();
    }
  }, [user]);

  const handleLogout = () => {
    logout();
    navigate('/');
    toast({
      title: language === 'fr' ? 'Déconnexion réussie' : 'Logout successful',
      description: language === 'fr' ? 'À bientôt !' : 'See you soon!'
    });
  };

  const handleDeleteAccount = async () => {
    // Check confirmation text
    const expectedText = language === 'fr' ? 'SUPPRIMER' : 'DELETE';
    if (deleteConfirmation !== expectedText) {
      toast({
        title: language === 'fr' ? 'Confirmation incorrecte' : 'Incorrect confirmation',
        description: language === 'fr' ? `Veuillez taper "${expectedText}" pour confirmer` : `Please type "${expectedText}" to confirm`,
        variant: 'destructive'
      });
      return;
    }

    setIsDeleting(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/auth/delete-account`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to delete account');
      }

      toast({
        title: language === 'fr' ? '✓ Compte supprimé' : '✓ Account deleted',
        description: language === 'fr' ? 'Toutes vos données ont été supprimées. Vous allez recevoir un email de confirmation.' : 'All your data has been deleted. You will receive a confirmation email.'
      });

      // Logout and redirect
      setTimeout(() => {
        logout();
        navigate('/');
      }, 2000);

    } catch (error) {
      toast({
        title: language === 'fr' ? 'Erreur' : 'Error',
        description: language === 'fr' ? 'Impossible de supprimer le compte' : 'Failed to delete account',
        variant: 'destructive'
      });
    } finally {
      setIsDeleting(false);
    }
  };

  const loadMyTestimonial = async () => {
    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/testimonials/my-testimonial`, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      });
      const data = await response.json();
      if (data.exists) {
        setMyTestimonial(data.testimonial);
      }
    } catch (error) {
      console.error('Failed to load testimonial:', error);
    }
  };

  const handleTestimonialSubmit = async (e) => {
    e.preventDefault();
    
    if (!testimonialData.comment.trim()) {
      toast({
        title: language === 'fr' ? 'Commentaire requis' : 'Comment required',
        description: language === 'fr' ? 'Veuillez écrire un commentaire' : 'Please write a comment',
        variant: 'destructive'
      });
      return;
    }

    setTestimonialLoading(true);

    try {
      const response = await fetch(`${process.env.REACT_APP_BACKEND_URL}/api/testimonials/submit`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        },
        body: JSON.stringify(testimonialData)
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail);
      }

      toast({
        title: language === 'fr' ? '✓ Témoignage soumis' : '✓ Testimonial submitted',
        description: language === 'fr' ? 'Merci ! Votre témoignage sera examiné par notre équipe.' : 'Thank you! Your testimonial will be reviewed by our team.'
      });

      loadMyTestimonial();
      setTestimonialData({ rating: 5, comment: '', country: user?.country || '' });

    } catch (error) {
      toast({
        title: language === 'fr' ? 'Erreur' : 'Error',
        description: error.message,
        variant: 'destructive'
      });
    } finally {
      setTestimonialLoading(false);
    }
  };

  const handleKycSubmit = async (e) => {
    e.preventDefault();

    // Check consent
    if (!consentChecked) {
      toast({
        title: language === 'fr' ? 'Consentement requis' : 'Consent required',
        description: language === 'fr' ? 'Veuillez accepter les conditions d\'utilisation des documents' : 'Please accept the document usage terms',
        variant: 'destructive'
      });
      return;
    }
    
    // Check if all documents are uploaded
    if (!documents.passport || !documents.idCard || !documents.proofOfResidence) {
      toast({
        title: language === 'fr' ? 'Documents manquants' : 'Missing documents',
        description: language === 'fr' ? 'Veuillez télécharger tous les documents requis' : 'Please upload all required documents',
        variant: 'destructive'
      });
      return;
    }

    try {
      // Create FormData
      const formData = new FormData();
      formData.append('firstName', kycData.firstName);
      formData.append('lastName', kycData.lastName);
      formData.append('country', kycData.country);
      formData.append('phone', kycData.phone);
      formData.append('passport', documents.passport);
      formData.append('idCard', documents.idCard);
      formData.append('proofOfResidence', documents.proofOfResidence);

      // Submit KYC
      await kycAPI.submit(formData);

      // Update user data
      await updateUser();

      toast({
        title: t(language, 'dashboard.kyc.success'),
        description: language === 'fr' ? 'Votre demande est en cours de vérification. Vous recevrez un email une fois validée.' : 'Your request is being reviewed. You will receive an email once validated.'
      });
    } catch (error) {
      toast({
        title: t(language, 'common.error'),
        description: error.response?.data?.detail || t(language, 'dashboard.kyc.error'),
        variant: 'destructive'
      });
    }
  };

  const handleFileChange = (e, docType) => {
    const file = e.target.files[0];
    if (file) {
      setDocuments(prev => ({ ...prev, [docType]: file }));
      toast({
        title: language === 'fr' ? 'Document ajouté' : 'Document added',
        description: language === 'fr' ? `${file.name} a été ajouté avec succès` : `${file.name} has been added successfully`
      });
    }
  };

  const getKycStatusBadge = () => {
    switch (user?.kycStatus) {
      case 'approved':
        return (
          <div className="flex items-center space-x-2 bg-green-500/20 text-green-400 px-4 py-2 rounded-full">
            <CheckCircle className="w-5 h-5" />
            <span>Vérifié</span>
          </div>
        );
      case 'pending_review':
        return (
          <div className="flex items-center space-x-2 bg-yellow-500/20 text-yellow-400 px-4 py-2 rounded-full">
            <Clock className="w-5 h-5" />
            <span>En cours de vérification</span>
          </div>
        );
      case 'rejected':
        return (
          <div className="flex items-center space-x-2 bg-red-500/20 text-red-400 px-4 py-2 rounded-full">
            <XCircle className="w-5 h-5" />
            <span>Refusé</span>
          </div>
        );
      default:
        return (
          <div className="flex items-center space-x-2 bg-purple-500/20 text-purple-400 px-4 py-2 rounded-full">
            <Clock className="w-5 h-5" />
            <span>{t(language, 'dashboard.kyc.pending')}</span>
          </div>
        );
    }
  };

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
          {language === 'fr' ? 'Retour à l\'accueil' : 'Back to home'}
        </Button>

        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-4xl font-bold mb-2">
              <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                {t(language, 'dashboard.title')}
              </span>
            </h1>
            <p className="text-white/70">{t(language, 'dashboard.welcome')}, {user?.email}</p>
          </div>
          <div className="flex items-center space-x-4">
            {getKycStatusBadge()}
            <Button
              onClick={handleLogout}
              variant="outline"
              className="border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white"
            >
              <LogOut className="w-4 h-4 mr-2" />
              {t(language, 'nav.logout')}
            </Button>
          </div>
        </div>

        {/* Tabs */}
        <Tabs defaultValue="formations" className="w-full">
          <TabsList className="bg-[#2B1F5C] border border-purple-500/30 p-1 mb-8">
            <TabsTrigger 
              value="formations"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white"
            >
              <Video className="w-4 h-4 mr-2" />
              {t(language, 'dashboard.myFormations')}
            </TabsTrigger>
            <TabsTrigger 
              value="kyc"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white"
            >
              <User className="w-4 h-4 mr-2" />
              {t(language, 'dashboard.kyc.title')}
            </TabsTrigger>
            <TabsTrigger 
              value="testimonial"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white"
            >
              <Star className="w-4 h-4 mr-2" />
              {language === 'fr' ? 'Témoignage' : 'Testimonial'}
            </TabsTrigger>
            <TabsTrigger 
              value="settings"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white"
            >
              <Settings className="w-4 h-4 mr-2" />
              {language === 'fr' ? 'Paramètres' : 'Settings'}
            </TabsTrigger>
          </TabsList>

          {/* Formations Tab */}
          <TabsContent value="formations">
            {purchasedFormations.length === 0 ? (
              <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-12 border border-purple-500/30 text-center">
                <Video className="w-16 h-16 text-pink-400 mx-auto mb-4" />
                <h3 className="text-2xl font-bold text-white mb-2">{t(language, 'dashboard.noFormations')}</h3>
                <p className="text-white/70 mb-6">{language === 'fr' ? 'Parcourez notre boutique pour commencer votre parcours de trading' : 'Browse our shop to start your trading journey'}</p>
                <Button
                  onClick={() => navigate('/boutique')}
                  className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-4 rounded-full"
                >
                  {t(language, 'dashboard.shopButton')}
                </Button>
              </div>
            ) : (
              <div className="space-y-6">
                {user?.kycStatus !== 'approved' && (
                  <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-6">
                    <h3 className="text-yellow-400 font-bold mb-2">{language === 'fr' ? 'Action requise' : 'Action required'}</h3>
                    <p className="text-white/80">
                      {language === 'fr' 
                        ? 'Veuillez compléter votre vérification KYC pour accéder aux vidéos et aux canaux Telegram VIP.'
                        : 'Please complete your KYC verification to access videos and VIP Telegram channels.'
                      }
                    </p>
                  </div>
                )}

                <div className="grid md:grid-cols-2 gap-6">
                  {purchasedFormations.map((formation) => {
                    // Get translated formation title
                    const translatedTitle = translations[language]?.formations?.[formation.title]?.title || formation.title;
                    
                    return (
                    <div
                      key={formation.id}
                      className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl overflow-hidden border border-purple-500/30"
                    >
                      <img
                        src={formation.image}
                        alt={translatedTitle}
                        className="w-full h-48 object-cover"
                      />
                      <div className="p-6">
                        <h3 className="text-2xl font-bold text-white mb-2">{translatedTitle}</h3>
                        <p className="text-white/70 mb-4">
                          {formation.videoCount} {language === 'fr' ? 'vidéos disponibles' : 'videos available'}
                        </p>

                        {user?.kycStatus === 'approved' ? (
                          <div className="space-y-3">
                            <Button
                              className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white"
                              onClick={() => toast({ 
                                title: language === 'fr' ? 'Vidéos disponibles' : 'Videos available', 
                                description: language === 'fr' ? 'Fonctionnalité en cours de développement' : 'Feature under development' 
                              })}
                            >
                              <Download className="w-4 h-4 mr-2" />
                              {language === 'fr' ? 'Accéder aux vidéos' : 'Access videos'}
                            </Button>
                            {formation.telegramLinks.map((link, idx) => (
                              <Button
                                key={idx}
                                variant="outline"
                                className="w-full border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white"
                                onClick={() => window.open(link.url, '_blank')}
                              >
                                <ExternalLink className="w-4 h-4 mr-2" />
                                {link.name}
                              </Button>
                            ))}
                          </div>
                        ) : (
                          <div className="bg-purple-500/20 rounded-xl p-4 text-center">
                            <p className="text-white/70 text-sm">
                              {language === 'fr' ? 'Complétez votre KYC pour débloquer l\'accès' : 'Complete your KYC to unlock access'}
                            </p>
                          </div>
                        )}
                      </div>
                    </div>
                    );
                  })}
                </div>
              </div>
            )}
          </TabsContent>

          {/* KYC Tab */}
          <TabsContent value="kyc">
            <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
              <h2 className="text-3xl font-bold text-white mb-6">
                {language === 'fr' ? 'Vérification d\'identité (KYC)' : 'Identity Verification (KYC)'}
              </h2>
              
              {user?.kycStatus === 'approved' ? (
                <div className="text-center py-12">
                  <CheckCircle className="w-20 h-20 text-green-400 mx-auto mb-4" />
                  <h3 className="text-2xl font-bold text-white mb-2">
                    {language === 'fr' ? 'Compte vérifié !' : 'Account verified!'}
                  </h3>
                  <p className="text-white/70">
                    {language === 'fr' 
                      ? 'Votre identité a été vérifiée avec succès. Vous avez accès à toutes vos formations.'
                      : 'Your identity has been successfully verified. You have access to all your courses.'
                    }
                  </p>
                </div>
              ) : user?.kycStatus === 'pending_review' ? (
                <div className="text-center py-12">
                  <Clock className="w-20 h-20 text-yellow-400 mx-auto mb-4" />
                  <h3 className="text-2xl font-bold text-white mb-2">
                    {language === 'fr' ? 'Vérification en cours' : 'Verification in progress'}
                  </h3>
                  <p className="text-white/70">
                    {language === 'fr' 
                      ? 'Votre demande est en cours de vérification. Vous recevrez un email une fois le processus terminé.'
                      : 'Your request is being reviewed. You will receive an email once the process is complete.'
                    }
                  </p>
                </div>
              ) : (
                <form onSubmit={handleKycSubmit} className="space-y-6">
                  {/* Personal Info */}
                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-white/80 mb-2 text-sm">{language === 'fr' ? 'Prénom' : 'First Name'}*</label>
                      <Input
                        type="text"
                        required
                        value={kycData.firstName}
                        onChange={(e) => setKycData({ ...kycData, firstName: e.target.value })}
                        className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                        placeholder={language === 'fr' ? 'Votre prénom' : 'Your first name'}
                      />
                    </div>
                    <div>
                      <label className="block text-white/80 mb-2 text-sm">{language === 'fr' ? 'Nom' : 'Last Name'}*</label>
                      <Input
                        type="text"
                        required
                        value={kycData.lastName}
                        onChange={(e) => setKycData({ ...kycData, lastName: e.target.value })}
                        className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                        placeholder={language === 'fr' ? 'Votre nom' : 'Your last name'}
                      />
                    </div>
                  </div>

                  <div className="grid md:grid-cols-2 gap-6">
                    <div>
                      <label className="block text-white/80 mb-2 text-sm">{language === 'fr' ? 'Pays' : 'Country'}*</label>
                      <Input
                        type="text"
                        required
                        value={kycData.country}
                        onChange={(e) => setKycData({ ...kycData, country: e.target.value })}
                        className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                        placeholder={language === 'fr' ? 'Votre pays' : 'Your country'}
                      />
                    </div>
                    <div>
                      <label className="block text-white/80 mb-2 text-sm">{language === 'fr' ? 'Téléphone' : 'Phone'}*</label>
                      <Input
                        type="tel"
                        required
                        value={kycData.phone}
                        onChange={(e) => setKycData({ ...kycData, phone: e.target.value })}
                        className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                        placeholder="+33 6 12 34 56 78"
                      />
                    </div>
                  </div>

                  {/* Document Uploads */}
                  <div className="space-y-4 pt-6 border-t border-purple-500/30">
                    <h3 className="text-xl font-bold text-white mb-4">{t(language, 'dashboard.kyc.documents')}</h3>

                    {/* Passport */}
                    <div className="bg-purple-500/10 rounded-xl p-4">
                      <label className="block text-white/80 mb-2 font-semibold">{t(language, 'dashboard.kyc.passport')}*</label>
                      <div className="flex items-center space-x-4">
                        <label className="flex-1 cursor-pointer">
                          <div className="border-2 border-dashed border-purple-500/50 rounded-xl p-6 text-center hover:border-pink-500/50 transition-colors">
                            <Upload className="w-8 h-8 text-pink-400 mx-auto mb-2" />
                            <p className="text-white/70 text-sm">
                              {documents.passport ? documents.passport.name : (language === 'fr' ? 'Cliquez pour télécharger' : 'Click to upload')}
                            </p>
                          </div>
                          <input
                            type="file"
                            accept="image/*,application/pdf"
                            className="hidden"
                            onChange={(e) => handleFileChange(e, 'passport')}
                          />
                        </label>
                      </div>
                    </div>

                    {/* ID Card */}
                    <div className="bg-purple-500/10 rounded-xl p-4">
                      <label className="block text-white/80 mb-2 font-semibold">{t(language, 'dashboard.kyc.idCard')}*</label>
                      <div className="flex items-center space-x-4">
                        <label className="flex-1 cursor-pointer">
                          <div className="border-2 border-dashed border-purple-500/50 rounded-xl p-6 text-center hover:border-pink-500/50 transition-colors">
                            <Upload className="w-8 h-8 text-pink-400 mx-auto mb-2" />
                            <p className="text-white/70 text-sm">
                              {documents.idCard ? documents.idCard.name : (language === 'fr' ? 'Cliquez pour télécharger' : 'Click to upload')}
                            </p>
                          </div>
                          <input
                            type="file"
                            accept="image/*,application/pdf"
                            className="hidden"
                            onChange={(e) => handleFileChange(e, 'idCard')}
                          />
                        </label>
                      </div>
                    </div>

                    {/* Proof of Residence */}
                    <div className="bg-purple-500/10 rounded-xl p-4">
                      <label className="block text-white/80 mb-2 font-semibold">{t(language, 'dashboard.kyc.residence')}*</label>
                      <div className="flex items-center space-x-4">
                        <label className="flex-1 cursor-pointer">
                          <div className="border-2 border-dashed border-purple-500/50 rounded-xl p-6 text-center hover:border-pink-500/50 transition-colors">
                            <Upload className="w-8 h-8 text-pink-400 mx-auto mb-2" />
                            <p className="text-white/70 text-sm">
                              {documents.proofOfResidence ? documents.proofOfResidence.name : (language === 'fr' ? 'Cliquez pour télécharger' : 'Click to upload')}
                            </p>
                          </div>
                          <input
                            type="file"
                            accept="image/*,application/pdf"
                            className="hidden"
                            onChange={(e) => handleFileChange(e, 'proofOfResidence')}
                          />
                        </label>
                      </div>
                    </div>
                  </div>

                  {/* Consent Checkbox */}
                  <div className="pt-6 border-t border-purple-500/30">
                    <div className="flex items-start space-x-3">
                      <input
                        type="checkbox"
                        id="consent"
                        checked={consentChecked}
                        onChange={(e) => setConsentChecked(e.target.checked)}
                        className="mt-1 w-4 h-4 text-pink-500 bg-transparent border-2 border-purple-500/50 rounded focus:ring-pink-500 focus:ring-2"
                      />
                      <label htmlFor="consent" className="text-white/80 text-sm leading-relaxed">
                        {language === 'fr' 
                          ? 'J\'accepte que mes documents d\'identité soient utilisés uniquement à des fins de vérification KYC et qu\'ils soient traités conformément à la réglementation en vigueur sur la protection des données.'
                          : 'I agree that my identity documents will be used solely for KYC verification purposes and processed in accordance with applicable data protection regulations.'
                        }
                      </label>
                    </div>
                  </div>

                  <div className="pt-6">
                    <Button
                      type="submit"
                      className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white py-6 rounded-full font-semibold text-lg"
                    >
                      {language === 'fr' ? 'Soumettre ma demande KYC' : 'Submit my KYC request'}
                    </Button>
                  </div>
                </form>
              )}
            </div>
          </TabsContent>

          {/* Settings Tab */}
          <TabsContent value="settings">
            <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
              <h2 className="text-2xl font-bold text-white mb-6">
                {language === 'fr' ? 'Paramètres du compte' : 'Account Settings'}
              </h2>

              {/* Account Info */}
              <div className="mb-8 p-6 bg-purple-500/10 rounded-xl">
                <h3 className="text-lg font-semibold text-white mb-4">
                  {language === 'fr' ? 'Informations du compte' : 'Account Information'}
                </h3>
                <div className="space-y-2 text-white/80">
                  <p><strong>{language === 'fr' ? 'Email :' : 'Email:'}</strong> {user?.email}</p>
                  <p><strong>{language === 'fr' ? 'Nom :' : 'Name:'}</strong> {user?.firstName} {user?.lastName}</p>
                  <p><strong>{language === 'fr' ? 'Statut KYC :' : 'KYC Status:'}</strong> {user?.kycStatus}</p>
                </div>
              </div>

              {/* Delete Account Section */}
              <div className="bg-red-500/10 border border-red-500/30 rounded-xl p-6">
                <div className="flex items-start space-x-4">
                  <div className="w-12 h-12 bg-red-500/20 rounded-full flex items-center justify-center flex-shrink-0">
                    <Trash2 className="w-6 h-6 text-red-400" />
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-2">
                      {language === 'fr' ? 'Zone de danger' : 'Danger Zone'}
                    </h3>
                    <p className="text-white/70 mb-4">
                      {language === 'fr' 
                        ? 'La suppression de votre compte est permanente et irréversible. Toutes vos données seront définitivement supprimées, y compris :'
                        : 'Account deletion is permanent and irreversible. All your data will be permanently deleted, including:'
                      }
                    </p>
                    <ul className="list-disc list-inside text-white/70 mb-4 space-y-1">
                      <li>{language === 'fr' ? 'Informations personnelles' : 'Personal information'}</li>
                      <li>{language === 'fr' ? 'Documents KYC' : 'KYC documents'}</li>
                      <li>{language === 'fr' ? 'Historique d\'achats' : 'Purchase history'}</li>
                      <li>{language === 'fr' ? 'Accès aux formations' : 'Access to training courses'}</li>
                      <li>{language === 'fr' ? 'Témoignages' : 'Testimonials'}</li>
                    </ul>
                    <Button
                      onClick={() => setShowDeleteDialog(true)}
                      className="bg-red-500 hover:bg-red-600 text-white"
                    >
                      <Trash2 className="w-4 h-4 mr-2" />
                      {language === 'fr' ? 'Supprimer mon compte' : 'Delete my account'}
                    </Button>
                  </div>
                </div>
              </div>
            </div>
          </TabsContent>
        </Tabs>

        {/* Delete Account Confirmation Dialog */}
        <Dialog open={showDeleteDialog} onOpenChange={setShowDeleteDialog}>
          <DialogContent className="bg-[#1E1540] border-red-500/30">
            <DialogHeader>
              <DialogTitle className="text-2xl font-bold text-white flex items-center">
                <Trash2 className="w-6 h-6 text-red-400 mr-2" />
                {language === 'fr' ? 'Confirmer la suppression' : 'Confirm Deletion'}
              </DialogTitle>
              <DialogDescription className="text-white/70 space-y-4 pt-4">
                <p className="font-semibold text-yellow-400">
                  {language === 'fr' 
                    ? '⚠️ ATTENTION : Cette action est irréversible !'
                    : '⚠️ WARNING: This action is irreversible!'
                  }
                </p>
                <p>
                  {language === 'fr'
                    ? 'Vous êtes sur le point de supprimer définitivement votre compte et toutes vos données. Cette action ne peut pas être annulée.'
                    : 'You are about to permanently delete your account and all your data. This action cannot be undone.'
                  }
                </p>
                <p>
                  {language === 'fr'
                    ? `Pour confirmer, veuillez taper "SUPPRIMER" ci-dessous :`
                    : `To confirm, please type "DELETE" below:`
                  }
                </p>
                <Input
                  value={deleteConfirmation}
                  onChange={(e) => setDeleteConfirmation(e.target.value)}
                  placeholder={language === 'fr' ? 'Tapez SUPPRIMER' : 'Type DELETE'}
                  className="bg-white/10 border-red-500/30 text-white placeholder:text-white/50"
                />
                <div className="flex space-x-3 pt-4">
                  <Button
                    onClick={() => {
                      setShowDeleteDialog(false);
                      setDeleteConfirmation('');
                    }}
                    variant="outline"
                    className="flex-1 border-purple-500/30 text-white hover:bg-purple-500/20"
                  >
                    {language === 'fr' ? 'Annuler' : 'Cancel'}
                  </Button>
                  <Button
                    onClick={handleDeleteAccount}
                    disabled={isDeleting}
                    className="flex-1 bg-red-500 hover:bg-red-600 text-white"
                  >
                    {isDeleting 
                      ? (language === 'fr' ? 'Suppression...' : 'Deleting...')
                      : (language === 'fr' ? 'Supprimer définitivement' : 'Delete permanently')
                    }
                  </Button>
                </div>
              </DialogDescription>
            </DialogHeader>
          </DialogContent>
        </Dialog>
      </div>
    </div>
  );
};

export default Dashboard;