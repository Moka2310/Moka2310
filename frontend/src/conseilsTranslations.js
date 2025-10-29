export const conseilsTranslations = {
  fr: {
    conseils: {
      title: '📚 Conseils & Guide TRADABOT',
      subtitle: 'Tout ce que vous devez savoir pour utiliser TRADABOT efficacement',
      tabs: {
        capital: '💰 Gestion du Capital',
        installation: '🔧 Installation',
        tips: '💡 Conseils de Trading',
        faq: '❓ FAQ'
      },
      capital: {
        title: 'Tableau de Gestion des Lots',
        subtitle: 'Ajustez vos lots selon votre capital pour respecter une gestion de risque optimale.',
        warning: '⚠️ Ces valeurs sont des recommandations. Adaptez selon votre tolérance au risque.',
        table: {
          capital: 'Capital',
          forex: 'Forex',
          crypto: 'Crypto',
          gold: 'Gold',
          indices: 'Indices',
          actions: 'Commodités',
          risk: 'Niveau de Risque'
        },
        important: {
          title: 'Important',
          points: [
            'Commencez toujours par le niveau de risque le plus faible',
            'Augmentez progressivement les lots après 2-3 semaines de résultats positifs',
            'Ne risquez JAMAIS plus de 5% de votre capital total sur une journée',
            'Gardez toujours une marge de sécurité d\'au moins 30% disponible'
          ]
        }
      },
      installation: {
        title: 'Guide d\'Installation Pas à Pas',
        note: {
          title: '📝 Note Technique',
          description: 'Le connecteur doit rester en exécution pendant les heures de trading. Nous recommandons d\'utiliser un VPS Windows si vous ne pouvez pas garder votre ordinateur allumé 24/7.'
        }
      },
      tips: {
        title: 'Conseils de Trading Essentiels',
        warning: {
          title: 'Avertissement',
          description: 'Le trading comporte des risques. Même avec des signaux de qualité, des pertes sont possibles. N\'investissez que de l\'argent que vous pouvez vous permettre de perdre. Les performances passées ne garantissent pas les résultats futurs.'
        }
      },
      faq: {
        title: 'Questions Fréquentes',
        needHelp: {
          title: 'Besoin d\'aide ?',
          description: 'Rejoignez notre canal Telegram de support pour obtenir de l\'aide en temps réel',
          button: '💬 Rejoindre le Support'
        }
      }
    }
  },
  en: {
    conseils: {
      title: '📚 Tips & TRADABOT Guide',
      subtitle: 'Everything you need to know to use TRADABOT effectively',
      tabs: {
        capital: '💰 Capital Management',
        installation: '🔧 Installation',
        tips: '💡 Trading Tips',
        faq: '❓ FAQ'
      },
      capital: {
        title: 'Lot Size Management Table',
        subtitle: 'Adjust your lots according to your capital to maintain optimal risk management.',
        warning: '⚠️ These are recommendations. Adjust according to your risk tolerance.',
        table: {
          capital: 'Capital',
          forex: 'Forex',
          crypto: 'Crypto',
          gold: 'Gold',
          indices: 'Indices',
          actions: 'Stocks',
          risk: 'Risk Level'
        },
        important: {
          title: 'Important',
          points: [
            'Always start with the lowest risk level',
            'Gradually increase lots after 2-3 weeks of positive results',
            'NEVER risk more than 5% of your total capital in a single day',
            'Always keep a safety margin of at least 30% available'
          ]
        }
      },
      installation: {
        title: 'Step-by-Step Installation Guide',
        note: {
          title: '📝 Technical Note',
          description: 'The connector must remain running during trading hours. We recommend using a Windows VPS if you cannot keep your computer on 24/7.'
        }
      },
      tips: {
        title: 'Essential Trading Tips',
        warning: {
          title: 'Warning',
          description: 'Trading involves risks. Even with quality signals, losses are possible. Only invest money you can afford to lose. Past performance does not guarantee future results.'
        }
      },
      faq: {
        title: 'Frequently Asked Questions',
        needHelp: {
          title: 'Need help?',
          description: 'Join our support Telegram channel for real-time assistance',
          button: '💬 Join Support'
        }
      }
    }
  }
};

export const referralTranslations = {
  fr: {
    referral: {
      title: '🎁 Programme de Parrainage',
      subtitle: 'Gagnez des récompenses en invitant vos amis',
      yourCode: {
        title: 'Votre Code de Parrainage',
        copy: 'Copier le lien',
        copied: 'Lien copié!'
      },
      howItWorks: {
        title: 'Comment ça marche ?',
        steps: [
          {
            title: 'Partagez votre lien',
            description: 'Envoyez votre lien de parrainage à vos amis'
          },
          {
            title: 'Ils s\'inscrivent',
            description: 'Vos amis créent un compte avec votre lien'
          },
          {
            title: 'Vous gagnez',
            description: 'Recevez des récompenses pour chaque parrainage'
          }
        ]
      },
      stats: {
        title: 'Vos Statistiques',
        totalReferrals: 'Parrainages Totaux',
        activeReferrals: 'Parrainages Actifs',
        totalEarnings: 'Gains Totaux'
      },
      history: {
        title: 'Historique des Parrainages',
        date: 'Date',
        user: 'Utilisateur',
        status: 'Statut',
        reward: 'Récompense',
        noReferrals: 'Aucun parrainage pour le moment'
      }
    }
  },
  en: {
    referral: {
      title: '🎁 Referral Program',
      subtitle: 'Earn rewards by inviting your friends',
      yourCode: {
        title: 'Your Referral Code',
        copy: 'Copy Link',
        copied: 'Link copied!'
      },
      howItWorks: {
        title: 'How it works?',
        steps: [
          {
            title: 'Share your link',
            description: 'Send your referral link to your friends'
          },
          {
            title: 'They sign up',
            description: 'Your friends create an account with your link'
          },
          {
            title: 'You earn',
            description: 'Receive rewards for each referral'
          }
        ]
      },
      stats: {
        title: 'Your Statistics',
        totalReferrals: 'Total Referrals',
        activeReferrals: 'Active Referrals',
        totalEarnings: 'Total Earnings'
      },
      history: {
        title: 'Referral History',
        date: 'Date',
        user: 'User',
        status: 'Status',
        reward: 'Reward',
        noReferrals: 'No referrals yet'
      }
    }
  }
};
