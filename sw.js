/* WĐT AI — Service Worker
   Chiến lược:
   - App shell (index.html, manifest, icon): network-first có cache fallback → lên mạng được thì luôn mới, mất mạng vẫn mở app.
   - API giá (Binance, alternative.me): KHÔNG cache — luôn live, lỗi thì UI tự hiện "MẤT KẾT NỐI".
*/
const CACHE = "wdtai-v1";
const SHELL = [
  "./",
  "./index.html",
  "./manifest.json",
  "./icon-192.png",
  "./icon-512.png",
  "./apple-touch-icon.png",
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);

  /* API live: đi thẳng mạng, không cache */
  if (url.hostname.includes("binance.com") || url.hostname.includes("alternative.me")) {
    return; /* để mặc định */
  }

  /* App shell: mạng trước, cache sau (offline fallback) */
  if (e.request.mode === "navigate" || SHELL.some((s) => url.pathname.endsWith(s.replace("./", "/")) || url.pathname === s.replace("./", ""))) {
    e.respondWith(
      fetch(e.request)
        .then((res) => {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, copy));
          return res;
        })
        .catch(() => caches.match(e.request).then((hit) => hit || caches.match("./index.html")))
    );
  }
});
