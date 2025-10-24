// Traductions pour Bonus et About Us
export const bonusTranslations = {
  fr: {
    bonus: {
      title: 'Bonus',
      subtitle: 'Découvrez nos offres exclusives et actualités',
      homeSubtitle: 'Offres spéciales et nouveautés',
      noAnnouncements: 'Aucune annonce pour le moment',
      learnMore: 'En savoir plus',
      viewAll: 'Voir tout',
      allAnnouncements: 'Toutes les annonces'
    },
    aboutUs: {
      title: 'Qui sommes nous?',
      subtitle: 'Découvrez l\'équipe Tradalife',
      description: 'Tradalife est une plateforme dédiée à l\'éducation et à l\'accompagnement des traders. Notre mission est de démocratiser l\'accès aux marchés financiers en fournissant des formations de qualité, des signaux fiables et un support personnalisé.',
      mission: 'Avec des années d\'expérience dans le trading et l\'enseignement, notre équipe s\'engage à vous transmettre les compétences nécessaires pour réussir sur les marchés Forex, Crypto, Indices et plus encore.',
      vision: 'Nous croyons que le succès en trading repose sur trois piliers: la formation continue, la discipline et une communauté solide. C\'est pourquoi nous avons créé un écosystème complet pour accompagner nos membres à chaque étape de leur parcours.',
      feature1Title: 'Excellence',
      feature1Desc: 'Des formations reconnues et des signaux de qualité professionnelle',
      feature2Title: 'Résultats',
      feature2Desc: 'Plus de 3765 traders accompagnés avec des résultats concrets',
      feature3Title: 'Fiabilité',
      feature3Desc: 'Support 24/7 et transparence totale dans nos opérations'
    }
  },
  en: {
    bonus: {
      title: 'Bonus',
      subtitle: 'Discover our exclusive offers and news',
      homeSubtitle: 'Special offers and updates',
      noAnnouncements: 'No announcements at the moment',
      learnMore: 'Learn more',
      viewAll: 'View all',
      allAnnouncements: 'All announcements'
    },
    aboutUs: {
      title: 'About Us',
      subtitle: 'Meet the Tradalife team',
      description: 'Tradalife is a platform dedicated to trader education and support. Our mission is to democratize access to financial markets by providing quality training, reliable signals and personalized support.',
      mission: 'With years of experience in trading and teaching, our team is committed to providing you with the skills you need to succeed in Forex, Crypto, Indices and more.',
      vision: 'We believe that success in trading is based on three pillars: continuous training, discipline and a strong community. That\'s why we created a complete ecosystem to support our members at every step of their journey.',
      feature1Title: 'Excellence',
      feature1Desc: 'Recognized training and professional-quality signals',
      feature2Title: 'Results',
      feature2Desc: 'Over 3,765 traders supported with concrete results',
      feature3Title: 'Reliability',
      feature3Desc: '24/7 support and complete transparency in our operations'
    }
  }
};

// Helper pour récupérer les traductions
export const getTranslation = (language, key) => {
  const keys = key.split('.');
  let result = bonusTranslations[language];
  
  for (const k of keys) {
    if (result && result[k]) {
      result = result[k];
    } else {
      return key; // Return key if translation not found
    }
  }
  
  return result;
};
