import React, { useState } from 'react';
import { Download, FileArchive, Book, CheckCircle, AlertCircle } from 'lucide-react';

const TradabotDownloadTab = () => {
  const [downloading, setDownloading] = useState(false);
  const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

  const handleDownload = () => {
    // Téléchargement direct du fichier statique
    const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
    window.location.href = `${BACKEND_URL}/TRADABOT_Package.zip`;
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-gradient-to-r from-green-500/20 to-emerald-600/20 rounded-3xl p-8 border border-green-500/30">
        <h2 className="text-3xl font-bold text-white mb-2 flex items-center">
          <Download className="w-8 h-8 mr-3" />
          Télécharger TRADABOT
        </h2>
        <p className="text-white/80">
          Package complet pour construire l'application Windows
        </p>
      </div>

      {/* Informations */}
      <div className="grid md:grid-cols-2 gap-6">
        <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <FileArchive className="w-6 h-6 mr-2 text-blue-400" />
            Contenu du Package
          </h3>
          <ul className="space-y-2 text-white/80">
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400 flex-shrink-0 mt-0.5" />
              <span>Code source complet de l'application</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400 flex-shrink-0 mt-0.5" />
              <span>Scripts de build automatisés</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400 flex-shrink-0 mt-0.5" />
              <span>200+ serveurs brokers pré-configurés</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400 flex-shrink-0 mt-0.5" />
              <span>Documentation complète en français</span>
            </li>
            <li className="flex items-start">
              <CheckCircle className="w-5 h-5 mr-2 text-green-400 flex-shrink-0 mt-0.5" />
              <span>Guide ultra-simple étape par étape</span>
            </li>
          </ul>
        </div>

        <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
          <h3 className="text-xl font-bold text-white mb-4 flex items-center">
            <AlertCircle className="w-6 h-6 mr-2 text-yellow-400" />
            Prérequis Windows
          </h3>
          <ul className="space-y-2 text-white/80">
            <li className="flex items-start">
              <span className="text-yellow-400 mr-2">•</span>
              <span>Windows 10 ou Windows 11 (64-bit)</span>
            </li>
            <li className="flex items-start">
              <span className="text-yellow-400 mr-2">•</span>
              <span>Python 3.11+ (gratuit, inclus dans le guide)</span>
            </li>
            <li className="flex items-start">
              <span className="text-yellow-400 mr-2">•</span>
              <span>MetaTrader 4 ou 5 (gratuit)</span>
            </li>
            <li className="flex items-start">
              <span className="text-yellow-400 mr-2">•</span>
              <span>Compte broker (démo ou réel)</span>
            </li>
            <li className="flex items-start">
              <span className="text-yellow-400 mr-2">•</span>
              <span>5-10 GB d'espace disque libre</span>
            </li>
          </ul>
        </div>
      </div>

      {/* Bouton de téléchargement */}
      <div className="bg-gradient-to-r from-blue-500/20 to-purple-600/20 rounded-3xl p-8 border border-blue-500/30 text-center">
        <h3 className="text-2xl font-bold text-white mb-4">
          Prêt à construire TRADABOT?
        </h3>
        <p className="text-white/80 mb-6">
          Téléchargez le package complet et suivez le guide ultra-simple!
        </p>
        <button
          onClick={handleDownload}
          className="bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white px-8 py-4 rounded-xl font-bold text-lg transition-all flex items-center justify-center mx-auto"
        >
          <Download className="w-6 h-6 mr-3" />
          TÉLÉCHARGER LE PACKAGE
        </button>
        <p className="text-white/60 text-sm mt-4">
          Taille: ~5-10 MB | Format: ZIP
        </p>
      </div>

      {/* Instructions rapides */}
      <div className="bg-white/5 rounded-2xl p-6 border border-white/10">
        <h3 className="text-xl font-bold text-white mb-4 flex items-center">
          <Book className="w-6 h-6 mr-2 text-purple-400" />
          Instructions Rapides
        </h3>
        <div className="space-y-4 text-white/80">
          <div className="flex items-start">
            <span className="bg-purple-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mr-3 font-bold">
              1
            </span>
            <div>
              <p className="font-semibold text-white">Télécharger le package</p>
              <p className="text-sm">Cliquez sur le bouton ci-dessus</p>
            </div>
          </div>
          <div className="flex items-start">
            <span className="bg-purple-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mr-3 font-bold">
              2
            </span>
            <div>
              <p className="font-semibold text-white">Extraire le ZIP</p>
              <p className="text-sm">Clic droit → "Extraire tout"</p>
            </div>
          </div>
          <div className="flex items-start">
            <span className="bg-purple-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mr-3 font-bold">
              3
            </span>
            <div>
              <p className="font-semibold text-white">Ouvrir GUIDE_ULTRA_SIMPLE.md</p>
              <p className="text-sm">Suivre les étapes une par une</p>
            </div>
          </div>
          <div className="flex items-start">
            <span className="bg-purple-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mr-3 font-bold">
              4
            </span>
            <div>
              <p className="font-semibold text-white">Construire l'application</p>
              <p className="text-sm">Exécuter: python build_windows.py</p>
            </div>
          </div>
          <div className="flex items-start">
            <span className="bg-green-500 text-white rounded-full w-8 h-8 flex items-center justify-center flex-shrink-0 mr-3 font-bold">
              ✓
            </span>
            <div>
              <p className="font-semibold text-white">Lancer TRADABOT.exe</p>
              <p className="text-sm">L'application est prête!</p>
            </div>
          </div>
        </div>
      </div>

      {/* Aide */}
      <div className="bg-yellow-500/10 rounded-2xl p-6 border border-yellow-500/30">
        <h3 className="text-lg font-bold text-white mb-2">
          💡 Besoin d'aide?
        </h3>
        <p className="text-white/80 text-sm">
          Le guide ultra-simple contient toutes les instructions détaillées avec captures d'écran.
          Si vous rencontrez un problème, contactez: <strong>yafoy2310@gmail.com</strong>
        </p>
      </div>
    </div>
  );
};

export default TradabotDownloadTab;
