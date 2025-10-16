export const translations = {
  fr: {
    // Navigation
    nav: {
      home: 'Accueil',
      shop: 'Boutique',
      channels: 'Nos canaux',
      applications: 'Nos applications',
      videos: 'Vidéos',
      contact: 'Contact',
      login: 'Connexion',
      dashboard: 'Tableau de bord',
      admin: 'Admin',
      logout: 'Déconnexion'
    },

    // Home Page
    home: {
      hero: {
        title: 'Maîtrisez les Marchés Financiers',
        subtitle: 'Formations de trading professionnelles et signaux VIP exclusifs',
        cta: 'Découvrir nos formations'
      },
      stats: {
        students: 'Étudiants Actifs',
        accuracy: 'Taux de Réussite',
        signals: 'Signaux par Jour',
        support: 'Support 24/7'
      },
      features: {
        title: 'Pourquoi Choisir Tradalife ?',
        training: {
          title: 'Formations Complètes',
          description: 'Des cours structurés du niveau débutant au niveau expert'
        },
        signals: {
          title: 'Signaux VIP',
          description: 'Accès à nos canaux Telegram avec signaux en temps réel'
        },
        support: {
          title: 'Support Personnalisé',
          description: 'Accompagnement WhatsApp privé pour tous nos membres'
        },
        accounts: {
          title: 'Comptes de Trading',
          description: 'Comptes live et demo inclus avec vos formations'
        }
      },
      videos: {
        title: 'Vidéos de Présentation',
        subtitle: 'Découvrez nos méthodes et stratégies de trading',
        watchNow: 'Regarder maintenant'
      },
      cta: {
        title: 'Prêt à Commencer Votre Parcours de Trading ?',
        subtitle: 'Rejoignez des milliers de traders qui ont transformé leur vie financière',
        button: 'Voir les Formations'
      }
    },

    // Shop Page
    shop: {
      title: 'Nos Formations',
      subtitle: 'Choisissez la formation adaptée à vos objectifs',
      includes: 'Ce qui est inclus :',
      benefits: {
        videos: 'Vidéos de formation complètes',
        telegram: 'Accès aux canaux Telegram VIP',
        accounts: 'Comptes de trading inclus',
        support: 'Support WhatsApp privé',
        copytrading: 'Formation au copytrading'
      },
      buy: 'Acheter maintenant',
      perMonth: '/mois'
    },

    // Formations
    formations: {
      'Formation Complète de Trading': {
        title: 'Formation Complète de Trading',
        description: 'Vous souhaitez apprendre le trading de manière simple, progressive et efficace ? Ce cours en ligne — composé de 10 modules vidéo — est conçu pour vous guider pas à pas, que vous soyez totalement débutant ou que vous ayez déjà quelques bases. Vous commencerez par comprendre les fondamentaux du copy trading, puis passerez au trading quotidien, à la prise de position indépendante, et enfin au scalping, une méthode de trading rapide et précise. ✅ Ce Que Vous Allez Apprendre : Comprendre le fonctionnement des marchés financiers, identifier les risques et apprendre à les gérer, découvrir les principaux indicateurs et stratégies utilisés par les traders, passer de la théorie à la pratique avec des exemples concrets, maîtriser le scalping et apprendre à profiter des tendances. 📚 Contenu du Cours : Modules 1-10 couvrant les Bases du Trading, Risques, Profits, Pips, Indicateurs, Méthodes, Scalping, Analyse des Tendances, Actifs et Plateformes.'
      },
      'Tradalife Ultra Adhésion': {
        title: 'Adhésion ULTRA Tradalife',
        description: '🔥 Adhésion ULTRA TRADALIFE - Accès à 6 Canaux VIP : Signaux et stratégies Gold, Matières premières (pétrole, gaz, matières premières), Forex (paires majeures et exotiques), Indices (S&P 500, Nasdaq, DAX), Opportunités Crypto sur Bitcoin, et signaux Actions. Comptes de trading inclus : 2 Comptes Live chez 2 courtiers différents pour diversifier vos stratégies, 1 Compte Demo pour pratiquer sans risque. Formation de base en Copytrading pour comprendre la logique, gérer les risques et copier les positions efficacement. Support privé via WhatsApp avec assistance personnalisée directe, réponses rapides et conseils pratiques pour progresser.'
      },
      'Tradalife Premium Membership': {
        title: 'Adhésion Premium Tradalife',
        description: 'Adhésion Premium TRADALIFE - Accès à 5 Canaux VIP : Signaux et stratégies Gold, Matières premières (pétrole, gaz, matières premières), Forex (paires majeures et exotiques), Indices (S&P 500, Nasdaq, DAX), et opportunités Crypto sur Bitcoin et principales cryptomonnaies. Comptes de Trading Inclus : 1 Compte Live pour trader en conditions réelles de marché, 1 Compte Demo pour pratiquer en toute sécurité sans risque financier. Formation de Base au Copy Trading pour comprendre le fonctionnement du copy trading, apprendre la gestion des risques et maîtriser la copie efficace des transactions. Support Privé via WhatsApp avec assistance personnalisée directe, réponses rapides et conseils pratiques pour vous aider à progresser.'
      }
    },

    // Login/Register
    auth: {
      login: {
        title: 'Connexion',
        subtitle: 'Accédez à votre espace membre',
        email: 'Adresse email',
        password: 'Mot de passe',
        button: 'Se connecter',
        noAccount: "Pas encore de compte ?",
        register: 'Créer un compte',
        success: 'Connexion réussie !',
        error: 'Email ou mot de passe incorrect'
      },
      register: {
        title: 'Créer un compte',
        subtitle: 'Rejoignez la communauté Tradalife',
        email: 'Adresse email',
        password: 'Mot de passe',
        confirmPassword: 'Confirmer le mot de passe',
        button: "S'inscrire",
        hasAccount: 'Déjà un compte ?',
        login: 'Se connecter',
        success: 'Compte créé avec succès !',
        error: 'Erreur lors de la création du compte',
        passwordMismatch: 'Les mots de passe ne correspondent pas'
      }
    },

    // Checkout
    checkout: {
      title: 'Finaliser l\'achat',
      summary: 'Résumé de la commande',
      price: 'Prix',
      paymentMethod: 'Méthode de paiement',
      card: 'Carte bancaire (Stripe)',
      paypal: 'PayPal',
      note: 'Note importante :',
      noteText: 'Après le paiement, vous recevrez un email de confirmation. Vous devrez ensuite compléter votre KYC (vérification d\'identité) pour accéder à vos formations et aux canaux Telegram VIP.',
      pay: 'Payer',
      processing: 'Traitement en cours...',
      secure: 'Paiement sécurisé et crypté',
      success: 'Paiement réussi !',
      successMessage: 'Vous recevrez un email de confirmation. Veuillez compléter votre KYC pour accéder aux formations.',
      error: 'Erreur de paiement',
      errorMessage: 'Une erreur est survenue'
    },

    // Dashboard
    dashboard: {
      title: 'Tableau de Bord',
      welcome: 'Bienvenue',
      myFormations: 'Mes Formations',
      noFormations: 'Aucune formation achetée pour le moment.',
      shopButton: 'Découvrir nos formations',
      kyc: {
        title: 'Vérification KYC',
        status: 'Statut',
        pending: 'En attente de vérification',
        approved: 'Approuvé',
        rejected: 'Rejeté',
        notSubmitted: 'Non soumis',
        submit: 'Soumettre mon KYC',
        resubmit: 'Soumettre à nouveau',
        documents: 'Documents requis',
        passport: 'Passeport',
        idCard: 'Carte d\'identité (recto-verso)',
        residence: 'Justificatif de domicile',
        driving: 'Permis de conduire (optionnel)',
        uploading: 'Envoi en cours...',
        success: 'KYC soumis avec succès !',
        successMessage: 'Votre KYC sera examiné sous 24-48h.',
        error: 'Erreur lors de la soumission'
      },
      access: {
        title: 'Vos Accès',
        videos: 'Vidéos de Formation',
        telegram: 'Canaux Telegram VIP',
        video1: 'Vidéo de Formation',
        video2: 'Utilisation de MT4',
        open: 'Ouvrir',
        join: 'Rejoindre'
      }
    },

    // Admin
    admin: {
      title: 'Administration',
      kycReview: 'Révision des KYC',
      userId: 'ID Utilisateur',
      email: 'Email',
      status: 'Statut',
      documents: 'Documents',
      actions: 'Actions',
      approve: 'Approuver',
      reject: 'Rejeter',
      view: 'Voir',
      reason: 'Raison du rejet',
      reasonPlaceholder: 'Entrez la raison du rejet...',
      noKYC: 'Aucun KYC en attente',
      approveSuccess: 'KYC approuvé avec succès',
      rejectSuccess: 'KYC rejeté',
      error: 'Une erreur est survenue'
    },

    // Footer
    footer: {
      description: 'Votre partenaire de confiance pour le trading professionnel',
      quickLinks: 'Liens Rapides',
      contact: 'Contact',
      support: 'Support',
      rights: 'Tous droits réservés'
    },

    // Common
    common: {
      loading: 'Chargement...',
      error: 'Erreur',
      success: 'Succès',
      close: 'Fermer',
      cancel: 'Annuler',
      confirm: 'Confirmer',
      save: 'Enregistrer',
      delete: 'Supprimer',
      edit: 'Modifier',
      back: 'Retour',
      next: 'Suivant'
    }
  },

  en: {
    // Navigation
    nav: {
      home: 'Home',
      shop: 'Shop',
      channels: 'Our Channels',
      applications: 'Our Apps',
      videos: 'Videos',
      contact: 'Contact',
      login: 'Login',
      dashboard: 'Dashboard',
      admin: 'Admin',
      logout: 'Logout'
    },

    // Home Page
    home: {
      hero: {
        title: 'Master Financial Markets',
        subtitle: 'Professional trading courses and exclusive VIP signals',
        cta: 'Explore Our Courses'
      },
      stats: {
        students: 'Active Students',
        accuracy: 'Success Rate',
        signals: 'Signals Per Day',
        support: '24/7 Support'
      },
      features: {
        title: 'Why Choose Tradalife?',
        training: {
          title: 'Complete Training',
          description: 'Structured courses from beginner to expert level'
        },
        signals: {
          title: 'VIP Signals',
          description: 'Access to our Telegram channels with real-time signals'
        },
        support: {
          title: 'Personalized Support',
          description: 'Private WhatsApp support for all our members'
        },
        accounts: {
          title: 'Trading Accounts',
          description: 'Live and demo accounts included with your courses'
        }
      },
      videos: {
        title: 'Presentation Videos',
        subtitle: 'Discover our trading methods and strategies',
        watchNow: 'Watch now'
      },
      cta: {
        title: 'Ready to Start Your Trading Journey?',
        subtitle: 'Join thousands of traders who have transformed their financial lives',
        button: 'View Courses'
      }
    },

    // Shop Page
    shop: {
      title: 'Our Courses',
      subtitle: 'Choose the course that fits your goals',
      includes: 'What\'s included:',
      benefits: {
        videos: 'Complete training videos',
        telegram: 'Access to VIP Telegram channels',
        accounts: 'Trading accounts included',
        support: 'Private WhatsApp support',
        copytrading: 'Copy trading training'
      },
      buy: 'Buy now',
      perMonth: '/month'
    },

    // Formations
    formations: {
      'Formation Complète de Trading': {
        title: 'Complete Trading Course',
        description: 'Would you like to learn trading in a simple, gradual, and effective way? This online course — made up of 10 video modules — is designed to guide you step by step, whether you are a complete beginner or already have some experience. You will start by understanding the basics of copy trading, then move on to daily trading, independent position taking, and finally scalping, a fast and precise trading method. ✅ What You Will Learn: Understand how financial markets work, identify risks and learn how to manage them, discover the main indicators and strategies used by traders, move from theory to practice with concrete examples, master scalping and learn to profit from trends. 📚 Course Content: Module 1-10 covering Trading Basics, Risks, Profits, Pips, Indicators, Methods, Scalping, Trend Analysis, Assets, and Platforms.'
      },
      'Tradalife Ultra Adhésion': {
        title: 'Tradalife ULTRA Membership',
        description: '🔥 ULTRA TRADALIFE Membership - Access to 6 VIP Channels: Gold signals and strategies, Commodities (oil, gas, raw materials), Forex (major and exotic pairs), Indices (S&P 500, Nasdaq, DAX), Crypto opportunities on Bitcoin, and Stocks signals. Trading accounts included: 2 Live Accounts at 2 different brokers to diversify your strategies, 1 Demo Account to practice without risk. Basic training in Copytrading to understand the logic, manage risks, and copy positions effectively. Private support via WhatsApp with direct personalized assistance, quick answers, and practical advice for progress.'
      },
      'Tradalife Premium Membership': {
        title: 'Tradalife Premium Membership',
        description: 'TRADALIFE Premium Membership - Access to 5 VIP Channels: Gold signals and strategies, Commodities (oil, gas, raw materials), Forex (major and exotic pairs), Indices (S&P 500, Nasdaq, DAX), and Crypto opportunities on Bitcoin and major cryptocurrencies. Included Trading Accounts: 1 Live Account to trade in real market conditions, 1 Demo Account to practice safely without financial risk. Basic Copy Trading Training to understand how copy trading works, learn risk management, and master efficient trade copying. Private Support via WhatsApp with direct personalized assistance, quick responses, and practical advice to help you progress.'
      }
    },

    // Login/Register
    auth: {
      login: {
        title: 'Login',
        subtitle: 'Access your member area',
        email: 'Email address',
        password: 'Password',
        button: 'Sign in',
        noAccount: "Don't have an account?",
        register: 'Create account',
        success: 'Login successful!',
        error: 'Incorrect email or password'
      },
      register: {
        title: 'Create Account',
        subtitle: 'Join the Tradalife community',
        email: 'Email address',
        password: 'Password',
        confirmPassword: 'Confirm password',
        button: 'Sign up',
        hasAccount: 'Already have an account?',
        login: 'Sign in',
        success: 'Account created successfully!',
        error: 'Error creating account',
        passwordMismatch: 'Passwords do not match'
      }
    },

    // Checkout
    checkout: {
      title: 'Complete Purchase',
      summary: 'Order Summary',
      price: 'Price',
      paymentMethod: 'Payment Method',
      card: 'Credit Card (Stripe)',
      paypal: 'PayPal',
      note: 'Important note:',
      noteText: 'After payment, you will receive a confirmation email. You will then need to complete your KYC (identity verification) to access your courses and VIP Telegram channels.',
      pay: 'Pay',
      processing: 'Processing...',
      secure: 'Secure and encrypted payment',
      success: 'Payment successful!',
      successMessage: 'You will receive a confirmation email. Please complete your KYC to access the courses.',
      error: 'Payment error',
      errorMessage: 'An error occurred'
    },

    // Dashboard
    dashboard: {
      title: 'Dashboard',
      welcome: 'Welcome',
      myFormations: 'My Courses',
      noFormations: 'No courses purchased yet.',
      shopButton: 'Explore our courses',
      kyc: {
        title: 'KYC Verification',
        status: 'Status',
        pending: 'Pending verification',
        approved: 'Approved',
        rejected: 'Rejected',
        notSubmitted: 'Not submitted',
        submit: 'Submit my KYC',
        resubmit: 'Submit again',
        documents: 'Required documents',
        passport: 'Passport',
        idCard: 'ID Card (front and back)',
        residence: 'Proof of residence',
        driving: 'Driver\'s license (optional)',
        uploading: 'Uploading...',
        success: 'KYC submitted successfully!',
        successMessage: 'Your KYC will be reviewed within 24-48h.',
        error: 'Error submitting'
      },
      access: {
        title: 'Your Access',
        videos: 'Training Videos',
        telegram: 'VIP Telegram Channels',
        video1: 'Training Video',
        video2: 'MT4 Usage',
        open: 'Open',
        join: 'Join'
      }
    },

    // Admin
    admin: {
      title: 'Administration',
      kycReview: 'KYC Review',
      userId: 'User ID',
      email: 'Email',
      status: 'Status',
      documents: 'Documents',
      actions: 'Actions',
      approve: 'Approve',
      reject: 'Reject',
      view: 'View',
      reason: 'Rejection reason',
      reasonPlaceholder: 'Enter rejection reason...',
      noKYC: 'No pending KYC',
      approveSuccess: 'KYC approved successfully',
      rejectSuccess: 'KYC rejected',
      error: 'An error occurred'
    },

    // Footer
    footer: {
      description: 'Your trusted partner for professional trading',
      quickLinks: 'Quick Links',
      contact: 'Contact',
      support: 'Support',
      rights: 'All rights reserved'
    },

    // Common
    common: {
      loading: 'Loading...',
      error: 'Error',
      success: 'Success',
      close: 'Close',
      cancel: 'Cancel',
      confirm: 'Confirm',
      save: 'Save',
      delete: 'Delete',
      edit: 'Edit',
      back: 'Back',
      next: 'Next'
    }
  }
};

// Helper function to get translation
export const t = (language, key) => {
  const keys = key.split('.');
  let value = translations[language];
  
  for (const k of keys) {
    if (value && typeof value === 'object') {
      value = value[k];
    } else {
      return key; // Return key if translation not found
    }
  }
  
  return value || key;
};
