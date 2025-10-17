import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useLanguage } from '../contexts/LanguageContext';
import { Button } from './ui/button';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from './ui/dialog';
import { AlertTriangle, Shield } from 'lucide-react';

const ProtectedVideoPlayer = ({ videoUrl, title }) => {
  const { user } = useAuth();
  const { language } = useLanguage();
  const [agreed, setAgreed] = useState(false);
  const [showWarning, setShowWarning] = useState(true);

  const content = {
    fr: {
      warningTitle: "⚠️ Avertissement Important - Protection du Contenu",
      warning1: "Ce contenu vidéo est protégé et réservé EXCLUSIVEMENT à l'usage personnel de :",
      warning2: "Toute diffusion, reproduction, enregistrement ou partage de ce contenu est STRICTEMENT INTERDIT et constitue une violation de nos conditions d'utilisation.",
      warning3: "Les violations seront poursuivies conformément aux lois en vigueur sur la propriété intellectuelle.",
      warning4: "Un filigrane contenant vos informations est visible sur cette vidéo à des fins de traçabilité.",
      accept: "J'ai lu et j'accepte les conditions",
      watchVideo: "Regarder la vidéo",
      copyright: "© TRADALIFE - Tous droits réservés"
    },
    en: {
      warningTitle: "⚠️ Important Warning - Content Protection",
      warning1: "This video content is protected and reserved EXCLUSIVELY for personal use by:",
      warning2: "Any broadcasting, reproduction, recording or sharing of this content is STRICTLY PROHIBITED and constitutes a violation of our terms of use.",
      warning3: "Violations will be prosecuted in accordance with applicable intellectual property laws.",
      warning4: "A watermark containing your information is visible on this video for traceability purposes.",
      accept: "I have read and accept the terms",
      watchVideo: "Watch video",
      copyright: "© TRADALIFE - All rights reserved"
    }
  };

  const t = content[language];

  if (!agreed) {
    return (
      <div className="relative aspect-video bg-gradient-to-br from-[#2B1F5C] to-[#1E1540] rounded-xl border border-purple-500/30 flex items-center justify-center">
        <div className="text-center p-8 max-w-2xl">
          <div className="mb-6 flex justify-center">
            <div className="w-20 h-20 bg-yellow-500/20 rounded-full flex items-center justify-center">
              <AlertTriangle className="w-10 h-10 text-yellow-400" />
            </div>
          </div>
          
          <h3 className="text-2xl font-bold text-white mb-4">{t.warningTitle}</h3>
          
          <div className="bg-yellow-500/10 border border-yellow-500/30 rounded-xl p-6 mb-6 text-left space-y-4">
            <p className="text-white/90">
              <strong>{t.warning1}</strong>
            </p>
            <p className="text-pink-400 font-bold text-lg">
              {user?.firstName} {user?.lastName} ({user?.email})
            </p>
            <p className="text-white/90">
              {t.warning2}
            </p>
            <p className="text-white/90">
              {t.warning3}
            </p>
            <p className="text-white/90">
              <Shield className="inline w-4 h-4 mr-2" />
              {t.warning4}
            </p>
          </div>

          <div className="mb-6">
            <label className="flex items-center justify-center space-x-3 cursor-pointer">
              <input
                type="checkbox"
                checked={agreed}
                onChange={(e) => setAgreed(e.target.checked)}
                className="w-5 h-5 text-pink-500 bg-transparent border-2 border-pink-500/50 rounded focus:ring-pink-500"
              />
              <span className="text-white font-medium">{t.accept}</span>
            </label>
          </div>

          <Button
            onClick={() => setAgreed(true)}
            disabled={!agreed}
            className="bg-gradient-to-r from-pink-500 to-purple-600 hover:from-pink-600 hover:to-purple-700 text-white px-8 py-6 text-lg rounded-full disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {t.watchVideo}
          </Button>

          <p className="text-white/50 text-sm mt-6">{t.copyright}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="relative aspect-video rounded-xl overflow-hidden border border-purple-500/30">
      {/* Video with watermark overlay */}
      <iframe
        src={videoUrl}
        className="w-full h-full"
        allow="autoplay; encrypted-media"
        title={title}
      ></iframe>
      
      {/* Watermark Overlay - Always visible */}
      <div className="absolute top-4 right-4 bg-black/70 text-white/80 px-4 py-2 rounded-lg text-sm font-mono pointer-events-none">
        {user?.email}
      </div>
      
      {/* Additional watermark - Bottom Left */}
      <div className="absolute bottom-4 left-4 bg-black/70 text-white/80 px-4 py-2 rounded-lg text-sm font-mono pointer-events-none">
        {user?.firstName} {user?.lastName}
      </div>

      {/* Center watermark - Semi-transparent */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 text-white/10 text-6xl font-bold rotate-[-30deg] pointer-events-none whitespace-nowrap">
        {user?.email}
      </div>

      {/* Prevent right-click */}
      <div 
        className="absolute inset-0 pointer-events-auto"
        onContextMenu={(e) => e.preventDefault()}
        style={{ userSelect: 'none' }}
      />
    </div>
  );
};

export default ProtectedVideoPlayer;
