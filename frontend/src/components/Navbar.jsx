import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, Menu, X, Globe } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';
import { Button } from './ui/button';

const Navbar = () => {
  const { user } = useAuth();
  const { language, toggleLanguage } = useLanguage();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [showInstallButton, setShowInstallButton] = useState(false);

  // Detect if PWA can be installed
  useEffect(() => {
    const handleBeforeInstallPrompt = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
      setShowInstallButton(true);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Check if already installed
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches;
    const isIOSStandalone = window.navigator.standalone === true;
    
    if (!isStandalone && !isIOSStandalone) {
      // Show button after 2 seconds if not already shown
      setTimeout(() => {
        if (!deferredPrompt) {
          setShowInstallButton(true); // Always show on mobile devices
        }
      }, 2000);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstallClick = async () => {
    if (deferredPrompt) {
      // Chrome Android with beforeinstallprompt event
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      
      if (outcome === 'accepted') {
        setShowInstallButton(false);
      }
      
      setDeferredPrompt(null);
    } else {
      // iOS or browsers without beforeinstallprompt
      // Show instructions
      const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent);
      const instructions = isIOS 
        ? (language === 'fr' 
            ? "Sur iPhone/iPad : Appuyez sur le bouton Partager puis 'Sur l'écran d'accueil'"
            : "On iPhone/iPad: Tap the Share button then 'Add to Home Screen'")
        : (language === 'fr'
            ? "Pour installer : Menu Chrome (3 points) → 'Installer l'application'"
            : "To install: Chrome Menu (3 dots) → 'Install app'");
      
      alert(instructions);
    }
  };

  const menuItems = [
    { label: t(language, 'nav.home'), path: '/' },
    { label: t(language, 'nav.channels'), path: '#canaux' },
    { label: t(language, 'nav.applications'), path: '#applications' },
    { label: t(language, 'nav.videos'), path: '#videos' },
    { label: t(language, 'nav.contact'), path: '#contact' },
    { label: t(language, 'nav.shop'), path: '/boutique' }
  ];

  const scrollToSection = (hash) => {
    if (hash.startsWith('#')) {
      const element = document.querySelector(hash);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  };

  const handleNavClick = (path) => {
    if (path.startsWith('#')) {
      if (window.location.pathname !== '/') {
        navigate('/');
        setTimeout(() => scrollToSection(path), 100);
      } else {
        scrollToSection(path);
      }
    } else {
      navigate(path);
    }
    setMobileMenuOpen(false);
  };

  return (
    <nav className="fixed top-0 w-full bg-[#1E1540] z-50 border-b border-purple-800/30">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          {/* Logo */}
          <Link to="/" className="flex items-center">
            <img 
              src="https://i.imgur.com/FrA3lov.gif" 
              alt="Tradalife Logo" 
              className="h-24 w-auto"
            />
          </Link>

          {/* Desktop Menu */}
          <div className="hidden md:flex items-center space-x-8">
            {menuItems.map((item) => (
              <button
                key={item.path}
                onClick={() => handleNavClick(item.path)}
                className="text-white/90 hover:text-pink-400 transition-colors text-sm font-medium"
              >
                {item.label}
              </button>
            ))}

            {/* Language Selector */}
            <button
              onClick={toggleLanguage}
              className="flex items-center space-x-2 text-white/90 hover:text-pink-400 transition-colors px-3 py-1.5 rounded-lg hover:bg-white/5"
              title={language === 'fr' ? 'Switch to English (Canada)' : 'Passer en Français'}
            >
              <Globe className="w-4 h-4" />
              <span className="text-sm font-medium">{language === 'fr' ? '🇨🇦 EN' : '🇫🇷 FR'}</span>
            </button>

            {/* Install App Button */}
            {showInstallButton && (
              <button
                onClick={handleInstallClick}
                className="flex items-center space-x-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-4 py-2 rounded-full transition-all transform hover:scale-105"
                title={language === 'fr' ? 'Installer l\'application' : 'Install app'}
              >
                <span className="text-sm font-bold">App</span>
                <span className="text-sm font-medium hidden lg:inline">
                  {language === 'fr' ? 'Installer' : 'Install'}
                </span>
              </button>
            )}

            {/* Cart Icon */}
            <button
              onClick={() => navigate(user ? '/dashboard' : '/login')}
              className="text-white/90 hover:text-pink-400 transition-colors"
            >
              <ShoppingCart className="w-5 h-5" />
            </button>

            {/* Telegram Button or User Button */}
            {user ? (
              <Button
                onClick={() => navigate('/dashboard')}
                className="bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white px-6 py-2 rounded-full"
              >
                {t(language, 'nav.dashboard')}
              </Button>
            ) : (
              <>
                <Button
                  onClick={() => navigate('/login')}
                  className="bg-transparent border border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white px-6 py-2 rounded-full transition-all"
                >
                  {t(language, 'nav.login')}
                </Button>
                <Button
                  onClick={() => window.open('https://t.me/TRADALIFE', '_blank')}
                  className="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white px-6 py-2 rounded-full"
                >
                  TELEGRAM
                </Button>
              </>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden text-white"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>
      </div>

      {/* Mobile Menu */}
      {mobileMenuOpen && (
        <div className="md:hidden bg-[#1E1540] border-t border-purple-800/30">
          <div className="px-4 py-4 space-y-3">
            {menuItems.map((item) => (
              <button
                key={item.path}
                onClick={() => handleNavClick(item.path)}
                className="block w-full text-left text-white/90 hover:text-pink-400 transition-colors py-2"
              >
                {item.label}
              </button>
            ))}
            
            {/* Language Selector Mobile */}
            <button
              onClick={toggleLanguage}
              className="flex items-center space-x-2 text-white/90 hover:text-pink-400 transition-colors py-2 w-full"
            >
              <Globe className="w-4 h-4" />
              <span className="text-sm font-medium">{language === 'fr' ? '🇨🇦 English' : '🇫🇷 Français'}</span>
            </button>
            
            {/* Install App Button Mobile */}
            {showInstallButton && (
              <Button
                onClick={handleInstallClick}
                className="w-full bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white flex items-center justify-center space-x-2"
              >
                <span className="font-bold">App</span>
                <span>{language === 'fr' ? 'Installer l\'application' : 'Install app'}</span>
              </Button>
            )}
            
            {user ? (
              <Button
                onClick={() => {
                  navigate('/dashboard');
                  setMobileMenuOpen(false);
                }}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
              >
                {t(language, 'nav.dashboard')}
              </Button>
            ) : (
              <>
                <Button
                  onClick={() => {
                    navigate('/login');
                    setMobileMenuOpen(false);
                  }}
                  className="w-full bg-transparent border border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white"
                >
                  {t(language, 'nav.login')}
                </Button>
                <Button
                  onClick={() => window.open('https://t.me/TRADALIFE', '_blank')}
                  className="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white"
                >
                  TELEGRAM
                </Button>
              </>
            )}
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;