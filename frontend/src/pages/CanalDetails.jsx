import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { ArrowLeft, ChevronDown, ChevronUp } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const CanalDetails = () => {
  const { canalName } = useParams();
  const navigate = useNavigate();
  const { language } = useLanguage();
  const [expandedAsset, setExpandedAsset] = useState(null);

  // Scroll to top when page loads
  React.useEffect(() => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }, [canalName]);

  // Descriptions des actifs
  const assetDescriptions = {
    // CRYPTO
    'BTCUSD': "BTCUSD représente la valeur du Bitcoin face au dollar américain. C'est la paire la plus connue du marché crypto. Elle reflète la confiance des investisseurs envers les monnaies numériques et la politique économique mondiale. Très volatile, le Bitcoin offre d'importantes opportunités de trading, notamment lors des périodes d'incertitude financière.",
    
    // GOLD
    'XAUUSD': "XAUUSD représente le prix de l'or face au dollar américain. Actif refuge par excellence, il est très prisé en période d'incertitude économique. Sa valeur évolue selon les taux d'intérêt, l'inflation et le niveau du dollar américain.",
    'XAUEUR': "XAUEUR compare l'or à l'euro. Il reflète la valeur du métal jaune pour les investisseurs européens. Utilisé comme protection contre la dépréciation monétaire et les crises économiques, c'est un actif stable et universel.",
    'XAGUSD': "XAGUSD mesure le prix de l'argent face au dollar américain. Moins cher mais plus volatile que l'or, il est influencé par la demande industrielle et la spéculation. Un actif apprécié pour ses fortes variations de prix.",
    'XAGEUR': "XAGEUR montre la valeur de l'argent en euros. Souvent utilisé comme alternative à l'or, il combine valeur refuge et usage industriel. Il réagit aux cycles économiques européens et mondiaux.",
    
    // FOREX
    'USDJPY': "La paire USD/JPY compare le dollar américain au yen japonais. C'est l'une des plus échangées au monde. Son mouvement reflète la politique monétaire de la Fed et de la Banque du Japon. Appréciée pour sa volatilité contrôlée et sa réaction aux taux d'intérêt.",
    'USDCAD': "La paire USD/CAD mesure la valeur du dollar américain face au dollar canadien. Étroitement liée aux prix du pétrole, elle reflète la force économique des deux pays nord-américains. Une paire stable et très suivie sur le Forex.",
    'USDCHF': "USD/CHF oppose le dollar américain au franc suisse. Souvent considérée comme une valeur refuge, cette paire réagit fortement aux périodes d'incertitude économique mondiale. Très utilisée pour la diversification et la couverture.",
    'GBPJPY': "La paire GBP/JPY combine la livre sterling et le yen japonais. C'est une paire dynamique et volatile, souvent appelée \"le monstre\" du Forex. Elle attire les traders expérimentés à la recherche de forts mouvements quotidiens.",
    'GBPUSD': "Connue sous le nom de \"Cable\", GBP/USD compare la livre britannique au dollar américain. Elle reflète les relations économiques entre le Royaume-Uni et les États-Unis et réagit aux annonces économiques majeures des deux pays.",
    'GBPAUD': "La paire GBPAUD montre la valeur de la livre sterling face au dollar australien. Elle dépend des politiques économiques du Royaume-Uni et de l'Australie, ainsi que des fluctuations des matières premières comme l'or et le fer.",
    'GBPCAD': "GBPCAD met en balance la livre britannique et le dollar canadien. Son cours est influencé par les prix du pétrole et les politiques monétaires respectives de la Banque d'Angleterre et de la Banque du Canada. Paire intermédiaire et fluide.",
    'GBPNZD': "Cette paire compare la livre sterling au dollar néo-zélandais. Elle est sensible aux variations des taux d'intérêt et au marché des matières premières agricoles. Une paire active et appréciée pour ses tendances nettes.",
    'GBPCHF': "GBPCHF associe la livre sterling et le franc suisse. Elle combine la stabilité suisse avec la volatilité britannique, offrant des opportunités intéressantes dans les marchés calmes ou agités.",
    'EURUSD': "La paire EUR/USD est la plus échangée au monde. Elle compare l'euro au dollar américain et reflète la santé économique de la zone euro et des États-Unis. Sa liquidité en fait un actif de base pour tout trader.",
    'EURAUD': "EURAUD représente l'euro face au dollar australien. Elle est influencée par les exportations australiennes de matières premières et par les annonces économiques européennes. Une paire appréciée pour ses mouvements techniques clairs.",
    'EURJPY': "EURJPY mesure la valeur de l'euro face au yen japonais. C'est une paire stable mais réactive aux changements économiques mondiaux et aux décisions de politique monétaire en Europe et au Japon.",
    'EURNZD': "EURNZD compare l'euro et le dollar néo-zélandais. Elle réagit aux politiques économiques européennes et aux cycles de production agricole en Océanie. Paire au comportement souvent directionnel.",
    'EURCAD': "EURCAD met en relation l'euro et le dollar canadien. Elle évolue selon les prix des matières premières, notamment du pétrole, et les annonces économiques européennes. Un choix populaire pour les stratégies swing.",
    'AUDJPY': "AUDJPY compare le dollar australien et le yen japonais. Elle réagit fortement aux cycles de risque mondial et aux cours des matières premières. Idéale pour ceux qui suivent la tendance \"risk-on / risk-off\".",
    'AUDCHF': "AUDCHF combine le dollar australien et le franc suisse. Elle reflète l'appétit ou l'aversion pour le risque des investisseurs, offrant un bon indicateur de la stabilité des marchés mondiaux.",
    'AUDUSD': "AUDUSD compare le dollar australien au dollar américain. Elle est influencée par les exportations australiennes et les décisions de la Réserve fédérale. C'est une paire populaire pour le trading de tendance.",
    'AUDCAD': "AUDCAD met en balance le dollar australien et le dollar canadien. Deux économies riches en ressources naturelles, cette paire est souvent stable mais sensible aux prix du pétrole et des métaux.",
    'NZDUSD': "NZDUSD oppose le dollar néo-zélandais au dollar américain. Elle est très liée au marché agricole et aux taux d'intérêt. Une paire fluide, prisée pour le trading de court et moyen terme.",
    'CADJPY': "CADJPY compare le dollar canadien et le yen japonais. Elle dépend fortement du prix du pétrole et du climat économique mondial. Un bon indicateur du sentiment de risque sur les marchés.",
    'NZDJPY': "NZDJPY met en relation le dollar néo-zélandais et le yen japonais. Sensible aux cycles économiques asiatiques et aux taux d'intérêt, elle attire les traders cherchant des tendances nettes.",
    'NZDCHF': "NZDCHF associe le dollar néo-zélandais au franc suisse. Elle reflète les flux de capitaux entre les marchés à haut rendement et les valeurs refuges. Paire modérée, utile pour la diversification.",
    'NZDCAD': "NZDCAD compare le dollar néo-zélandais et le dollar canadien. Influencée par le commerce des matières premières, elle offre des mouvements réguliers et une bonne stabilité.",
    
    // INDICES
    'NAS100': "Le NAS100 regroupe les 100 plus grandes entreprises technologiques américaines, comme Apple, Tesla et Microsoft. C'est un indice très volatil, idéal pour le trading à court terme. Il reflète la performance globale du secteur technologique américain.",
    'US500': "L'indice US500 représente les 500 plus grandes entreprises cotées aux États-Unis. C'est un baromètre majeur de la santé économique américaine. Stable et diversifié, il attire les traders recherchant des mouvements structurés et des tendances durables.",
    'UK100': "Le UK100 réunit les 100 plus grandes sociétés britanniques cotées à la Bourse de Londres. Il reflète la santé économique du Royaume-Uni et réagit aux politiques de la Banque d'Angleterre, ainsi qu'aux variations de la livre sterling.",
    'FRA40': "Le FRA40 est l'indice phare de la Bourse de Paris, regroupant les 40 plus grandes entreprises françaises. C'est un indicateur clé de l'économie européenne, prisé pour sa régularité et ses réactions nettes aux annonces économiques de la zone euro.",
    'HK50': "Le HK50 représente les principales entreprises cotées à Hong Kong. Il reflète l'économie chinoise et asiatique, souvent influencée par les tensions commerciales et les politiques économiques de Pékin. Volatil et riche en opportunités.",
    
    // COMMODITÉS
    'SUGARRAW': "SUGARRAW représente le prix du sucre brut échangé sur les marchés mondiaux. Son cours dépend des conditions climatiques, des récoltes de canne à sucre, et de la production mondiale. C'est un actif agricole sensible aux cycles saisonniers et aux politiques commerciales.",
    'SOYBEAN': "Le soja est une matière première agricole majeure utilisée dans l'alimentation et les biocarburants. Son prix varie selon les récoltes, la demande mondiale et les échanges entre les États-Unis, le Brésil et la Chine. Actif stable et stratégique pour suivre les tendances agricoles mondiales.",
    'XTIUSD': "Le WTI (West Texas Intermediate) est une référence mondiale pour le prix du pétrole américain. Son cours dépend de l'offre et de la demande mondiale, des stocks et des tensions géopolitiques. Actif très volatil, il offre d'excellentes opportunités de trading.",
    'XBRUSD': "Le Brent est le principal indice du pétrole européen. Il reflète la santé de l'économie mondiale et les équilibres géopolitiques. C'est un actif incontournable pour les traders de matières premières.",
    'XNGUSD': "XNGUSD représente le prix du gaz naturel face au dollar américain. Il est influencé par les conditions climatiques, la production énergétique et la demande industrielle. Un actif énergique et volatil.",
    'XPTUSD': "Le platine est un métal précieux rare, utilisé dans l'industrie automobile et la joaillerie. Sa valeur dépend de la demande industrielle et des tensions d'approvisionnement. Moins connu que l'or, mais souvent très réactif.",
    'XPDUSD': "Le palladium est un métal stratégique utilisé dans les catalyseurs automobiles. Son prix reflète les évolutions de l'industrie et de la production minière. Actif rare et très volatil, apprécié des traders avancés.",
    'XCUUSD': "Le cuivre est un indicateur clé de la croissance économique mondiale. Utilisé dans la construction et la technologie, il réagit aux cycles industriels et à la demande de la Chine. Un actif cyclique et prévisible.",
    'WHEAT': "Le blé est une matière première agricole essentielle. Son prix varie selon les récoltes, la météo et les politiques d'exportation. Actif suivi pour anticiper les tendances alimentaires mondiales.",
    'CORN': "Le maïs est une denrée agricole majeure, utilisée dans l'alimentation et les biocarburants. Son cours dépend des conditions climatiques, de la demande mondiale et du marché de l'énergie.",
    
    // ACTIONS
    'AAPL': "Apple est l'une des plus grandes entreprises technologiques au monde, connue pour l'iPhone, le Mac et ses services numériques. Son action symbolise l'innovation et la stabilité du secteur technologique américain.",
    'AAL': "American Airlines est l'une des plus grandes compagnies aériennes mondiales. Son cours reflète la santé du transport aérien et les tendances économiques globales.",
    'ADBE': "Adobe développe des logiciels incontournables comme Photoshop et Acrobat. Son action attire les investisseurs intéressés par la croissance du secteur de la création numérique et du cloud.",
    'AMD': "AMD est un leader dans la conception de processeurs et cartes graphiques. Concurrente directe de NVIDIA et Intel, l'entreprise incarne la puissance du secteur des semi-conducteurs.",
    'AMZN': "Amazon domine le commerce en ligne mondial et le cloud computing à travers AWS. Son action est un pilier de la technologie et de la consommation mondiale.",
    'EA': "Electronic Arts est un géant du jeu vidéo, créateur de franchises comme FIFA et Battlefield. Son action reflète la vitalité du secteur du divertissement numérique.",
    'EBAY': "eBay est une plateforme mondiale de commerce entre particuliers. Son action suit les tendances de la consommation en ligne et des places de marché numériques.",
    'META': "Anciennement Facebook, Meta est au cœur des réseaux sociaux et du métavers. Son action est liée à la croissance de la publicité en ligne et des technologies immersives.",
    'GOOG': "Alphabet, maison mère de Google, est un acteur dominant de la recherche en ligne, de la publicité numérique et de l'intelligence artificielle. Son action symbolise la solidité technologique mondiale.",
    'MSFT': "Microsoft est un pilier de l'informatique mondiale, avec Windows, Office, Azure et l'IA. Son action reflète la stabilité et la croissance durable du secteur technologique.",
    'NFLX': "Netflix est le leader mondial du streaming vidéo. Son cours suit l'évolution des abonnements, des productions originales et des tendances du divertissement.",
    'NVDA': "NVIDIA est un géant mondial des processeurs graphiques (GPU) et de l'intelligence artificielle. Son action incarne la révolution technologique dans le cloud, le gaming et l'IA.",
    'PEP': "PepsiCo est une multinationale de l'agroalimentaire et des boissons. Son action combine stabilité et performance, soutenue par des marques fortes et une présence mondiale.",
    'TSLA': "Tesla est le pionnier mondial des véhicules électriques et de l'énergie propre. Son action attire les traders pour sa forte volatilité et son potentiel d'innovation à long terme."
  };

  // Définir les actifs pour chaque canal
  const canalsData = {
    crypto: {
      name: { fr: 'CRYPTO', en: 'CRYPTO' },
      description: { 
        fr: 'Trading de cryptomonnaies',
        en: 'Cryptocurrency trading'
      },
      assets: ['BTCUSD']
    },
    gold: {
      name: { fr: 'GOLD', en: 'GOLD' },
      description: { 
        fr: 'Trading de l\'or et métaux précieux',
        en: 'Gold and precious metals trading'
      },
      assets: ['XAUUSD', 'XAUEUR', 'XAGUSD', 'XAGEUR']
    },
    forex: {
      name: { fr: 'FOREX', en: 'FOREX' },
      description: { 
        fr: 'Trading des paires de devises',
        en: 'Currency pairs trading'
      },
      assets: ['USDJPY', 'USDCAD', 'USDCHF', 'GBPJPY', 'GBPUSD', 'GBPAUD', 'GBPCAD', 'GBPNZD', 'GBPCHF', 'EURUSD', 'EURAUD', 'EURJPY', 'EURNZD', 'EURCAD', 'AUDJPY', 'AUDCHF', 'AUDUSD', 'AUDCAD', 'NZDUSD', 'CADJPY', 'NZDJPY', 'NZDCHF', 'NZDCAD']
    },
    indices: {
      name: { fr: 'INDICES', en: 'INDICES' },
      description: { 
        fr: 'Trading des indices boursiers',
        en: 'Stock indices trading'
      },
      assets: ['NAS100', 'US500', 'UK100', 'FRA40', 'HK50']
    },
    commodités: {
      name: { fr: 'COMMODITÉS', en: 'COMMODITIES' },
      description: { 
        fr: 'Trading des matières premières',
        en: 'Commodities trading'
      },
      assets: ['SUGARRAW', 'SOYBEAN', 'XTIUSD', 'XBRUSD', 'XNGUSD', 'XPTUSD', 'XPDUSD', 'XCUUSD', 'WHEAT', 'CORN']
    },
    actions: {
      name: { fr: 'ACTIONS', en: 'STOCKS' },
      description: { 
        fr: 'Trading des actions',
        en: 'Stock trading'
      },
      assets: ['AAPL', 'AAL', 'ADBE', 'AMD', 'AMZN', 'EA', 'EBAY', 'META', 'GOOG', 'MSFT', 'NFLX', 'NVDA', 'PEP', 'TSLA']
    }
  };

  const canal = canalsData[canalName?.toLowerCase()];

  if (!canal) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-[#1E1540] via-black to-[#1E1540] flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold text-white mb-4">Canal non trouvé</h1>
          <button
            onClick={() => navigate('/')}
            className="text-pink-400 hover:text-pink-300"
          >
            Retour à l'accueil
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-[#1E1540] via-black to-[#1E1540] pt-24 pb-16">
      <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Bouton retour */}
        <button
          onClick={() => {
            navigate('/');
            setTimeout(() => {
              document.getElementById('canaux')?.scrollIntoView({ behavior: 'smooth' });
            }, 100);
          }}
          className="flex items-center space-x-2 text-pink-400 hover:text-pink-300 mb-8 transition-colors"
        >
          <ArrowLeft className="w-5 h-5" />
          <span>{language === 'fr' ? 'Retour aux canaux' : 'Back to channels'}</span>
        </button>

        {/* En-tête du canal */}
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold bg-gradient-to-r from-pink-500 via-purple-500 to-pink-500 bg-clip-text text-transparent mb-4">
            {canal.name[language]}
          </h1>
          <p className="text-white/70 text-lg">
            {canal.description[language]}
          </p>
        </div>

        {/* Liste des actifs avec descriptions */}
        <div className="bg-gradient-to-br from-purple-900/30 to-pink-900/30 backdrop-blur-lg rounded-2xl p-8 border border-purple-500/30">
          <h2 className="text-2xl font-bold text-white mb-6 text-center">
            {language === 'fr' ? 'Liste des actifs tradés' : 'List of traded assets'}
          </h2>
          
          <div className="space-y-4">
            {canal.assets.map((asset, index) => (
              <div
                key={index}
                className="bg-gradient-to-br from-purple-600/20 to-pink-600/20 rounded-xl border border-purple-500/30 hover:border-pink-500/50 transition-all duration-300 overflow-hidden"
              >
                <button
                  onClick={() => setExpandedAsset(expandedAsset === asset ? null : asset)}
                  className="w-full p-4 flex items-center justify-between text-left"
                >
                  <span className="text-white font-bold text-lg">{asset}</span>
                  {expandedAsset === asset ? (
                    <ChevronUp className="w-5 h-5 text-pink-400" />
                  ) : (
                    <ChevronDown className="w-5 h-5 text-pink-400" />
                  )}
                </button>
                
                {expandedAsset === asset && (
                  <div className="px-4 pb-4 pt-0">
                    <div className="border-t border-purple-500/30 pt-3">
                      <p className="text-white/80 text-sm leading-relaxed">
                        {assetDescriptions[asset] || 'Description non disponible'}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Info supplémentaire */}
        <div className="mt-8 text-center">
          <p className="text-white/60 text-sm">
            {language === 'fr' 
              ? 'Ces actifs sont disponibles sur notre canal Telegram VIP'
              : 'These assets are available on our VIP Telegram channel'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default CanalDetails;
