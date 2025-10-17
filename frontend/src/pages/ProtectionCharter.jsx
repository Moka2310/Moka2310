import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Shield, AlertTriangle, Info, CheckCircle2, ArrowLeft } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const ProtectionCharter = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();

  const content = {
    fr: {
      title: "Charte de Protection - Trading",
      subtitle: "Votre sécurité est notre priorité",
      sections: [
        {
          icon: AlertTriangle,
          title: "Avertissement sur les Risques",
          content: [
            "Le trading sur les marchés financiers (Forex, Crypto, Actions, Indices, Commodités) comporte un risque élevé de perte financière.",
            "Les performances passées ne garantissent pas les résultats futurs.",
            "Ne tradez jamais avec des fonds que vous ne pouvez pas vous permettre de perdre.",
            "Les signaux et formations fournis sont à titre éducatif uniquement et ne constituent pas des conseils financiers."
          ]
        },
        {
          icon: Shield,
          title: "Protection de vos Données",
          content: [
            "Vos informations personnelles sont cryptées et sécurisées.",
            "Nous ne partageons jamais vos données avec des tiers sans votre consentement.",
            "Vos documents KYC sont stockés de manière confidentielle.",
            "Vous pouvez demander la suppression de vos données à tout moment."
          ]
        },
        {
          icon: CheckCircle2,
          title: "Vos Droits",
          content: [
            "Accès à tous les contenus de formation après achat.",
            "Support client disponible pour toute question.",
            "Transparence totale sur nos services et tarifs.",
            "Droit de rétractation selon les conditions générales de vente."
          ]
        },
        {
          icon: Info,
          title: "Responsabilités",
          content: [
            "Tradalife fournit des outils éducatifs et des signaux de trading.",
            "Vous êtes seul responsable de vos décisions de trading.",
            "Nous recommandons fortement de pratiquer sur un compte démo avant le trading réel.",
            "Consultez un conseiller financier indépendant si nécessaire."
          ]
        }
      ],
      disclaimer: "En utilisant nos services, vous reconnaissez avoir lu et compris cette charte de protection et acceptez les risques associés au trading.",
      backButton: "Retour à l'accueil"
    },
    en: {
      title: "Protection Charter - Trading",
      subtitle: "Your security is our priority",
      sections: [
        {
          icon: AlertTriangle,
          title: "Risk Warning",
          content: [
            "Trading in financial markets (Forex, Crypto, Stocks, Indices, Commodities) carries a high risk of financial loss.",
            "Past performance does not guarantee future results.",
            "Never trade with funds you cannot afford to lose.",
            "The signals and training provided are for educational purposes only and do not constitute financial advice."
          ]
        },
        {
          icon: Shield,
          title: "Data Protection",
          content: [
            "Your personal information is encrypted and secured.",
            "We never share your data with third parties without your consent.",
            "Your KYC documents are stored confidentially.",
            "You can request deletion of your data at any time."
          ]
        },
        {
          icon: CheckCircle2,
          title: "Your Rights",
          content: [
            "Access to all training content after purchase.",
            "Customer support available for any questions.",
            "Full transparency on our services and pricing.",
            "Right of withdrawal according to terms and conditions."
          ]
        },
        {
          icon: Info,
          title: "Responsibilities",
          content: [
            "Tradalife provides educational tools and trading signals.",
            "You are solely responsible for your trading decisions.",
            "We strongly recommend practicing on a demo account before live trading.",
            "Consult an independent financial advisor if necessary."
          ]
        }
      ],
      disclaimer: "By using our services, you acknowledge that you have read and understood this protection charter and accept the risks associated with trading.",
      backButton: "Back to home"
    }
  };

  const t = content[language];

  return (
    <div className="min-h-screen bg-[#1E1540] pt-28 pb-20 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="inline-flex items-center justify-center w-20 h-20 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full mb-6">
            <Shield className="w-10 h-10 text-white" />
          </div>
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
              {t.title}
            </span>
          </h1>
          <p className="text-white/70 text-lg">{t.subtitle}</p>
        </div>

        {/* Sections */}
        <div className="space-y-8">
          {t.sections.map((section, index) => {
            const Icon = section.icon;
            return (
              <div
                key={index}
                className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl p-8 border border-purple-500/30"
              >
                <div className="flex items-start space-x-4">
                  <div className="flex-shrink-0">
                    <div className="w-12 h-12 bg-pink-500/20 rounded-full flex items-center justify-center">
                      <Icon className="w-6 h-6 text-pink-400" />
                    </div>
                  </div>
                  <div className="flex-1">
                    <h2 className="text-2xl font-bold text-white mb-4">{section.title}</h2>
                    <ul className="space-y-3">
                      {section.content.map((item, idx) => (
                        <li key={idx} className="flex items-start space-x-3">
                          <span className="text-pink-400 mt-1">•</span>
                          <span className="text-white/80 text-lg leading-relaxed">{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
              </div>
            );
          })}
        </div>

        {/* Disclaimer */}
        <div className="mt-12 bg-yellow-500/10 border border-yellow-500/30 rounded-2xl p-6">
          <p className="text-yellow-200 text-center leading-relaxed">
            <strong className="font-bold">⚠️ Clause de non-responsabilité : </strong>
            {t.disclaimer}
          </p>
        </div>

        {/* Back Button */}
        <div className="mt-12 text-center">
          <Button
            onClick={() => navigate('/')}
            className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-6 text-lg rounded-full"
          >
            {t.backButton}
          </Button>
        </div>
      </div>
    </div>
  );
};

export default ProtectionCharter;
