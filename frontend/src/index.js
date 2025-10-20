import React from "react";
import ReactDOM from "react-dom/client";
import "@/index.css";
import App from "@/App";

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);

// Service Worker avec mise à jour automatique
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker
      .register('/service-worker.js')
      .then((registration) => {
        console.log('[App] Service Worker enregistré avec succès:', registration.scope);

        // Vérifier les mises à jour toutes les heures
        setInterval(() => {
          registration.update();
        }, 60 * 60 * 1000); // 1 heure

        // Écouter les mises à jour du Service Worker
        registration.addEventListener('updatefound', () => {
          const newWorker = registration.installing;
          console.log('[App] Nouvelle version du Service Worker détectée');

          newWorker.addEventListener('statechange', () => {
            if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
              // Nouvelle version disponible, activer automatiquement
              console.log('[App] Mise à jour disponible, activation automatique...');
              newWorker.postMessage({ type: 'SKIP_WAITING' });
              
              // Recharger la page après un court délai
              setTimeout(() => {
                window.location.reload();
              }, 1000);
            }
          });
        });
      })
      .catch((error) => {
        console.error('[App] Erreur lors de l\'enregistrement du Service Worker:', error);
      });

    // Recharger la page quand un nouveau Service Worker prend le contrôle
    let refreshing = false;
    navigator.serviceWorker.addEventListener('controllerchange', () => {
      if (!refreshing) {
        refreshing = true;
        console.log('[App] Nouveau Service Worker actif, rechargement...');
        window.location.reload();
      }
    });
  });
}
