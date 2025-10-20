// Mock data for Tradalife clone

export const formations = [
  {
    id: '1',
    title: 'Formation Trading Crypto',
    description: 'Apprenez les bases du trading de cryptomonnaies avec nos experts. Stratégies, analyses techniques et gestion de risque.',
    price: 299,
    duration: '8 heures',
    level: 'Débutant',
    image: 'https://images.unsplash.com/photo-1621761191319-c6fb62004040?w=500',
    videoCount: 12,
    telegramLinks: [
      { name: 'Canal Crypto VIP', url: 'https://t.me/tradalife_crypto' },
      { name: 'Groupe Support', url: 'https://t.me/tradalife_support' }
    ]
  },
  {
    id: '2',
    title: 'Formation Trading Forex',
    description: 'Maîtrisez le marché des devises. Apprenez à trader les paires de devises majeures et exotiques.',
    price: 349,
    duration: '10 heures',
    level: 'Intermédiaire',
    image: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500',
    videoCount: 15,
    telegramLinks: [
      { name: 'Canal Forex VIP', url: 'https://t.me/tradalife_forex' },
      { name: 'Signaux Forex', url: 'https://t.me/tradalife_signaux' }
    ]
  },
  {
    id: '3',
    title: 'Formation Trading Gold',
    description: 'Spécialisez-vous dans le trading de l\'or. Stratégies avancées et analyses de marché.',
    price: 399,
    duration: '6 heures',
    level: 'Avancé',
    image: 'https://images.unsplash.com/photo-1610375461246-83df859d849d?w=500',
    videoCount: 10,
    telegramLinks: [
      { name: 'Canal Gold VIP', url: 'https://t.me/tradalife_gold' }
    ]
  },
  {
    id: '4',
    title: 'Formation Indices Boursiers',
    description: 'Trading sur les indices majeurs: CAC40, DAX, S&P500. Stratégies et timing parfait.',
    price: 279,
    duration: '7 heures',
    level: 'Intermédiaire',
    image: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?w=500',
    videoCount: 11,
    telegramLinks: [
      { name: 'Canal Indices VIP', url: 'https://t.me/tradalife_indices' }
    ]
  },
  {
    id: '5',
    title: 'Pack Complet Trading',
    description: 'Toutes nos formations réunies: Crypto, Forex, Gold, Indices, Commodités et Actions.',
    price: 999,
    duration: '50+ heures',
    level: 'Tous niveaux',
    image: 'https://images.unsplash.com/photo-1642790106117-e829e14a795f?w=500',
    videoCount: 60,
    telegramLinks: [
      { name: 'Tous les canaux VIP', url: 'https://t.me/tradalife_vip' },
      { name: 'Support Premium', url: 'https://t.me/tradalife_premium' }
    ]
  }
];

export const canaux = [
  { name: 'Crypto', icon: 'https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,fit=crop/A3Ql90nqlVUN4Xox/logo-crypto-m6L27y8BnrC1Vbbz.png' },
  { name: 'Forex', icon: 'https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,fit=crop/A3Ql90nqlVUN4Xox/forex-dOqZvkMGWNCjDPxo.jpg' },
  { name: 'Indices', icon: 'https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,fit=crop/A3Ql90nqlVUN4Xox/indices-dJoPLkl9XGSBxOy2.jpg' },
  { name: 'Commodités', icon: 'https://i.imgur.com/63KI3jn.jpeg' },
  { name: 'Gold', icon: 'https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,fit=crop/A3Ql90nqlVUN4Xox/gold-YD0EekrWkoTklRaY.jpg' },
  { name: 'Actions', icon: 'https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,fit=crop/A3Ql90nqlVUN4Xox/actions-ALp25k8430sQMDZX.jpg' }
];

export const stats = [
  { 
    value: '+75%', 
    label: { fr: 'de taux de réussite', en: 'Success Rate' }, 
    sublabel: { fr: 'Hebdomadaire', en: 'Weekly' } 
  },
  { 
    value: '+4.000', 
    label: { fr: 'Membres actifs', en: 'Active Members' }, 
    sublabel: '' 
  },
  { 
    value: '+6', 
    label: { fr: 'Canaux V.I.P', en: 'V.I.P Channels' }, 
    sublabel: '' 
  },
  { 
    value: '+5 à 15', 
    label: { fr: 'Positions par jour', en: 'Positions per Day' }, 
    sublabel: '' 
  },
  { 
    value: '+2', 
    label: { fr: 'Brokers partenaires', en: 'Partner Brokers' }, 
    sublabel: '' 
  },
  { 
    value: '+3', 
    label: { fr: 'ans sur le marché financier', en: 'Years in Financial Market' }, 
    sublabel: '' 
  }
];