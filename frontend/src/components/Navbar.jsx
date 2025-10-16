import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { ShoppingCart, Menu, X } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from './ui/button';

const Navbar = () => {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  const menuItems = [
    { label: 'Accueil', path: '/' },
    { label: 'Nos canaux', path: '#canaux' },
    { label: 'Nos applications', path: '#applications' },
    { label: 'Vidéos', path: '#videos' },
    { label: 'Contact', path: '#contact' },
    { label: 'Boutique', path: '/boutique' }
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
              className="h-16 w-auto"
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
            <div className="flex items-center space-x-2">
              <img src="https://flagcdn.com/w40/fr.png" alt="FR" className="w-6 h-4" />
            </div>

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
                Mon Panel
              </Button>
            ) : (
              <>
                <Button
                  onClick={() => navigate('/login')}
                  className="bg-transparent border border-pink-500 text-pink-500 hover:bg-pink-500 hover:text-white px-6 py-2 rounded-full transition-all"
                >
                  Connexion
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
            {user ? (
              <Button
                onClick={() => {
                  navigate('/dashboard');
                  setMobileMenuOpen(false);
                }}
                className="w-full bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white"
              >
                Mon Panel
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
                  Connexion
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