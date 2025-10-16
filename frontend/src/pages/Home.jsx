import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { canaux, stats } from '../mockData';
import { Check, Download, Maximize2 } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Textarea } from '../components/ui/textarea';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '../components/ui/dialog';
import { toast } from '../hooks/use-toast';
import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const Home = () => {
  const navigate = useNavigate();
  const [videos, setVideos] = useState([]);
  const [selectedVideo, setSelectedVideo] = useState(null);
  const [isVideoModalOpen, setIsVideoModalOpen] = useState(false);
  const [contactForm, setContactForm] = useState({
    firstName: '',
    lastName: '',
    email: '',
    message: ''
  });

  useEffect(() => {
    // Load videos from backend
    const loadVideos = async () => {
      try {
        // For now, load from MongoDB directly - we'll create an API endpoint later
        // Using mock for now until we add the endpoint
      } catch (error) {
        console.error('Failed to load videos:', error);
      }
    };
    loadVideos();
  }, []);

  const openVideoModal = (video) => {
    setSelectedVideo(video);
    setIsVideoModalOpen(true);
  };

  const closeVideoModal = () => {
    setIsVideoModalOpen(false);
    setSelectedVideo(null);
  };

  const handleContactSubmit = (e) => {
    e.preventDefault();
    toast({
      title: 'Message envoyé !',
      description: 'Nous vous répondrons dans les plus brefs délais.'
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
                Bienvenue chez <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">TRADALIFE</span>
              </h1>
              <p className="text-white/80 text-lg mb-8">
                Rejoignez notre communauté de plus de 4000 traders et accédez à des signaux exclusifs sur Crypto, Forex, Gold, Indices et plus encore.
              </p>
              <div className="flex flex-col sm:flex-row gap-4">
                <Button
                  onClick={() => navigate('/boutique')}
                  className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-6 text-lg rounded-full"
                >
                  Découvrir nos formations
                </Button>
                <Button
                  onClick={() => window.open('https://t.me/TRADALIFE', '_blank')}
                  className="bg-transparent border-2 border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white px-8 py-6 text-lg rounded-full transition-all"
                >
                  Rejoindre Telegram
                </Button>
              </div>
            </div>

            {/* Right Side - Image */}
            <div className="relative">
              <div className="rounded-3xl overflow-hidden shadow-2xl shadow-pink-500/20">
                <img
                  src="https://assets.zyrosite.com/cdn-cgi/image/format=auto,w=768,h=442,fit=crop,trim=70.87350835322195;0;70.87350835322195;0/A3Ql90nqlVUN4Xox/chatgpt-image-9-oct.-2025-21-h-47-min-36-s-AVLx81l6vNtvoNEx.png"
                  alt="Tradalife Team"
                  className="w-full h-auto"
                />
              </div>
              <div className="absolute -top-6 -left-6 w-24 h-24 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full blur-2xl opacity-60"></div>
              <div className="absolute -bottom-6 -right-6 w-32 h-32 bg-gradient-to-br from-purple-500 to-blue-600 rounded-full blur-2xl opacity-60"></div>
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
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Notre Mission</span>
              </h2>
              <div className="space-y-4 text-white/80 leading-relaxed">
                <p>
                  Chez <strong className="text-white">TRADALIFE</strong>, notre mission est de rendre le trading accessible, transparent et performant pour tous.
                </p>
                <p>
                  Nous croyons que chaque trader, qu'il soit débutant ou expérimenté, mérite d'avoir les bons outils, un accompagnement personnalisé et une véritable stratégie pour réussir sur les marchés financiers.
                </p>
                <p>
                  Notre objectif est d'aider nos membres à développer leur autonomie, à maîtriser les bases du trading et à atteindre une rentabilité durable grâce à une approche structurée, éducative et réaliste.
                </p>
                <p>
                  Au-delà du trading, TRADALIFE est une <strong className="text-white">communauté internationale</strong> unie par une même passion : apprendre, partager et grandir ensemble.
                </p>
              </div>
            </div>

            {/* Pourquoi Nous Choisir */}
            <div>
              <h2 className="text-3xl font-bold mb-6">
                <span className="text-pink-500">●</span>{' '}
                <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Pourquoi Nous Choisir</span>
              </h2>
              <p className="text-white/80 mb-6">
                Nous mettons à votre disposition des outils performants, une équipe expérimentée et un accompagnement constant, afin que vous puissiez trader avec confiance, même dans les marchés les plus volatils.
              </p>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <Check className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-white font-semibold mb-1">Accompagnement personnalisé</h3>
                    <p className="text-white/70 text-sm">
                      Nos membres bénéficient d'un suivi privé via WhatsApp, ainsi que d'un accès à plusieurs canaux spécialisés (Gold, Forex, Crypto, Indices, Commodités, Actions).
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Check className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-white font-semibold mb-1">Communauté active et bienveillante</h3>
                    <p className="text-white/70 text-sm">
                      Avec plus de 4 000 membres à travers le monde, TRADALIFE est une famille de traders passionnés qui s'entraident, partagent leurs analyses et évoluent ensemble.
                    </p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <Check className="w-5 h-5 text-green-400 mt-1 flex-shrink-0" />
                  <div>
                    <h3 className="text-white font-semibold mb-1">Opportunités exclusives</h3>
                    <p className="text-white/70 text-sm">
                      Grâce à nos partenariats avec des brokers reconnus, nos membres profitent de conditions de trading avantageuses et d'un accès privilégié à des formations premium.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-20 px-4 bg-gradient-to-b from-transparent to-[#2B1F5C]/30">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
            {stats.map((stat, index) => (
              <div key={index} className="text-center">
                <h3 className="text-4xl md:text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400 mb-2">
                  {stat.value}
                </h3>
                <p className="text-white font-semibold">{stat.label}</p>
                {stat.sublabel && <p className="text-white/60 text-sm">{stat.sublabel}</p>}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Canaux Section */}
      <section id="canaux" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Nos Canaux</span>
          </h2>
          <p className="text-white/70 text-center mb-12">Découvrez nos 6 canaux d'actifs</p>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-6">
            {canaux.map((canal, index) => (
              <div
                key={index}
                className="group relative overflow-hidden rounded-2xl aspect-square hover:scale-105 transition-transform duration-300 cursor-pointer"
              >
                <img
                  src={canal.icon}
                  alt={canal.name}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent flex items-end justify-center pb-4">
                  <span className="text-white font-bold text-lg">{canal.name}</span>
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
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Nos Applications</span>
          </h2>
          <p className="text-white/70 text-center mb-12">Découvrez nos applications de trading</p>
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
                  <span>Lien de téléchargement</span>
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
                  <span>Lien de téléchargement</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Videos Section */}
      <section id="videos" className="py-20 px-4">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Vidéos</span>
          </h2>
          <p className="text-white/70 text-center mb-12">Découvrez nos tutoriels vidéo</p>
          
          <div className="grid md:grid-cols-3 gap-8">
            {/* Video 1 */}
            <div className="bg-[#2B1F5C]/50 rounded-3xl overflow-hidden border border-purple-500/30 hover:border-pink-500/50 transition-all">
              <div className="aspect-video">
                <iframe
                  src="https://drive.google.com/file/d/1gRDkNANoag2efegjIaQx1gPt-MI-VLve/preview"
                  className="w-full h-full"
                  allow="autoplay"
                  title="Comment ouvrir votre compte GlobalPrime"
                ></iframe>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-bold text-white mb-2">Comment ouvrir votre compte GlobalPrime</h3>
                <p className="text-white/70 text-sm">Guide complet pour créer et configurer votre compte de trading</p>
              </div>
            </div>

            {/* Video 2 */}
            <div className="bg-[#2B1F5C]/50 rounded-3xl overflow-hidden border border-purple-500/30 hover:border-pink-500/50 transition-all">
              <div className="aspect-video">
                <iframe
                  src="https://drive.google.com/file/d/1q5e7vg7SeuLebmShKeZ2jGC9S7FnDpwT/preview"
                  className="w-full h-full"
                  allow="autoplay"
                  title="Comment connecter son compte à MetaTrader 4"
                ></iframe>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-bold text-white mb-2">Comment connecter son compte à MetaTrader 4</h3>
                <p className="text-white/70 text-sm">Tutoriel pas à pas pour connecter votre compte à la plateforme MT4</p>
              </div>
            </div>

            {/* Video 3 */}
            <div className="bg-[#2B1F5C]/50 rounded-3xl overflow-hidden border border-purple-500/30 hover:border-pink-500/50 transition-all">
              <div className="aspect-video">
                <iframe
                  src="https://drive.google.com/file/d/13Rqhtq1fXkfGoGHIX65ToCeFjbhRnNUO/preview"
                  className="w-full h-full"
                  allow="autoplay"
                  title="Aperçu du contenu de notre groupe Telegram"
                ></iframe>
              </div>
              <div className="p-6">
                <h3 className="text-xl font-bold text-white mb-2">Aperçu du contenu de notre groupe Telegram</h3>
                <p className="text-white/70 text-sm">Découvrez ce que vous recevrez dans nos canaux VIP</p>
              </div>
            </div>
          </div>

          <div className="text-center mt-12">
            <Button
              onClick={() => window.open('https://globalprime.com/?refcode=83247', '_blank')}
              className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-4 text-lg rounded-full"
            >
              Ouvrir un compte GlobalPrime
            </Button>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 px-4 bg-gradient-to-b from-transparent to-[#2B1F5C]/30">
        <div className="max-w-2xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-purple-400">Contact</span>
          </h2>
          <p className="text-white/70 text-center mb-12">Nous sommes là pour vous</p>
          <form onSubmit={handleContactSubmit} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <div>
                <Input
                  type="text"
                  placeholder="Prénom*"
                  required
                  value={contactForm.firstName}
                  onChange={(e) => setContactForm({ ...contactForm, firstName: e.target.value })}
                  className="bg-white/10 border-purple-500/30 text-white placeholder:text-white/50 focus:border-pink-500"
                />
              </div>
              <div>
                <Input
                  type="text"
                  placeholder="Nom*"
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
                placeholder="Votre email*"
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
                className="bg-white text-[#1E1540] hover:bg-white/90 px-12 py-6 text-lg rounded-full font-semibold"
              >
                Envoyer
              </Button>
            </div>
          </form>
        </div>
      </section>
    </div>
  );
};

export default Home;