import React from 'react';
import { Users, Award, TrendingUp, Shield, Target, Heart } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const AboutUs = () => {
  const { language } = useLanguage();

  // Texte biographie
  const biographyFr = {
    intro: "Je m'appelle Kalot Mohamad, Canadien d'origine libanaise, passionné par le monde de la finance et du trading. Mon parcours n'a pourtant pas commencé dans cet univers. Pendant plusieurs années, j'ai exercé dans des domaines très éloignés des marchés financiers.",
    discovery: "Mais il y a environ huit ans, au moment où le monde découvrait les NFT et l'essor fulgurant de la crypto-monnaie, j'ai eu un véritable déclic. Fasciné par cette révolution numérique et économique, j'ai décidé de m'y plonger à fond. J'ai d'abord fait mes armes dans le secteur des cryptos et des NFT, en observant les cycles, les innovations et les comportements du marché.",
    evolution: "Cette expérience m'a permis de développer une compréhension fine des dynamiques financières modernes. Très vite, j'ai souhaité aller plus loin et me tourner vers le trading professionnel, en étudiant de manière approfondie l'analyse technique, la gestion du risque et les stratégies multi-actifs.",
    tradalife: "C'est ainsi qu'est née TRADALIFE, une communauté de traders que j'ai fondée il y a maintenant trois ans. Depuis sa création, TRADALIFE affiche un taux de réussite hebdomadaire d'environ 75%, fruit d'une approche structurée, disciplinée et axée sur la performance collective.",
    mission: "Aujourd'hui, j'ai l'honneur de former personnellement tous les nouveaux membres qui rejoignent l'aventure. J'y transmets non seulement mes connaissances techniques, mais aussi ma vision du trading : une discipline basée sur la patience, la rigueur et la maîtrise émotionnelle.",
    goal: "Mon objectif est de permettre à chacun — qu'il soit débutant ou déjà expérimenté — d'apprendre à lire le marché, à construire sa propre stratégie et à devenir financièrement indépendant.",
    conclusion: "Installé au Canada depuis 8 ans, j'ai su bâtir une structure solide, professionnelle et ouverte sur le monde, qui reflète ma philosophie :",
    quote: "\"Le trading n'est pas un jeu de hasard, c'est une science, une stratégie et un état d'esprit.\""
  };

  const biographyEn = {
    intro: "My name is Kalot Mohamad, a Canadian of Lebanese origin, passionate about the world of finance and trading. However, my journey didn't start in this field. For several years, I worked in areas far removed from financial markets.",
    discovery: "But about eight years ago, when the world was discovering NFTs and the meteoric rise of cryptocurrency, I had a real awakening. Fascinated by this digital and economic revolution, I decided to dive in headfirst. I first cut my teeth in the crypto and NFT sector, observing cycles, innovations and market behaviors.",
    evolution: "This experience allowed me to develop a fine understanding of modern financial dynamics. Very quickly, I wanted to go further and turn to professional trading, studying technical analysis, risk management and multi-asset strategies in depth.",
    tradalife: "This is how TRADALIFE was born, a community of traders that I founded three years ago. Since its creation, TRADALIFE has achieved a weekly success rate of around 75%, the result of a structured, disciplined approach focused on collective performance.",
    mission: "Today, I have the honor of personally training all new members who join the adventure. I transmit not only my technical knowledge, but also my vision of trading: a discipline based on patience, rigor and emotional control.",
    goal: "My goal is to enable everyone — whether beginner or experienced — to learn to read the market, build their own strategy and become financially independent.",
    conclusion: "Having lived in Canada for 8 years, I have built a solid, professional structure open to the world, which reflects my philosophy:",
    quote: "\"Trading is not a game of chance, it's a science, a strategy and a mindset.\""
  };

  const biography = language === 'fr' ? biographyFr : biographyEn;

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#0A0118] via-[#1a0b2e] to-[#16213E] pt-32 px-4 pb-20">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-400 to-purple-600 bg-clip-text text-transparent mb-4">
            {language === 'fr' ? 'Qui sommes nous?' : 'About Us'}
          </h1>
          <p className="text-white/70 text-lg">
            {language === 'fr' 
              ? 'Découvrez l\'histoire et la vision du fondateur de TRADALIFE'
              : 'Discover the story and vision of TRADALIFE\'s founder'}
          </p>
        </div>

        {/* Main Content Card */}
        <div className="bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-3xl border border-purple-500/30 overflow-hidden mb-12">
          {/* Image Section */}
          <div className="relative h-96 overflow-hidden">
            <img
              src="https://customer-assets.emergentagent.com/job_tradebot-launch/artifacts/bcatt7w6_ChatGPT%20Image%2023%20oct.%202025%2C%2021%20h%2052%20min%2025%20s.png"
              alt="Calo Mohamed - Fondateur TRADALIFE"
              className="w-full h-full object-cover object-top"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-[#2B1F5C] via-[#2B1F5C]/50 to-transparent" />
            
            {/* Overlay Info */}
            <div className="absolute bottom-8 left-8 right-8">
              <div className="bg-gradient-to-r from-pink-500 to-purple-600 p-1 rounded-2xl inline-block">
                <div className="bg-[#1E1540] px-6 py-4 rounded-2xl">
                  <h2 className="text-2xl font-bold text-white">Calo Mohamed</h2>
                  <p className="text-pink-400">{language === 'fr' ? 'Fondateur de TRADALIFE' : 'Founder of TRADALIFE'}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Text Content */}
          <div className="p-8 md:p-12">
            <div className="space-y-6 text-white/90 text-lg leading-relaxed">
              <p>{biography.intro}</p>
              
              <p>{biography.discovery}</p>

              <p>{biography.evolution}</p>

              <div className="bg-gradient-to-r from-pink-500/10 to-purple-500/10 border-l-4 border-pink-500 p-6 rounded-r-xl my-6">
                <p className="font-semibold">{biography.tradalife}</p>
              </div>

              <p>{biography.mission}</p>

              <p>{biography.goal}</p>

              <p>{biography.conclusion}</p>

              <div className="text-center my-8">
                <p className="text-2xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-600">
                  {biography.quote}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Stats/Features Grid */}
        <div className="grid md:grid-cols-3 gap-6">
          <div className="bg-gradient-to-br from-blue-500/20 to-purple-500/20 rounded-2xl border border-blue-500/30 p-6 backdrop-blur-sm">
            <div className="bg-blue-500/20 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Award className="w-7 h-7 text-blue-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">
              {language === 'fr' ? '8 ans d\'expérience' : '8 years of experience'}
            </h3>
            <p className="text-white/70">
              {language === 'fr' 
                ? 'Dans le trading et les marchés financiers depuis 2017'
                : 'In trading and financial markets since 2017'}
            </p>
          </div>

          <div className="bg-gradient-to-br from-pink-500/20 to-purple-500/20 rounded-2xl border border-pink-500/30 p-6 backdrop-blur-sm">
            <div className="bg-pink-500/20 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Target className="w-7 h-7 text-pink-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">
              {language === 'fr' ? '75% de réussite' : '75% success rate'}
            </h3>
            <p className="text-white/70">
              {language === 'fr' 
                ? 'Taux de réussite hebdomadaire constant depuis 3 ans'
                : 'Consistent weekly success rate for 3 years'}
            </p>
          </div>

          <div className="bg-gradient-to-br from-green-500/20 to-emerald-500/20 rounded-2xl border border-green-500/30 p-6 backdrop-blur-sm">
            <div className="bg-green-500/20 w-14 h-14 rounded-xl flex items-center justify-center mb-4">
              <Heart className="w-7 h-7 text-green-400" />
            </div>
            <h3 className="text-xl font-bold text-white mb-2">
              {language === 'fr' ? 'Formation personnelle' : 'Personal training'}
            </h3>
            <p className="text-white/70">
              {language === 'fr' 
                ? 'Chaque membre est formé personnellement par le fondateur'
                : 'Every member is personally trained by the founder'}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AboutUs;
