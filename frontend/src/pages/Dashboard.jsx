import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { t, translations } from '../translations';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
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
  Star,
  X,
  Zap,
  Bot
} from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from '../components/ui/dialog';
import SubscriptionSection from '../components/SubscriptionSection';

const Dashboard = () => {
  const { user, logout, updateUser } = useAuth();
  const { language } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();
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
  const [documentPreviews, setDocumentPreviews] = useState({
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
  const [hiddenFormations, setHiddenFormations] = useState([]);

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
      loadMyTestimonial();
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
      const response = await kycAPI.submit(formData);

      // Force refresh user data from server
      await updateUser();
      
      // Reload page to refresh all data
      setTimeout(() => {
        window.location.reload();
      }, 1000);

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
      // Validation de la taille (max 10 MB)
      const maxSize = 10 * 1024 * 1024; // 10 MB
      if (file.size > maxSize) {
        toast({
          title: language === 'fr' ? '❌ Fichier trop volumineux' : '❌ File too large',
          description: language === 'fr' 
            ? 'La taille maximale est de 10 MB. Veuillez compresser votre image.'
            : 'Maximum size is 10 MB. Please compress your image.',
          variant: 'destructive'
        });
        return;
      }

      // Validation du type
      const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf'];
      if (!allowedTypes.includes(file.type)) {
        toast({
          title: language === 'fr' ? '❌ Format invalide' : '❌ Invalid format',
          description: language === 'fr' 
            ? 'Formats acceptés : JPG, PNG, PDF uniquement'
            : 'Accepted formats: JPG, PNG, PDF only',
          variant: 'destructive'
        });
        return;
      }

      setDocuments(prev => ({ ...prev, [docType]: file }));
      
      // Créer une prévisualisation pour les images
      if (file.type.startsWith('image/')) {
        const reader = new FileReader();
        reader.onloadend = () => {
          setDocumentPreviews(prev => ({ ...prev, [docType]: reader.result }));
        };
        reader.readAsDataURL(file);
      } else {
        // Pour les PDF, pas de prévisualisation
        setDocumentPreviews(prev => ({ ...prev, [docType]: 'pdf' }));
      }
      
      toast({
        title: language === 'fr' ? '✓ Document ajouté' : '✓ Document added',
        description: language === 'fr' 
          ? `${file.name} - Assurez-vous que la photo est nette et bien cadrée`
          : `${file.name} - Make sure the photo is sharp and well-framed`
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

        {/* TRADABOT Button */}
        <div className="mb-8">
          <button
            onClick={() => navigate('/tradabot-demo')}
            className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white p-6 rounded-3xl border-2 border-green-400/50 hover:border-green-400 transition-all shadow-lg hover:shadow-green-500/50 flex items-center justify-center gap-4 group"
          >
            <Bot className="w-8 h-8 group-hover:scale-110 transition-transform" />
            <div className="text-left">
              <div className="text-2xl font-bold">TRADABOT - MODE DÉMO</div>
              <div className="text-sm text-white/90">
                {language === 'fr' ? '🎮 Tester maintenant (simulation)' : '🎮 Test Now (simulation)'}
              </div>
            </div>
            <ExternalLink className="w-6 h-6 ml-auto" />
          </button>
        </div>

        {/* Tabs */}
        <Tabs defaultValue={new URLSearchParams(location.search).get('tab') || 'formations'} className="w-full">
          <TabsList className="bg-[#2B1F5C] border border-purple-500/30 p-1 mb-8 grid grid-cols-2 sm:grid-cols-5 gap-1">
            <TabsTrigger 
              value="formations"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white text-xs sm:text-sm"
            >
              <Video className="w-4 h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">{t(language, 'dashboard.myFormations')}</span>
              <span className="sm:hidden">Formations</span>
            </TabsTrigger>
            <TabsTrigger 
              value="subscription"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white text-xs sm:text-sm"
            >
              <Zap className="w-4 h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">{language === 'fr' ? 'Abonnement' : 'Subscription'}</span>
              <span className="sm:hidden">Abonnement</span>
            </TabsTrigger>
            <TabsTrigger 
              value="kyc"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white text-xs sm:text-sm"
            >
              <User className="w-4 h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">{t(language, 'dashboard.kyc.title')}</span>
              <span className="sm:hidden">KYC</span>
            </TabsTrigger>
            <TabsTrigger 
              value="testimonial"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white text-xs sm:text-sm"
            >
              <Star className="w-4 h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">{language === 'fr' ? 'Témoignage' : 'Testimonial'}</span>
              <span className="sm:hidden">Avis</span>
            </TabsTrigger>
            <TabsTrigger 
              value="settings"
              className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-pink-500 data-[state=active]:to-purple-600 data-[state=active]:text-white text-xs sm:text-sm"
            >
              <Settings className="w-4 h-4 mr-1 sm:mr-2" />
              <span className="hidden sm:inline">{language === 'fr' ? 'Paramètres' : 'Settings'}</span>
              <span className="sm:hidden">Réglages</span>
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
                {/* Bouton pour acheter plus de formations */}
                <div className="flex justify-end">
                  <Button
                    onClick={() => navigate('/boutique')}
                    className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-6 py-3 rounded-full"
                  >
                    🛒 {language === 'fr' ? 'Acheter une Formation' : 'Buy a Course'}
                  </Button>
                </div>

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
                  {purchasedFormations
                    .filter(formation => !hiddenFormations.includes(formation.id))
                    .map((formation) => {
                    // Get translated formation title
                    const translatedTitle = translations[language]?.formations?.[formation.title]?.title || formation.title;
                    
                    return (
                    <div
                      key={formation.id}
                      className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl overflow-hidden border border-purple-500/30 relative"
                    >
                      {/* Hide button */}
                      <button
                        onClick={() => {
                          if (window.confirm(language === 'fr' ? 'Masquer cette formation de votre liste ?' : 'Hide this course from your list?')) {
                            setHiddenFormations([...hiddenFormations, formation.id]);
                            toast({
                              title: language === 'fr' ? 'Formation masquée' : 'Course hidden',
                              description: language === 'fr' ? 'Rechargez la page pour la voir à nouveau' : 'Reload the page to see it again'
                            });
                          }
                        }}
                        className="absolute top-2 right-2 z-10 w-8 h-8 bg-red-500/80 hover:bg-red-600 rounded-full flex items-center justify-center text-white transition-all"
                      >
                        <X className="w-5 h-5" />
                      </button>
                      
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

          {/* Subscription Tab */}
          <TabsContent value="subscription">
            <SubscriptionSection user={user} />
          </TabsContent>

          {/* KYC Tab */}
          <TabsContent value="kyc">
            <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
              <h2 className="text-3xl font-bold text-white mb-6">
                {language === 'fr' ? 'Vérification d\'identité (KYC)' : 'Identity Verification (KYC)'}
              </h2>
              
              {user?.kycStatus === 'approved' ? (
                <div className="text-center py-12 bg-green-500/10 border-2 border-green-500/50 rounded-2xl">
                  <CheckCircle className="w-20 h-20 text-green-400 mx-auto mb-4" />
                  <h3 className="text-3xl font-bold text-green-400 mb-2">
                    ✓ {language === 'fr' ? 'Compte Approuvé' : 'Account Approved'}
                  </h3>
                  <p className="text-white/80 text-lg">
                    {language === 'fr' 
                      ? 'Votre identité a été vérifiée avec succès. Vous pouvez maintenant acheter des formations !'
                      : 'Your identity has been successfully verified. You can now purchase courses!'
                    }
                  </p>
                </div>
              ) : user?.kycStatus === 'pending' && user?.kycSubmittedAt ? (
                <div className="space-y-6">
                  <div className="text-center py-8 bg-yellow-500/10 border-2 border-yellow-500/50 rounded-2xl">
                    <Clock className="w-16 h-16 text-yellow-400 mx-auto mb-4 animate-pulse" />
                    <h3 className="text-2xl font-bold text-yellow-400 mb-2">
                      ⏳ {language === 'fr' ? 'Documents en cours de vérification' : 'Documents under review'}
                    </h3>
                    <p className="text-white/80">
                      {language === 'fr' 
                        ? 'Vous pouvez déjà acheter des formations. Si vos documents sont rejetés, vous devrez en soumettre de nouveaux.'
                        : 'You can already purchase courses. If your documents are rejected, you will need to submit new ones.'
                      }
                    </p>
                  </div>
                  
                  {/* Show uploaded documents summary */}
                  <div className="bg-purple-500/10 rounded-xl p-6">
                    <h4 className="text-white font-semibold mb-3">
                      {language === 'fr' ? '📄 Documents soumis' : '📄 Submitted documents'}
                    </h4>
                    <ul className="text-white/70 space-y-2">
                      <li>✓ {language === 'fr' ? 'Passeport' : 'Passport'}</li>
                      <li>✓ {language === 'fr' ? 'Carte d\'identité' : 'ID Card'}</li>
                      <li>✓ {language === 'fr' ? 'Justificatif de domicile' : 'Proof of residence'}</li>
                    </ul>
                  </div>
                </div>
              ) : user?.kycStatus === 'rejected' ? (
                <div className="text-center py-12 bg-red-500/10 border-2 border-red-500/50 rounded-2xl mb-6">
                  <XCircle className="w-20 h-20 text-red-400 mx-auto mb-4" />
                  <h3 className="text-3xl font-bold text-red-400 mb-2">
                    ✗ {language === 'fr' ? 'Documents Rejetés' : 'Documents Rejected'}
                  </h3>
                  <p className="text-white/80 text-lg mb-4">
                    {language === 'fr' 
                      ? 'Vos documents ont été rejetés. Veuillez soumettre de nouveaux documents conformes aux critères.'
                      : 'Your documents have been rejected. Please submit new documents that meet the criteria.'
                    }
                  </p>
                </div>
              ) : null}
              
              {(!user?.kycStatus || user?.kycStatus === 'rejected') && (
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
                      <select
                        required
                        value={kycData.country}
                        onChange={(e) => setKycData({ ...kycData, country: e.target.value })}
                        className="w-full bg-white/10 border border-purple-500/30 text-white rounded-lg px-4 py-3 focus:border-pink-500 focus:outline-none"
                      >
                        <option value="" className="bg-[#1E1540]">{language === 'fr' ? 'Sélectionnez un pays' : 'Select a country'}</option>
                        <option value="Canada" className="bg-[#1E1540]">Canada</option>
                        <option value="France" className="bg-[#1E1540]">France</option>
                        <option value="Belgique" className="bg-[#1E1540]">Belgique / Belgium</option>
                        <option value="Suisse" className="bg-[#1E1540]">Suisse / Switzerland</option>
                        <option value="États-Unis" className="bg-[#1E1540]">États-Unis / USA</option>
                        <option value="Maroc" className="bg-[#1E1540]">Maroc / Morocco</option>
                        <option value="Algérie" className="bg-[#1E1540]">Algérie / Algeria</option>
                        <option value="Tunisie" className="bg-[#1E1540]">Tunisie / Tunisia</option>
                        <option value="Sénégal" className="bg-[#1E1540]">Sénégal / Senegal</option>
                        <option value="Côte d'Ivoire" className="bg-[#1E1540]">Côte d'Ivoire / Ivory Coast</option>
                        <option value="Cameroun" className="bg-[#1E1540]">Cameroun / Cameroon</option>
                        <option value="Mali" className="bg-[#1E1540]">Mali</option>
                        <option value="Burkina Faso" className="bg-[#1E1540]">Burkina Faso</option>
                        <option value="Niger" className="bg-[#1E1540]">Niger</option>
                        <option value="Bénin" className="bg-[#1E1540]">Bénin / Benin</option>
                        <option value="Togo" className="bg-[#1E1540]">Togo</option>
                        <option value="Guinée" className="bg-[#1E1540]">Guinée / Guinea</option>
                        <option value="Congo" className="bg-[#1E1540]">Congo</option>
                        <option value="RDC" className="bg-[#1E1540]">RDC / DR Congo</option>
                        <option value="Gabon" className="bg-[#1E1540]">Gabon</option>
                        <option value="Madagascar" className="bg-[#1E1540]">Madagascar</option>
                        <option value="Haïti" className="bg-[#1E1540]">Haïti / Haiti</option>
                        <option value="Autre" className="bg-[#1E1540]">{language === 'fr' ? 'Autre' : 'Other'}</option>
                      </select>
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
                    
                    {/* Quality Instructions */}
                    <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-4 mb-6">
                      <h4 className="text-yellow-400 font-bold mb-2 flex items-center">
                        ⚠️ {language === 'fr' ? 'Critères de Qualité Obligatoires' : 'Mandatory Quality Criteria'}
                      </h4>
                      <ul className="text-white/80 text-sm space-y-1">
                        <li>✓ {language === 'fr' ? 'Photos bien cadrées (document entier visible)' : 'Well-framed photos (entire document visible)'}</li>
                        <li>✓ {language === 'fr' ? 'Texte parfaitement lisible et net' : 'Text perfectly readable and sharp'}</li>
                        <li>✓ {language === 'fr' ? 'Sans reflets ou effets de lumière' : 'No glare or light effects'}</li>
                        <li>✓ {language === 'fr' ? 'Format JPG, PNG ou PDF (max 10 MB)' : 'JPG, PNG or PDF format (max 10 MB)'}</li>
                        <li className="text-red-400 font-semibold">✗ {language === 'fr' ? 'Photos floues = REJET AUTOMATIQUE' : 'Blurry photos = AUTOMATIC REJECTION'}</li>
                      </ul>
                    </div>

                    {/* Passport */}
                    <div className="bg-purple-500/10 rounded-xl p-4 mb-4">
                      <label className="block text-white/80 mb-2 font-semibold">{t(language, 'dashboard.kyc.passport')}*</label>
                      <p className="text-yellow-300 text-xs mb-3">
                        📸 {language === 'fr' 
                          ? 'Photo de la page identité de votre passeport - Cadrage complet, luminosité uniforme'
                          : 'Photo of your passport identity page - Full frame, uniform lighting'
                        }
                      </p>
                      <div className="flex items-center space-x-4">
                        <label className="flex-1 cursor-pointer">
                          <div className="border-2 border-dashed border-purple-500/50 rounded-xl p-6 text-center hover:border-pink-500/50 transition-colors">
                            {documentPreviews.passport ? (
                              documentPreviews.passport === 'pdf' ? (
                                <div>
                                  <CheckCircle className="w-8 h-8 text-green-400 mx-auto mb-2" />
                                  <p className="text-green-400 text-sm font-semibold">{documents.passport.name}</p>
                                  <p className="text-white/60 text-xs mt-1">{language === 'fr' ? 'PDF téléchargé' : 'PDF uploaded'}</p>
                                </div>
                              ) : (
                                <div>
                                  <img src={documentPreviews.passport} alt="Passport preview" className="w-full h-32 object-contain rounded-lg mb-2" />
                                  <p className="text-green-400 text-sm font-semibold">{documents.passport.name}</p>
                                  <p className="text-white/60 text-xs mt-1">{language === 'fr' ? 'Cliquez pour changer' : 'Click to change'}</p>
                                </div>
                              )
                            ) : (
                              <>
                                <Upload className="w-8 h-8 text-pink-400 mx-auto mb-2" />
                                <p className="text-white/70 text-sm">{language === 'fr' ? 'Cliquez pour télécharger' : 'Click to upload'}</p>
                              </>
                            )}
                          </div>
                          <input
                            type="file"
                            accept="image/jpeg,image/png,image/jpg,application/pdf"
                            className="hidden"
                            onChange={(e) => handleFileChange(e, 'passport')}
                          />
                        </label>
                      </div>
                    </div>

                    {/* ID Card */}
                    <div className="bg-purple-500/10 rounded-xl p-4 mb-4">
                      <label className="block text-white/80 mb-2 font-semibold">{t(language, 'dashboard.kyc.idCard')}*</label>
                      <p className="text-yellow-300 text-xs mb-3">
                        📸 {language === 'fr' 
                          ? 'Recto et verso de votre carte d\'identité - Coins visibles, texte net'
                          : 'Front and back of your ID card - Corners visible, sharp text'
                        }
                      </p>
                      <div className="flex items-center space-x-4">
                        <label className="flex-1 cursor-pointer">
                          <div className="border-2 border-dashed border-purple-500/50 rounded-xl p-6 text-center hover:border-pink-500/50 transition-colors">
                            {documentPreviews.idCard ? (
                              documentPreviews.idCard === 'pdf' ? (
                                <div>
                                  <CheckCircle className="w-8 h-8 text-green-400 mx-auto mb-2" />
                                  <p className="text-green-400 text-sm font-semibold">{documents.idCard.name}</p>
                                  <p className="text-white/60 text-xs mt-1">{language === 'fr' ? 'PDF téléchargé' : 'PDF uploaded'}</p>
                                </div>
                              ) : (
                                <div>
                                  <img src={documentPreviews.idCard} alt="ID Card preview" className="w-full h-32 object-contain rounded-lg mb-2" />
                                  <p className="text-green-400 text-sm font-semibold">{documents.idCard.name}</p>
                                  <p className="text-white/60 text-xs mt-1">{language === 'fr' ? 'Cliquez pour changer' : 'Click to change'}</p>
                                </div>
                              )
                            ) : (
                              <>
                                <Upload className="w-8 h-8 text-pink-400 mx-auto mb-2" />
                                <p className="text-white/70 text-sm">{language === 'fr' ? 'Cliquez pour télécharger' : 'Click to upload'}</p>
                              </>
                            )}
                          </div>
                          <input
                            type="file"
                            accept="image/jpeg,image/png,image/jpg,application/pdf"
                            className="hidden"
                            onChange={(e) => handleFileChange(e, 'idCard')}
                          />
                        </label>
                      </div>
                    </div>

                    {/* Proof of Residence */}
                    <div className="bg-purple-500/10 rounded-xl p-4 mb-4">
                      <label className="block text-white/80 mb-2 font-semibold">{t(language, 'dashboard.kyc.residence')}*</label>
                      <p className="text-yellow-300 text-xs mb-3">
                        📸 {language === 'fr' 
                          ? 'Facture récente (< 3 mois) : électricité, eau, téléphone - Document complet visible'
                          : 'Recent bill (< 3 months): electricity, water, phone - Full document visible'
                        }
                      </p>
                      <div className="flex items-center space-x-4">
                        <label className="flex-1 cursor-pointer">
                          <div className="border-2 border-dashed border-purple-500/50 rounded-xl p-6 text-center hover:border-pink-500/50 transition-colors">
                            {documentPreviews.proofOfResidence ? (
                              documentPreviews.proofOfResidence === 'pdf' ? (
                                <div>
                                  <CheckCircle className="w-8 h-8 text-green-400 mx-auto mb-2" />
                                  <p className="text-green-400 text-sm font-semibold">{documents.proofOfResidence.name}</p>
                                  <p className="text-white/60 text-xs mt-1">{language === 'fr' ? 'PDF téléchargé' : 'PDF uploaded'}</p>
                                </div>
                              ) : (
                                <div>
                                  <img src={documentPreviews.proofOfResidence} alt="Proof of Residence preview" className="w-full h-32 object-contain rounded-lg mb-2" />
                                  <p className="text-green-400 text-sm font-semibold">{documents.proofOfResidence.name}</p>
                                  <p className="text-white/60 text-xs mt-1">{language === 'fr' ? 'Cliquez pour changer' : 'Click to change'}</p>
                                </div>
                              )
                            ) : (
                              <>
                                <Upload className="w-8 h-8 text-pink-400 mx-auto mb-2" />
                                <p className="text-white/70 text-sm">{language === 'fr' ? 'Cliquez pour télécharger' : 'Click to upload'}</p>
                              </>
                            )}
                          </div>
                          <input
                            type="file"
                            accept="image/jpeg,image/png,image/jpg,application/pdf"
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

          {/* Testimonial Tab */}
          <TabsContent value="testimonial">
            <div className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30">
              <h2 className="text-2xl font-bold text-white mb-2">
                {language === 'fr' ? 'Partagez votre expérience' : 'Share your experience'}
              </h2>
              <p className="text-white/70 mb-6">
                {language === 'fr' 
                  ? 'Votre avis compte ! Partagez votre expérience avec Tradalife.'
                  : 'Your opinion matters! Share your experience with Tradalife.'
                }
              </p>

              {myTestimonial ? (
                <div className="bg-purple-500/10 border border-purple-500/30 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-semibold text-white">
                      {language === 'fr' ? 'Votre témoignage' : 'Your testimonial'}
                    </h3>
                    <div className={`px-4 py-2 rounded-full text-sm ${
                      myTestimonial.status === 'approved' 
                        ? 'bg-green-500/20 text-green-400'
                        : myTestimonial.status === 'rejected'
                        ? 'bg-red-500/20 text-red-400'
                        : 'bg-yellow-500/20 text-yellow-400'
                    }`}>
                      {myTestimonial.status === 'approved' 
                        ? (language === 'fr' ? '✓ Approuvé' : '✓ Approved')
                        : myTestimonial.status === 'rejected'
                        ? (language === 'fr' ? '✗ Rejeté' : '✗ Rejected')
                        : (language === 'fr' ? '⏳ En attente' : '⏳ Pending')
                      }
                    </div>
                  </div>

                  <div className="flex space-x-1 mb-4">
                    {[...Array(5)].map((_, index) => (
                      <Star
                        key={index}
                        className={`w-5 h-5 ${
                          index < myTestimonial.rating
                            ? 'text-yellow-400 fill-yellow-400'
                            : 'text-gray-600'
                        }`}
                      />
                    ))}
                  </div>

                  <p className="text-white/80 mb-4 italic">"{myTestimonial.comment}"</p>
                  <p className="text-pink-400 text-sm">{myTestimonial.country}</p>
                </div>
              ) : (
                <form onSubmit={handleTestimonialSubmit} className="space-y-6">
                  {/* Rating */}
                  <div>
                    <label className="block text-white/80 mb-3 font-medium">
                      {language === 'fr' ? 'Note (étoiles)' : 'Rating (stars)'}
                    </label>
                    <div className="flex space-x-2">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          type="button"
                          onClick={() => setTestimonialData({ ...testimonialData, rating: star })}
                          className="transition-transform hover:scale-110"
                        >
                          <Star
                            className={`w-10 h-10 ${
                              star <= testimonialData.rating
                                ? 'text-yellow-400 fill-yellow-400'
                                : 'text-gray-600'
                            }`}
                          />
                        </button>
                      ))}
                    </div>
                  </div>

                  {/* Country */}
                  <div>
                    <label className="block text-white/80 mb-2 font-medium">
                      {language === 'fr' ? 'Pays' : 'Country'}
                    </label>
                    <select
                      value={testimonialData.country}
                      onChange={(e) => setTestimonialData({ ...testimonialData, country: e.target.value })}
                      className="w-full bg-white/10 border border-purple-500/30 text-white rounded-lg px-4 py-3 focus:border-pink-500 focus:outline-none"
                      required
                    >
                      <option value="" className="bg-[#1E1540]">{language === 'fr' ? 'Sélectionnez un pays' : 'Select a country'}</option>
                      <option value="Canada" className="bg-[#1E1540]">Canada</option>
                      <option value="France" className="bg-[#1E1540]">France</option>
                      <option value="Belgique" className="bg-[#1E1540]">Belgique / Belgium</option>
                      <option value="Suisse" className="bg-[#1E1540]">Suisse / Switzerland</option>
                      <option value="États-Unis" className="bg-[#1E1540]">États-Unis / USA</option>
                      <option value="Maroc" className="bg-[#1E1540]">Maroc / Morocco</option>
                      <option value="Algérie" className="bg-[#1E1540]">Algérie / Algeria</option>
                      <option value="Tunisie" className="bg-[#1E1540]">Tunisie / Tunisia</option>
                      <option value="Sénégal" className="bg-[#1E1540]">Sénégal / Senegal</option>
                      <option value="Côte d'Ivoire" className="bg-[#1E1540]">Côte d'Ivoire / Ivory Coast</option>
                      <option value="Cameroun" className="bg-[#1E1540]">Cameroun / Cameroon</option>
                      <option value="Mali" className="bg-[#1E1540]">Mali</option>
                      <option value="Burkina Faso" className="bg-[#1E1540]">Burkina Faso</option>
                      <option value="Niger" className="bg-[#1E1540]">Niger</option>
                      <option value="Bénin" className="bg-[#1E1540]">Bénin / Benin</option>
                      <option value="Togo" className="bg-[#1E1540]">Togo</option>
                      <option value="Guinée" className="bg-[#1E1540]">Guinée / Guinea</option>
                      <option value="Congo" className="bg-[#1E1540]">Congo</option>
                      <option value="Gabon" className="bg-[#1E1540]">Gabon</option>
                      <option value="Madagascar" className="bg-[#1E1540]">Madagascar</option>
                      <option value="Maurice" className="bg-[#1E1540]">Maurice / Mauritius</option>
                      <option value="Haïti" className="bg-[#1E1540]">Haïti / Haiti</option>
                      <option value="Luxembourg" className="bg-[#1E1540]">Luxembourg</option>
                      <option value="Autre" className="bg-[#1E1540]">{language === 'fr' ? 'Autre' : 'Other'}</option>
                    </select>
                  </div>

                  {/* Comment */}
                  <div>
                    <label className="block text-white/80 mb-2 font-medium">
                      {language === 'fr' ? 'Votre témoignage' : 'Your testimonial'}
                    </label>
                    <Textarea
                      value={testimonialData.comment}
                      onChange={(e) => setTestimonialData({ ...testimonialData, comment: e.target.value })}
                      placeholder={language === 'fr' ? 'Partagez votre expérience avec Tradalife...' : 'Share your experience with Tradalife...'}
                      className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 min-h-[150px]"
                      required
                    />
                  </div>

                  <Button
                    type="submit"
                    disabled={testimonialLoading}
                    className="w-full bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white py-6 rounded-full font-semibold text-lg"
                  >
                    {testimonialLoading 
                      ? (language === 'fr' ? 'Envoi...' : 'Sending...')
                      : (language === 'fr' ? 'Soumettre mon témoignage' : 'Submit my testimonial')
                    }
                  </Button>
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