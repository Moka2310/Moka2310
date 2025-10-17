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
        description: `💎 Formation complète : 8h - 10 vidéos - Avancé

✨ Ce Que Vous Allez Apprendre :

✓ Comprendre le fonctionnement des marchés financiers
✓ Identifier les risques et apprendre à les gérer
✓ Découvrir les principaux indicateurs et stratégies
✓ Passer de la théorie à la pratique avec des exemples concrets
✓ Maîtriser le scalping et profiter des tendances

📚 Contenu Complet :

• Modules 1-10 : Bases du Trading
• Gestion des Risques et Profits
• Analyse des Pips et Indicateurs
• Méthodes de Trading Avancées
• Scalping et Analyse des Tendances
• Choix des Actifs et Plateformes`
      },
      'Tradalife Ultra Adhésion': {
        title: 'Adhésion ULTRA Tradalife',
        description: `💎 Formation : 1h40 min - 2 vidéos - Débutant

🔥 Accès à 6 Canaux VIP :

✓ Signaux et stratégies Gold
✓ Matières premières (pétrole, gaz)
✓ Forex (paires majeures et exotiques)
✓ Indices (S&P 500, Nasdaq, DAX)
✓ Opportunités Crypto sur Bitcoin
✓ Signaux Actions

💼 Comptes de Trading Inclus :

• 2 Comptes Live chez 2 courtiers différents
• 1 Compte Demo pour pratiquer sans risque

📖 Formation Copytrading :

• Comprendre la logique du copytrading
• Gérer les risques efficacement
• Copier les positions comme un pro

📱 Support Privé WhatsApp :

• Assistance personnalisée directe
• Réponses rapides à vos questions
• Conseils pratiques pour progresser`
      },
      'Tradalife Premium Membership': {
        title: 'Adhésion Premium Tradalife',
        description: `💎 Formation : 1h40 - 2 vidéos - Débutant

⭐ Accès à 5 Canaux VIP :

✓ Signaux et stratégies Gold
✓ Matières premières (pétrole, gaz)
✓ Forex (paires majeures et exotiques)
✓ Indices (S&P 500, Nasdaq, DAX)
✓ Opportunités Crypto Bitcoin

💼 Comptes de Trading Inclus :

• 1 Compte Live pour trader en réel
• 1 Compte Demo pour pratiquer sans risque

📖 Formation Copy Trading :

• Comprendre le fonctionnement
• Apprendre la gestion des risques
• Maîtriser la copie des transactions

📱 Support Privé WhatsApp :

• Assistance personnalisée directe
• Réponses rapides
• Conseils pratiques`
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
        description: `💎 Complete course: 8h - 10 videos - Advanced

✨ What You Will Learn:

✓ Understand how financial markets work
✓ Identify risks and learn to manage them
✓ Discover main indicators and strategies
✓ Move from theory to practice with examples
✓ Master scalping and profit from trends

📚 Complete Content:

• Modules 1-10: Trading Basics
• Risk and Profit Management
• Pips Analysis and Indicators
• Advanced Trading Methods
• Scalping and Trend Analysis
• Assets and Platforms Selection`
      },
      'Tradalife Ultra Adhésion': {
        title: 'Tradalife ULTRA Membership',
        description: `💎 Course: 1h40 min - 2 videos - Beginner

🔥 Access to 6 VIP Channels:

✓ Gold signals and strategies
✓ Commodities (oil, gas)
✓ Forex (major and exotic pairs)
✓ Indices (S&P 500, Nasdaq, DAX)
✓ Crypto opportunities on Bitcoin
✓ Stocks signals

💼 Trading Accounts Included:

• 2 Live Accounts at 2 different brokers
• 1 Demo Account to practice risk-free

📖 Copytrading Training:

• Understand copytrading logic
• Manage risks effectively
• Copy positions like a pro

📱 Private WhatsApp Support:

• Direct personalized assistance
• Quick answers to your questions
• Practical advice for progress`
      },
      'Tradalife Premium Membership': {
        title: 'Tradalife Premium Membership',
        description: `💎 Course: 1h40 - 2 videos - Beginner

⭐ Access to 5 VIP Channels:

✓ Gold signals and strategies
✓ Commodities (oil, gas)
✓ Forex (major and exotic pairs)
✓ Indices (S&P 500, Nasdaq, DAX)
✓ Crypto Bitcoin opportunities

💼 Trading Accounts Included:

• 1 Live Account to trade for real
• 1 Demo Account to practice risk-free

📖 Copy Trading Training:

• Understand how it works
• Learn risk management
• Master trade copying

📱 Private WhatsApp Support:

• Direct personalized assistance
• Quick responses
• Practical advice`
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
