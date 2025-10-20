import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { canaux, stats } from '../mockData';
import { Check, Download, Star } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import ChatWidget from '../components/ChatWidget';
 
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const navigate = useNavigate();
  const { language } = useLanguage();
  const [testimonials, setTestimonials] = useState([]);
  const [telegramMembers, setTelegramMembers] = useState(4000); // Valeur par défaut
  
  const [contactForm, setContactForm] = useState({
    firstName: '',
    lastName: '',
    email: '',
    message: ''
  });

  // Load Telegram members count
  useEffect(() => {
    const loadTelegramMembers = async () => {
      try {
        const response = await fetch(`${API}/telegram/member-count`);
        const data = await response.json();
        if (data.count) {
          setTelegramMembers(data.count);
        }
      } catch (error) {
        console.error('Error loading Telegram members:', error);
        // Garder la valeur par défaut en cas d'erreur
      }
    };
    loadTelegramMembers();
  }, []);

  // Load testimonials
  useEffect(() => {
    const loadTestimonials = async () => {
      try {
        const response = await axios.get(`${API}/testimonials/approved`);
        setTestimonials(response.data);
      } catch (error) {
        console.error('Failed to load testimonials:', error);
      }
    };
    loadTestimonials();
  }, []);

  const handleContactSubmit = (e) => {
    e.preventDefault();
    toast({
      title: language === 'fr' ? 'Message envoyé !' : 'Message sent!',
      description: language === 'fr' ? 'Nous vous répondrons dans les plus brefs délais.' : 'We will respond to you shortly.'
    });
    setContactForm({ firstName: '', lastName: '', email: '', message: '' });
  };

  return (
    <div className="min-h-screen bg-[#1E1540]">
      {/* Hero Section */}
      <section className="pt-32 pb-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left Side - Text */}
            <div>
              <h1 className="text-4xl md:text-5xl font-bold text-white mb-6 leading-tight">
                {language === 'fr' ? 'Bienvenue chez' : 'Welcome to'} <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">TRADALIFE</span>
              </h1>
              <p className="text-white/80 text-lg mb-8">
                {language === 'fr' 
                  ? 'Rejoignez notre communauté de plus de 4000 traders et accédez à des signaux exclusifs sur Crypto, Forex, Gold, Indices et plus encore.'
                  : 'Join our community of over 4000 traders and access exclusive signals on Crypto, Forex, Gold, Indices and more.'
                }
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  onClick={() => navigate('/boutique')}
                  className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-6 text-lg rounded-full"
                >
                  {language === 'fr' ? 'Découvrir nos formations' : 'Explore Our Courses'}
                </Button>
                <Button
                  onClick={() => window.open('https://t.me/TRADALIFE', '_blank')}
                  className="bg-transparent border-2 border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white px-8 py-6 text-lg rounded-full transition-all"
                >
                  {language === 'fr' ? 'Rejoindre Telegram' : 'Join Telegram'}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Video Banner - Groupe TRADALIFE HD Full avec cadre lumineux */}
      <section className="w-full overflow-hidden bg-black relative py-12">
        <div className="max-w-7xl mx-auto px-4">
          {/* Conteneur avec animation lumineuse */}
          <div className="relative rounded-3xl overflow-hidden video-frame-glow">
            {/* Cadre animé avec bordure lumineuse */}
            <div className="absolute inset-0 rounded-3xl p-[3px] animated-border">
              <div className="w-full h-full bg-black rounded-3xl"></div>
            </div>
            
            {/* Vidéo */}
            <div className="relative w-full rounded-3xl overflow-hidden" style={{ height: '600px' }}>
              <div className="absolute inset-0 overflow-hidden rounded-3xl">
                <iframe
                  src="https://www.youtube.com/embed/kIpu18ACAXc?autoplay=1&mute=1&loop=1&playlist=kIpu18ACAXc&controls=0&showinfo=0&modestbranding=1&rel=0&iv_load_policy=3&disablekb=1&vq=hd1080&playsinline=1"
                  className="absolute top-1/2 left-1/2"
                  style={{
                    width: '177.77vh',
                    height: '100vh',
                    minWidth: '100%',
                    minHeight: '100%',
                    transform: 'translate(-50%, -50%) scale(1.3)',
                    border: 'none',
                    pointerEvents: 'none'
                  }}
                  allow="autoplay; encrypted-media"
                  allowFullScreen
                  playsInline
                  title="Groupe TRADALIFE"
                ></iframe>
              </div>
              {/* Overlay avec lueur subtile */}
              <div className="absolute inset-0 bg-gradient-to-b from-[#1E1540]/10 via-transparent to-[#1E1540]/10 pointer-events-none"></div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission & Why Choose Us Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <div className="grid md:grid-cols-2 gap-16">
            {/* Notre Mission */}
            <div>
              <h2 className="text-3xl font-bold mb-6">
                <span className="text-pink-500">●</span>{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                  {language === 'fr' ? 'Notre Mission' : 'Our Mission'}
                </span>
              </h2>
              <div className="space-y-4 text-white/80 leading-relaxed">
                <p>
                  {language === 'fr' 
                    ? <><strong className="text-white">TRADALIFE</strong>, notre mission est de rendre le trading accessible, transparent et performant pour tous.</>
                    : <>At <strong className="text-white">TRADALIFE</strong>, our mission is to make trading accessible, transparent and efficient for everyone.</>
                  }
                </p>
                <p>
                  {language === 'fr'
                    ? 'Nous croyons que chaque trader, qu\'il soit débutant ou expérimenté, mérite d\'avoir les bons outils, un accompagnement personnalisé et une véritable stratégie pour réussir sur les marchés financiers.'
                    : 'We believe that every trader, whether beginner or experienced, deserves to have the right tools, personalized support and a real strategy to succeed in financial markets.'
                  }
                </p>
                <p>
                  {language === 'fr'
                    ? 'Notre objectif est d\'aider nos membres à développer leur autonomie, à maîtriser les bases du trading et à atteindre une rentabilité durable grâce à une approche structurée, éducative et réaliste.'
                    : 'Our goal is to help our members develop their autonomy, master the basics of trading and achieve sustainable profitability through a structured, educational and realistic approach.'
                  }
                </p>
                <p>
                  {language === 'fr'
                    ? <>Au-delà du trading, TRADALIFE est une <strong className="text-white">communauté internationale</strong> unie par une même passion : apprendre, partager et grandir ensemble.</>
                    : <>Beyond trading, TRADALIFE is an <strong className="text-white">international community</strong> united by the same passion: learning, sharing and growing together.</>
                  }
                </p>
              </div>
            </div>

            {/* Pourquoi Nous Choisir */}
            <div>
              <h2 className="text-3xl font-bold mb-6">
                <span className="text-pink-500">●</span>{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
                  {language === 'fr' ? 'Pourquoi Nous Choisir' : 'Why Choose Us'}
                </span>
              </h2>
              <p className="text-white/80 mb-6">
                {language === 'fr'
                  ? 'Nous mettons à votre disposition des outils performants, une équipe expérimentée et un accompagnement constant, afin que vous puissiez trader avec confiance, même dans les marchés les plus volatils.'
                  : 'We provide you with powerful tools, an experienced team and constant support, so you can trade with confidence, even in the most volatile markets.'
                }
              </p>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Check className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-white font-semibold mb-1">
                      {language === 'fr' ? 'Accompagnement personnalisé' : 'Personalized Support'}
                    </h3>
                    <p className="text-white/70 text-sm">
                      {language === 'fr'
                        ? 'Nos membres bénéficient d\'un suivi privé via WhatsApp, ainsi que d\'un accès à plusieurs canaux spécialisés (Gold, Forex, Crypto, Indices, Commodités, Actions).'
                        : 'Our members benefit from private monitoring via WhatsApp, as well as access to several specialized channels (Gold, Forex, Crypto, Indices, Commodities, Stocks).'
                      }
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Check className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-white font-semibold mb-1">
                      {language === 'fr' ? 'Communauté active et bienveillante' : 'Active and Caring Community'}
                    </h3>
                    <p className="text-white/70 text-sm">
                      {language === 'fr'
                        ? 'Avec plus de 4 000 membres à travers le monde, TRADALIFE est une famille de traders passionnés qui s\'entraident, partagent leurs analyses et évoluent ensemble.'
                        : 'With over 4,000 members worldwide, TRADALIFE is a family of passionate traders who help each other, share their analysis and grow together.'
                      }
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Check className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-white font-semibold mb-1">
                      {language === 'fr' ? 'Opportunités exclusives' : 'Exclusive Opportunities'}
                    </h3>
                    <p className="text-white/70 text-sm">
                      {language === 'fr'
                        ? 'Grâce à nos partenariats avec des brokers reconnus, nos membres profitent de conditions de trading avantageuses et d\'un accès privilégié à des formations premium.'
                        : 'Thanks to our partnerships with recognized brokers, our members enjoy advantageous trading conditions and privileged access to premium training.'
                      }
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section - Redesigned */}
      <section className="py-20 px-4 bg-gradient-to-b from-transparent to-[#2B1F5C]/30">
        <div className="max-w-7xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
              {language === 'fr' ? 'TRADALIFE en Chiffres' : 'TRADALIFE in Numbers'}
            </span>
          </h2>
          <p className="text-white/70 text-center mb-12">
            {language === 'fr' ? 'Notre communauté grandit chaque jour' : 'Our community grows every day'}
          </p>
          
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {stats.map((stat, index) => (
              <div key={index} className="stat-card-wrapper">
                {/* Bordure lumineuse */}
                <div className="stat-card-border"></div>
                
                {/* Contenu de la carte */}
                <div className="stat-card-content group">
                  <div className="relative z-10">
                    {/* Icône décorative */}
                    <div className="stat-icon-wrapper mb-4">
                      {stat.label === 'de taux de réussite' && (
                        <TrendingUp className="w-10 h-10 text-green-400" />
                      )}
                      {stat.label === 'Membres actifs' && (
                        <Users className="w-10 h-10 text-blue-400" />
                      )}
                      {stat.label === 'Canaux V.I.P' && (
                        <Star className="w-10 h-10 text-yellow-400" />
                      )}
                      {stat.label === 'Positions par jour' && (
                        <BarChart3 className="w-10 h-10 text-purple-400" />
                      )}
                      {stat.label === 'Brokers partenaires' && (
                        <Handshake className="w-10 h-10 text-pink-400" />
                      )}
                      {stat.label === 'ans sur le marché financier' && (
                        <Calendar className="w-10 h-10 text-indigo-400" />
                      )}
                    </div>
                    
                    {/* Valeur */}
                    <h3 className="text-5xl md:text-6xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 via-purple-400 to-blue-400 mb-3 leading-tight">
                      {stat.label === 'Membres actifs' 
                        ? `+${telegramMembers.toLocaleString('fr-FR')}`
                        : stat.value
                      }
                    </h3>
                    
                    {/* Label */}
                    <p className="text-white font-semibold text-lg mb-1">{stat.label}</p>
                    {stat.sublabel && (
                      <p className="text-white/60 text-sm">{stat.sublabel}</p>
                    )}
                    
                    {/* Badge "Live" pour les membres actifs */}
                    {stat.label === 'Membres actifs' && (
                      <div className="flex items-center justify-center gap-2 mt-3">
                        <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                        <span className="text-green-400 text-xs font-semibold">LIVE</span>
                      </div>
                    )}
                  </div>
                  
                  {/* Effet de brillance au hover */}
                  <div className="stat-shine"></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Canaux Section */}
      <section id="canaux" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
              {language === 'fr' ? 'Nos Canaux' : 'Our Channels'}
            </span>
          </h2>
          <p className="text-white/70 text-center mb-12">
            {language === 'fr' ? 'Découvrez nos 6 canaux d\'actifs' : 'Discover our 6 asset channels'}
          </p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {canaux.map((canal, index) => (
              <div
                key={index}
                onClick={() => navigate(`/canal/${canal.name.toLowerCase()}`)}
                className="canal-card-wrapper cursor-pointer"
              >
                {/* Bordure lumineuse animée */}
                <div className="canal-card-border"></div>
                
                {/* Contenu de la carte */}
                <div className="canal-card-content group relative overflow-hidden rounded-2xl aspect-square hover:scale-105 transition-all duration-300">
                  <img
                    src={canal.icon}
                    alt={canal.name}
                    className="w-full h-full object-cover"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex items-end justify-center pb-4">
                    <span className="text-white font-bold text-lg">{canal.name}</span>
                  </div>
                  
                  {/* Indicateur de clic */}
                  <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                    <div className="bg-white/20 backdrop-blur-sm rounded-full p-2">
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Applications Section */}
      <section id="applications" className="py-20 px-4 bg-gradient-to-b from-transparent to-[#2B1F5C]/30">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
              {language === 'fr' ? 'Nos Applications' : 'Our Applications'}
            </span>
          </h2>
          <p className="text-white/70 text-center mb-12">
            {language === 'fr' ? 'Découvrez nos applications de trading' : 'Discover our trading applications'}
          </p>
          <div className="grid md:grid-cols-2 gap-12 max-w-4xl mx-auto">
            <div className="bg-[#2B1F5C]/50 rounded-3xl overflow-hidden border border-purple-500/30 hover:border-pink-500/50 transition-all">
              <img
                src="https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=375,fit=crop/A3Ql90nqlVUN4Xox/mt5-mnl48DXPlJCVGqqv.jpg"
                alt="MetaTrader 5"
                className="w-full h-64 object-cover"
              />
              <div className="p-6">
                <h3 className="text-2xl font-bold text-white mb-4">Metatrader 5</h3>
                <a
                  href="https://play.google.com/store/apps/details?id=net.metaquotes.metatrader5"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-2 text-pink-400 hover:text-pink-300 transition-colors"
                >
                  <Download className="w-5 h-5" />
                  <span>{language === 'fr' ? 'Lien de téléchargement' : 'Download link'}</span>
                </a>
              </div>
            </div>
            <div className="bg-[#2B1F5C]/50 rounded-3xl overflow-hidden border border-purple-500/30 hover:border-pink-500/50 transition-all">
              <img
                src="https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=375,h=375,fit=crop/A3Ql90nqlVUN4Xox/mt4-YbN4LQ6z5PUbGVO5.jpg"
                alt="MetaTrader 4"
                className="w-full h-64 object-cover"
              />
              <div className="p-6">
                <h3 className="text-2xl font-bold text-white mb-4">Metatrader 4</h3>
                <a
                  href="https://play.google.com/store/apps/details?id=net.metaquotes.metatrader4"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center space-x-2 text-pink-400 hover:text-pink-300 transition-colors"
                >
                  <Download className="w-5 h-5" />
                  <span>{language === 'fr' ? 'Lien de téléchargement' : 'Download link'}</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <section className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">
              {language === 'fr' ? 'Témoignages de nos clients' : 'Client Testimonials'}
            </span>
          </h2>
          <p className="text-white/70 text-center mb-12">
            {language === 'fr' ? 'Découvrez ce que nos clients disent de nous' : 'Discover what our clients say about us'}
          </p>

          {testimonials.length > 0 ? (
            <div className="grid md:grid-cols-3 gap-6">
              {testimonials.slice(0, 6).map((testimonial) => (
                <div
                  key={testimonial.id}
                  className="bg-gradient-to-b from-[#2B1F5C] to-[#1E1540] rounded-3xl p-6 border border-purple-500/30 hover:border-pink-500/50 transition-all"
                >
                  {/* Stars Rating */}
                  <div className="flex space-x-1 mb-4">
                    {[...Array(5)].map((_, index) => (
                      <Star
                        key={index}
                        className={`w-5 h-5 ${
                          index < testimonial.rating
                            ? 'text-yellow-400 fill-yellow-400'
                            : 'text-gray-600'
                        }`}
                      />
                    ))}
                  </div>

                  {/* Comment */}
                  <p className="text-white/80 mb-4 italic">"{testimonial.comment}"</p>

                  {/* Author */}
                  <div className="border-t border-purple-500/30 pt-4">
                    <p className="text-white font-semibold">{testimonial.userName}</p>
                    <p className="text-pink-400 text-sm">{testimonial.country}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-white/70 py-12">
              <p>{language === 'fr' ? 'Aucun témoignage pour le moment' : 'No testimonials yet'}</p>
            </div>
          )}
        </div>
      </section>

 

      {/* Contact Section */}
      <section id="contact" className="py-20 px-4 bg-gradient-to-b from-transparent to-[#2B1F5C]/30">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Contact</span>
          </h2>
          <p className="text-white/70 text-center mb-12">
            {language === 'fr' ? 'Nous sommes là pour vous' : 'We are here for you'}
          </p>
          <form onSubmit={handleContactSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <Input
                  type="text"
                  placeholder={language === 'fr' ? 'Prénom*' : 'First Name*'}
                  required
                  value={contactForm.firstName}
                  onChange={(e) => setContactForm({ ...contactForm, firstName: e.target.value })}
                  className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                />
              </div>
              <div>
                <Input
                  type="text"
                  placeholder={language === 'fr' ? 'Nom*' : 'Last Name*'}
                  required
                  value={contactForm.lastName}
                  onChange={(e) => setContactForm({ ...contactForm, lastName: e.target.value })}
                  className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                />
              </div>
            </div>
            <div>
              <Input
                type="email"
                placeholder={language === 'fr' ? 'Votre email*' : 'Your email*'}
                required
                value={contactForm.email}
                onChange={(e) => setContactForm({ ...contactForm, email: e.target.value })}
                className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
              />
            </div>
            <div>
              <Textarea
                placeholder="Message*"
                required
                rows={5}
                value={contactForm.message}
                onChange={(e) => setContactForm({ ...contactForm, message: e.target.value })}
                className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500 resize-none"
              />
            </div>
            <div className="text-center">
              <Button
                type="submit"
                className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-12 py-6 text-lg rounded-full"
              >
                {language === 'fr' ? 'Envoyer' : 'Send'}
              </Button>
            </div>
          </form>
        </div>
      </section>

      {/* Chat Widget */}
      <ChatWidget />
    </div>
  );
};

export default Home;