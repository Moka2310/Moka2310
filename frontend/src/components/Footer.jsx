import React from 'react';
import { Send, Shield, FileText } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { useLanguage } from '../contexts/LanguageContext';
import { t } from '../translations';

const Footer = () => {
  const { language } = useLanguage();
  const navigate = useNavigate();
  
  return (
    <footer className="bg-gradient-to-b from-[#1E1540] to-black py-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Protection Charter Section - Mise en valeur */}
        <div className="mb-12">
          <div className="charter-card-wrapper max-w-3xl mx-auto">
            <div className="charter-card-border"></div>
            <div 
              onClick={() => navigate('/protection-charter')}
              className="charter-card-content cursor-pointer group"
            >
              <div className="flex flex-col md:flex-row items-center justify-between gap-6">
                {/* Icône et texte */}
                <div className="flex items-center gap-4">
                  <div className="charter-icon-wrapper">
                    <Shield className="w-12 h-12 text-white" />
                  </div>
                  <div className="text-left">
                    <h3 className="text-2xl font-bold text-white mb-1 flex items-center gap-2">
                      {language === 'fr' ? 'Charte de Protection' : 'Protection Charter'}
                    </h3>
                    <p className="text-white/70 text-sm">
                      {language === 'fr' 
                        ? 'Votre sécurité et vos droits sont notre priorité' 
                        : 'Your security and rights are our priority'}
                    </p>
                  </div>
                </div>
                
                {/* Bouton CTA */}
                <div className="charter-button">
                  <FileText className="w-5 h-5" />
                  <span className="font-semibold">
                    {language === 'fr' ? 'Consulter' : 'View Charter'}
                  </span>
                  <svg className="w-5 h-5 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Social Links */}
        <div className="flex justify-center items-center mb-8">
          <a
            href="https://t.me/TRADALIFE"
            target="_blank"
            rel="noopener noreferrer"
            className="w-16 h-16 bg-gradient-to-br from-pink-500 to-purple-600 rounded-full flex items-center justify-center hover:scale-110 transition-transform shadow-lg shadow-pink-500/50"
          >
            <Send className="w-7 h-7 text-white" />
          </a>
        </div>

        {/* Copyright */}
        <div className="text-center">
          <p className="text-pink-500 font-semibold text-lg">
            {t(language, 'footer.rights')} © 2025
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;