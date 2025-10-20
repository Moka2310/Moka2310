// Service Worker for Tradalife PWA avec mise à jour automatique
const CACHE_VERSION = 'tradalife-v2.0';
const CACHE_NAME = CACHE_VERSION;

const STATIC_ASSETS = [
  '/',
  '/boutique',
  '/login',
  '/dashboard'
];

// Install - Skip waiting pour activer immédiatement
self.addEventListener('install', (event) => {
  console.log('[SW] Installation du Service Worker', CACHE_NAME);
  self.skipWaiting(); // Active immédiatement le nouveau SW
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Cache ouvert');
        // Essaie de mettre en cache, mais ne bloque pas si ça échoue
        return cache.addAll(STATIC_ASSETS).catch(err => {
          console.log('[SW] Erreur de cache initiale (non bloquant):', err);
        });
      })
  );
});

// Stratégie: Network First avec Cache Fallback
// Toujours essayer le réseau d'abord pour avoir le contenu le plus récent
self.addEventListener('fetch', (event) => {
  // Ignorer les requêtes non-GET
  if (event.request.method !== 'GET') {
    return;
  }

  // Ignorer les requêtes chrome-extension et autres
  if (!event.request.url.startsWith('http')) {
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((response) => {
        // Si la réponse est valide, la mettre en cache
        if (response && response.status === 200) {
          const responseClone = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Si le réseau échoue, utiliser le cache
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) {
            console.log('[SW] Utilisation du cache pour:', event.request.url);
            return cachedResponse;
          }
          // Si pas de cache, retourner une réponse d'erreur
          return new Response('Hors ligne - contenu non disponible', {
            status: 503,
            statusText: 'Service Unavailable',
            headers: new Headers({
              'Content-Type': 'text/plain'
            })
          });
        });
      })
  );
});

// Activate - Nettoyer les anciens caches et prendre le contrôle immédiatement
self.addEventListener('activate', (event) => {
  console.log('[SW] Activation du Service Worker', CACHE_NAME);
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW] Suppression ancien cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => {
      // Prendre le contrôle de toutes les pages immédiatement
      return self.clients.claim();
    })
  );
});

// Message pour forcer la mise à jour
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
});
