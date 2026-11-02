/* AXEZENT Beats for Sale — static public catalog.
   No payment collection, paid-download path or owner analytics exists in this frontend.
   Enable only after implementing a secure server-side checkout. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const cards = $("tracks"), query = $("query"), region = $("region"), sort = $("sort");
  const more = $("more"), results = $("resultsText"), empty = $("empty");
  const dialog = $("trackDialog"), modal = $("dialogContent"), player = $("player");
  const state = { all: [], filtered: [], displayed: 0, playing: null };
  const PAGE = 24;
  const accents = {
    "Southern":"#8c643b", "East Coast":"#487e9d", "West Coast":"#7c589c",
    "Midwest":"#607b87", "Mountain & Southwest":"#9b7546",
    "Pacific & Far North":"#2e847e", "Appalachian":"#837c59"
  };
  const el = (tag, className, txt) => {
    const n = document.createElement(tag);
    if(className) n.className = className;
    if(txt !== undefined) n.textContent = txt;
    return n;
  };
  const previewReady = b => b.status === "preview_ready" && typeof b.previewUrl === "string" &&
    /^previews\/[A-Za-z0-9_-]+(?:-tagged)?\.mp3$/.test(b.previewUrl);
  const elAppend = (parent, ...nodes) => { nodes.forEach(n => parent.appendChild(n)); return parent; };
  const trackCard = (beat) => {
    const article = el("article","track-card");
    const art = el("div","track-art");
    art.style.setProperty("--accent", accents[beat.collection] || "#7d8795");
    elAppend(art,el("b","",beat.id),el("small","",beat.collection));
    const body = el("div","track-content");
    const h3 = el("h3","",beat.title); h3.title = beat.title;
    const meta = el("div","track-meta",beat.city + ", " + beat.state + (beat.bpm ? " · "+beat.bpm+" BPM" : ""));
    const status = el("span","status"+(previewReady(beat)?" ready":""),previewReady(beat)?"Preview ready":"In production queue");
    const buttons = el("div","track-actions");
    const play = el("button","play-button",previewReady(beat)?"▶ Preview":"Preview soon");
    play.type = "button"; play.disabled = !previewReady(beat);
    if(!play.disabled) play.addEventListener("click",() => startPreview(beat,play));
    const detail = el("button","detail-button","View Details");
    detail.type = "button"; detail.addEventListener("click",()=>showDetails(beat));
    elAppend(buttons,play,detail);
    const available = el("p","availability","$100 commercial license planned · Not on sale yet");
    elAppend(body,h3,meta,status,buttons,available);
    return elAppend(article,art,body);
  };
  const stopPreview = () => {
    player.pause(); player.removeAttribute("src"); player.load();
    state.playing = null;
    document.querySelectorAll(".play-button").forEach(b=>{if(!b.disabled) b.textContent="▶ Preview";});
  };
  function startPreview(b,button) {
    if(state.playing === b.id && !player.paused) {stopPreview();return;}
    stopPreview(); player.src = b.previewUrl; state.playing = b.id;
    player.play().then(()=>{button.textContent="Ⅱ Pause";}).catch(()=>{
      stopPreview(); alert("The preview could not be played. Please try again.");
    });
  }
  player.addEventListener("ended",stopPreview);
  function showDetails(beat) {
    modal.replaceChildren();
    elAppend(modal,
      el("span","micro",beat.id+" · "+beat.city.toUpperCase()+", "+beat.state.toUpperCase()),
      el("h2","",beat.title),
      el("p","",beat.collection+" collection"+(beat.bpm?" · "+beat.bpm+" BPM":"")+" · "+(beat.key||"Original key pending composition")),
      el("p","",previewReady(beat)?"An original tagged audio preview is ready to play.":"This track is planned; the original instrumental has not been uploaded."),
      el("div","details-note","Proposed price: $100 for a nonexclusive commercial license. The final rights agreement, verified checkout and secure customer delivery are not enabled yet.")
    );
    if(typeof dialog.showModal === "function") dialog.showModal(); else dialog.setAttribute("open","");
  }
  $("closeDialog").addEventListener("click",()=>{if(dialog.close)dialog.close();else dialog.removeAttribute("open");});
  dialog.addEventListener("click",(e)=>{if(e.target===dialog)dialog.close();});
  function applyFilters() {
    const term = query.value.toLocaleLowerCase().trim();
    const selectedRegion = region.value;
    let filtered = state.all.filter(b =>
      (!selectedRegion || selectedRegion===b.collection) &&
      (!term || [b.id,b.title,b.city,b.state,b.collection,String(b.bpm||"")].join(" ").toLocaleLowerCase().includes(term))
    );
    if(sort.value==="title") filtered.sort((a,b)=>a.title.localeCompare(b.title));
    else if(sort.value==="state")filtered.sort((a,b)=>a.state.localeCompare(b.state)||a.city.localeCompare(b.city));
    else if(sort.value==="released")filtered.sort((a,b)=>Number(previewReady(b))-Number(previewReady(a)));
    state.filtered = filtered; state.displayed = 0; cards.replaceChildren(); renderPage();
  }
  function renderPage() {
    const page=state.filtered.slice(state.displayed,state.displayed+PAGE);
    const frag=document.createDocumentFragment();
    page.forEach(b=>frag.appendChild(trackCard(b)));
    cards.appendChild(frag);
    state.displayed += page.length;
    results.textContent = state.filtered.length+" beat concepts found · "+state.displayed+" showing";
    empty.hidden = state.filtered.length!==0;
    more.hidden=state.displayed>=state.filtered.length;
  }
  more.addEventListener("click",renderPage);
  query.addEventListener("input",applyFilters);
  region.addEventListener("change",applyFilters);
  sort.addEventListener("change",applyFilters);
  $("year").textContent=new Date().getFullYear();
  fetch("data/catalog.json",{cache:"no-cache"}).then(r=>{if(!r.ok)throw Error("Catalog request failed");return r.json();}).then(data=>{
    if(!Array.isArray(data) || data.length!==200)throw Error("Catalog validation failed");
    state.all=data;
    const collections=[...new Set(data.map(x=>x.collection))].sort();
    collections.forEach(c=>{const option=el("option","",c);option.value=c;region.appendChild(option);});
    $("heroTotal").textContent=String(data.length);
    $("heroLive").textContent=String(data.filter(previewReady).length);
    applyFilters();
  }).catch(err=>{results.textContent="Catalog could not load. Please refresh.";cards.replaceChildren();more.hidden=true;console.error(err);});
})();