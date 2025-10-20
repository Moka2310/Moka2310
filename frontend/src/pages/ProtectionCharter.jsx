import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Shield, AlertTriangle, Info, CheckCircle2, ArrowLeft, ArrowUp } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const ProtectionCharter = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();

  // Scroll to top when component mounts
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, []);

  const scrollToTop = () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  };

  const content = {
    fr: {
      title: "Charte de Protection",
      subtitle: "Votre sécurité et vos droits",
      sections: [
        {
          icon: Info,
          title: "1. Objet de la Charte",
          content: [
            "La présente charte définit les conditions générales d'utilisation du site TRADALIFE ainsi que les engagements pris pour la protection des utilisateurs et de leurs données personnelles.",
            "TRADALIFE est une plateforme d'informations, de formation et d'accompagnement en trading. Elle ne propose aucun service de courtage, ne détient aucun fonds d'utilisateurs et n'exécute pas directement d'opérations financières."
          ]
        },
        {
          icon: AlertTriangle,
          title: "2. Responsabilités et Limitation de Garantie",
          content: [
            "Le trading sur les marchés financiers (Forex, indices, crypto, matières premières, actions, etc.) comporte un risque élevé de perte partielle ou totale du capital investi.",
            "Les analyses, signaux ou formations diffusés par TRADALIFE sont à titre éducatif et informatif uniquement.",
            "TRADALIFE ne peut être tenue responsable des pertes, décisions, ou résultats liés aux transactions effectuées par les utilisateurs sur leurs propres comptes de trading.",
            "Chaque utilisateur demeure pleinement responsable de sa gestion du risque, de ses investissements et de ses choix financiers.",
            "TRADALIFE se dégage de toute responsabilité concernant les pertes financières, les défaillances techniques de plateformes partenaires, ou les erreurs/interruptions temporaires de service."
          ]
        },
        {
          icon: Shield,
          title: "3. Protection des Données Personnelles",
          content: [
            "TRADALIFE accorde une importance primordiale à la confidentialité des données de ses utilisateurs et se conforme au RGPD (Union Européenne) et à la LPRPDE/PIPEDA (Canada).",
            "Les données collectées (nom, prénom, adresse, e-mail, pièces d'identité, justificatifs) sont strictement nécessaires à la création du compte de trading et à la vérification d'identité.",
            "Aucune donnée n'est vendue, échangée ou partagée à des tiers non autorisés."
          ]
        },
        {
          icon: Shield,
          title: "4. Sécurité et Conservation des Données",
          content: [
            "Toutes les données personnelles sont stockées sur des serveurs sécurisés conformes aux standards internationaux (cryptage SSL, hébergement certifié).",
            "Accessibles uniquement par les membres autorisés de TRADALIFE ou par les courtiers partenaires à des fins de vérification de compte.",
            "Conservées pour la durée nécessaire à la gestion du compte, puis supprimées de manière sécurisée sur demande de l'utilisateur."
          ]
        },
        {
          icon: CheckCircle2,
          title: "5. Droit de Suppression et de Portabilité",
          content: [
            "Droit d'accès à ses données.",
            "Droit de rectification en cas d'erreur ou de changement d'information.",
            "Droit à la suppression complète de son compte et de toutes ses données personnelles.",
            "La suppression du compte peut être effectuée directement via le portail client TRADALIFE, ou par simple demande écrite au support.",
            "Une fois supprimées, les données sont définitivement effacées de nos serveurs dans un délai de 30 jours maximum."
          ]
        },
        {
          icon: Info,
          title: "6. Cookies et Outils de Suivi",
          content: [
            "Le site TRADALIFE utilise des cookies à des fins techniques, analytiques et de sécurité.",
            "L'utilisateur peut à tout moment désactiver ou supprimer les cookies via les paramètres de son navigateur.",
            "Aucune donnée comportementale n'est utilisée à des fins publicitaires sans consentement explicite."
          ]
        },
        {
          icon: Info,
          title: "7. Juridiction et Droit Applicable",
          content: [
            "Cette charte est régie par les lois en vigueur au Canada, dans la province de Québec, et conformément aux normes internationales de protection des données.",
            "En cas de litige, les tribunaux compétents seront ceux du district judiciaire de Montréal (Québec, Canada)."
          ]
        },
        {
          icon: CheckCircle2,
          title: "8. Acceptation de la Charte",
          content: [
            "En utilisant le site TRADALIFE, l'utilisateur reconnaît avoir lu, compris et accepté la présente charte dans son intégralité.",
            "L'inscription, la consultation du site ou la participation aux services offerts implique l'adhésion pleine et entière à ces conditions."
          ]
        },
        {
          icon: Info,
          title: "9. Contact",
          content: [
            "Pour toute question concernant la charte, la gestion de vos données ou une demande de suppression de compte :",
            "📧 kalot2310@gmail.com ou support@tradalife.com",
            "🌐 www.tradalife.com"
          ]
        }
      ],
      disclaimer: "En utilisant nos services, vous reconnaissez avoir lu et compris cette charte de protection et acceptez les risques associés au trading.",
      backButton: "Retour à l'accueil"
    },
    en: {
      title: "Protection Charter",
      subtitle: "Your security and your rights",
      sections: [
        {
          icon: Info,
          title: "1. Purpose of the Charter",
          content: [
            "This charter defines the general terms and conditions of use of the TRADALIFE website as well as the commitments made for the protection of users and their personal data.",
            "TRADALIFE is a platform for information, training and support in trading. It does not offer any brokerage services, does not hold any user funds and does not directly execute financial transactions."
          ]
        },
        {
          icon: AlertTriangle,
          title: "2. Responsibilities and Limitation of Warranty",
          content: [
            "Trading in financial markets (Forex, indices, crypto, commodities, stocks, etc.) carries a high risk of partial or total loss of invested capital.",
            "The analyzes, signals or training broadcast by TRADALIFE are for educational and informational purposes only.",
            "TRADALIFE cannot be held responsible for losses, decisions, or results related to transactions carried out by users on their own trading accounts.",
            "Each user remains fully responsible for their risk management, investments and financial choices.",
            "TRADALIFE disclaims all responsibility for financial losses, technical failures of partner platforms, or errors/temporary service interruptions."
          ]
        },
        {
          icon: Shield,
          title: "3. Personal Data Protection",
          content: [
            "TRADALIFE attaches paramount importance to the confidentiality of user data and complies with GDPR (European Union) and PIPEDA (Canada).",
            "The data collected (name, first name, address, email, identity documents, proof of address) are strictly necessary for creating the trading account and identity verification.",
            "No data is sold, exchanged or shared with unauthorized third parties."
          ]
        },
        {
          icon: Shield,
          title: "4. Data Security and Storage",
          content: [
            "All personal data is stored on secure servers compliant with international standards (SSL encryption, certified hosting).",
            "Accessible only by authorized members of TRADALIFE or by partner brokers for account verification purposes.",
            "Kept for the duration necessary to manage the account, then securely deleted upon user request."
          ]
        },
        {
          icon: CheckCircle2,
          title: "5. Right to Deletion and Portability",
          content: [
            "Right of access to your data.",
            "Right to rectification in case of error or change of information.",
            "Right to complete deletion of your account and all personal data.",
            "Account deletion can be done directly via the TRADALIFE client portal, or by simple written request to support.",
            "Once deleted, data is permanently erased from our servers within a maximum of 30 days."
          ]
        },
        {
          icon: Info,
          title: "6. Cookies and Tracking Tools",
          content: [
            "The TRADALIFE website uses cookies for technical, analytical and security purposes.",
            "The user can disable or delete cookies at any time via their browser settings.",
            "No behavioral data is used for advertising purposes without explicit consent."
          ]
        },
        {
          icon: Info,
          title: "7. Jurisdiction and Applicable Law",
          content: [
            "This charter is governed by the laws in force in Canada, in the province of Quebec, and in accordance with international data protection standards.",
            "In the event of a dispute, the competent courts will be those of the judicial district of Montreal (Quebec, Canada)."
          ]
        },
        {
          icon: CheckCircle2,
          title: "8. Acceptance of the Charter",
          content: [
            "By using the TRADALIFE site, the user acknowledges having read, understood and accepted this charter in its entirety.",
            "Registration, consultation of the site or participation in the services offered implies full and complete adherence to these conditions."
          ]
        },
        {
          icon: Info,
          title: "9. Contact",
          content: [
            "For any questions concerning the charter, the management of your data or a request for account deletion:",
            "📧 kalot2310@gmail.com or support@tradalife.com",
            "🌐 www.tradalife.com"
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
        {/* Back Button */}
        <Button
          onClick={() => navigate(-1)}
          variant="ghost"
          className="mb-6 text-pink-400 hover:text-pink-300 hover:bg-pink-500/10"
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          {language === 'fr' ? 'Retour' : 'Back'}
        </Button>

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

      {/* Floating Scroll to Top Button */}
      <button
        onClick={scrollToTop}
        className="fixed bottom-8 right-8 bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white p-4 rounded-full shadow-lg shadow-pink-500/50 hover:shadow-pink-500/70 transition-all hover:scale-110 z-50"
        aria-label="Scroll to top"
      >
        <ArrowUp className="w-6 h-6" />
      </button>
    </div>
  );
};

export default ProtectionCharter;
