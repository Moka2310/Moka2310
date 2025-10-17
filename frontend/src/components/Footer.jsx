import React from 'react';
import { Send, Facebook, Shield } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const Footer = () => {
  const { language } = useLanguage();
  const navigate = useNavigate();
  
  return (
    <footer className="bg-gradient-to-b from-[#1E1540] to-black py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-center items-center space-x-8 mb-8">
          {/* Telegram */}
          <a
            href="https://t.me/TRADALIFE"
            target="_blank"
            rel="noopener noreferrer"
            className="w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center hover:scale-110 transition-transform"
          >
            <Send className="w-7 h-7 text-white" />
          </a>

          {/* Facebook */}
          <a
            href="https://www.facebook.com/profile.php?id=61568614032065"
            target="_blank"
            rel="noopener noreferrer"
            className="w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center hover:scale-110 transition-transform"
          >
            <Facebook className="w-7 h-7 text-white" />
          </a>
        </div>

        <div className="text-center space-y-4">
          <div>
            <button
              onClick={() => navigate('/protection-charter')}
              className="text-pink-400 hover:text-pink-300 transition-colors inline-flex items-center space-x-2"
            >
              <Shield className="w-4 h-4" />
              <span>{language === 'fr' ? 'Charte de Protection' : 'Protection Charter'}</span>
            </button>
          </div>
          <p className="text-pink-500 font-semibold text-lg">
            {t(language, 'footer.rights')} © 2025
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;