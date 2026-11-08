/* AXEZENT persistent public display counters for a static GitHub Pages site.
   One website session hit per browser tab/session; one successful first playback
   per song per session. Not unique humans, fraud-proof sales metrics, or DRM.
   This service is independent of GitHub Pages; do not expose personal data,
   tokens or passwords. The public provider may be unavailable or reset data. */
(() => {
  "use strict";
  const ENDPOINT = "https://countapi.mileshilliard.com/api/v1";
  const PREFIX = "axezent_beats_for_sale_20261108";
  const DELAY_MS = 360;
  const cache = new Map();
  const pending = new Set();
  const subscribers = new Map();
  const queue = [];
  let draining = false;
  const asCount = (x) => Number.isSafeInteger(x) && x >= 0 ? x : null;
  const format = x => Number.isSafeInteger(x) ? x.toLocaleString("en-US") : "—";
  const keyFor = id => PREFIX + "_plays_" + id.toLowerCase().replace(/[^a-z0-9_-]/g,"");
  const notify = (key, value) => {
    cache.set(key, value);
    for (const element of subscribers.get(key) || []) {
      if (element.isConnected) {
        element.textContent = value === null ? "Plays: —" : "Plays: " + format(value);
        element.title = value === null ? "Count service unavailable" :
          "Successful first plays per browser visit. Not unique people.";
      }
    }
  };
  const subscribe = (key, element) => {
    if (!subscribers.has(key)) subscribers.set(key,new Set());
    subscribers.get(key).add(element);
    if(cache.has(key)) notify(key,cache.get(key));
    else element.textContent="Plays: —";
  };
  async function api(kind,key) {
    const target=ENDPOINT+"/"+kind+"/"+encodeURIComponent(key);
    const response=await fetch(target,{
      method:"GET",mode:"cors",cache:"no-store",referrerPolicy:"no-referrer"
    });
    if (kind==="get" && response.status===404) return 0;
    if (!response.ok) throw new Error("counter endpoint "+response.status);
    const body=await response.json();
    const count=asCount(body.value);
    if(count===null) throw new Error("invalid counter response");
    return count;
  }
  const enqueue=fn=>new Promise((resolve,reject)=>{
    queue.push({fn,resolve,reject});
    if(!draining) drain();
  });
  async function drain() {
    draining=true;
    while(queue.length) {
      const job=queue.shift();
      try {job.resolve(await job.fn());}
      catch(err) {job.reject(err);}
      if(queue.length) await new Promise(resolve=>setTimeout(resolve,DELAY_MS));
    }
    draining=false;
  }
  function read(key) {
    if(cache.has(key)) return Promise.resolve(cache.get(key));
    if(pending.has(key)) return Promise.resolve(null);
    pending.add(key);
    return enqueue(()=>api("get",key)).then(v=>{
      notify(key,v);return v;
    }).catch(()=>{
      notify(key,null);return null;
    }).finally(()=>pending.delete(key));
  }
  async function hit(key) {
    const value=await enqueue(()=>api("hit",key));
    notify(key,value);
    return value;
  }
  const siteKey=PREFIX+"_site_visits";
  const onceKey=PREFIX+"_site_counted_in_tab";
  const visitTarget=document.getElementById("totalVisits");
  async function visit() {
    if(!visitTarget) return;
    visitTarget.textContent="Loading…";
    try {
      const already=sessionStorage.getItem(onceKey)==="yes";
      const count=already ? await read(siteKey) : await hit(siteKey);
      if(!already) sessionStorage.setItem(onceKey,"yes");
      visitTarget.textContent = format(count);
    }catch(err){
      visitTarget.textContent="Unavailable";
      visitTarget.title="Third-party count service could not be reached";
    }
  }
  const observer = typeof IntersectionObserver!=="undefined" ?
    new IntersectionObserver((entries)=>{
      for(const entry of entries) {
        if(!entry.isIntersecting) continue;
        observer.unobserve(entry.target);
        const key=entry.target.dataset.counterKey;
        if(key) read(key);
      }
    },{rootMargin:"100px"}) : null;
  function registerCard(id,element) {
    if(!/^AXZ-\d{3}$/.test(id)||!element) return;
    const key=keyFor(id);
    element.dataset.counterKey=key;
    subscribe(key,element);
    if(observer)observer.observe(element);
    else read(key);
  }
  const recorded=new Set();
  async function recordFirstPlay(id) {
    if(!/^AXZ-\d{3}$/.test(id)) return;
    const key=keyFor(id);
    const storageKey=PREFIX+"_played_"+id;
    if(recorded.has(id)) return;
    try {
      if(sessionStorage.getItem(storageKey)==="yes") return;
    } catch { /* Privacy-limited browser: use in-page de-duplication. */ }
    recorded.add(id);
    try {
      const value=await hit(key);
      try{sessionStorage.setItem(storageKey,"yes");}catch{}
      return value;
    }catch{
      recorded.delete(id);
      return null;
    }
  }
  // No IP, email, account identifier, cookie or third-party secret transmitted.
  visit();
  window.AXEZENT_COUNTERS=Object.freeze({registerCard,recordFirstPlay,read,
    onSelected:(id,element)=>registerCard(id,element)});
})();
