// Simple service worker for eTax Mobile PWA
const CACHE_NAME = "etax-mobile-cache-v1";

const APP_SHELL = [
  "./",
  "./index.html",
  "./login.html",
  "./home.html",
  "./manifest.json",
  "./css/common.css",
  "./login.css",
  "./home.css",
  "./js/auth.js",
  "./js/utils.js",
  "./js/firebase-config.js",
  "./assets/logo-192.webp",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(APP_SHELL);
    })
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) =>
      Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      )
    )
  );
});

self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((response) => {
      return (
        response ||
        fetch(event.request).catch(() =>
          // Fallback to home page for navigation requests when offline
          event.request.mode === "navigate"
            ? caches.match("./home.html")
            : undefined
        )
      );
    })
  );
});


