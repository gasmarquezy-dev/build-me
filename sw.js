const V='bm-v4';
const CORE=['./','./index.html','./manifest.webmanifest','./icons/icon-192.png','./icons/icon-512.png','./icons/apple-touch-icon.png'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(V).then(c=>c.addAll(CORE)).then(()=>self.skipWaiting()))});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(ks=>Promise.all(ks.filter(k=>k!==V).map(k=>caches.delete(k)))).then(()=>self.clients.claim()))});
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET')return;
  // data.json : toujours essayer le réseau d'abord (nouveau briefing), sinon la copie gardée
  if(u.pathname.endsWith('.json')){
    e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put(e.request,c));return r}).catch(()=>caches.match(e.request)));
    return;
  }
  if(e.request.mode==='navigate'){e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(V).then(x=>x.put('./index.html',c));return r}).catch(()=>caches.match('./index.html')));return}
  e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request).then(n=>{if(u.origin===location.origin||u.host.includes('fonts')){const c=n.clone();caches.open(V).then(x=>x.put(e.request,c))}return n})));
});
