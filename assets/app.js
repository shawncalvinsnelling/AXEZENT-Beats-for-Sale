/* AXEZENT Beats for Sale — static public catalog.
   No payment collection, paid-download path or owner analytics exists in this frontend.
   Enable only after implementing a secure server-side checkout. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const cards = $("tracks"), query = $("query"), region = $("region"), sort = $("sort");
  const more = $("more"), results = $("resultsText"), empty = $("empty");
  const dialog = $("trackDialog"), modal = $("dialogContent"), player = $("player");
  const state = { all: [], filtered: [], displayed: 0, playing: null, selected: null };
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
    /^\/api\/preview\/AXZ-\d{3}$/.test(b.previewUrl);
  const elAppend = (parent, ...nodes) => { nodes.forEach(n => parent.appendChild(n)); return parent; };
  const trackCard = (beat) => {
    const article = el("article","track-card");
    const art = el("div","track-art");
    art.style.setProperty("--accent", accents[beat.collection] || "#7d8795");
    elAppend(art,el("b","",beat.id),el("small","",beat.collection));
    const body = el("div","track-content");
    const h3 = el("h3","",beat.title); h3.title = beat.title;
    const meta = el("div","track-meta",beat.city + ", " + beat.state + (beat.bpm ? " · "+beat.bpm+" BPM" : ""));
    const status = el("span","status"+(previewReady(beat)?" ready":""),previewReady(beat)?"Listen to the beat":beat.status==="mix_review"?"Audio not published":"Coming soon");
    const buttons = el("div","track-actions");
    const play = el("button","play-button",previewReady(beat)?"▶ Listen to "+beat.title:"▶ "+beat.title+" · Coming soon");
    play.type = "button"; play.disabled = !previewReady(beat);
    if(!play.disabled) play.addEventListener("click",() => openPlayer(beat));
    const detail = el("button","detail-button","View Details");
    detail.type = "button"; detail.addEventListener("click",()=>showDetails(beat));
    elAppend(buttons,play,detail);
    const inquiry = el("a","inquiry-action","✉ Email about $100 ownership");
    inquiry.href = "mailto:axezentai@gmail.com?subject=" + encodeURIComponent("AXEZENT $100 beat inquiry — " + beat.id + " — " + beat.title);
    inquiry.title = "Request exclusive rights to " + beat.title + " before sending payment";
    const available = el("p","availability",beat.status==="preview_ready"?"Listen now · Ask about $100 exclusive ownership":"Under review · Ask about $100 exclusive ownership");
    elAppend(body,h3,meta,status,buttons,inquiry,available);
    return elAppend(article,art,body);
  };
  const musicDialog = $("playerDialog");
  const musicTitle = $("musicTitle"), musicMeta = $("musicMeta");
  const musicStatus = $("musicStatus");
  const musicPlay = $("musicPlay"), musicPause = $("musicPause"), musicStop = $("musicStop");
  const musicTime = $("musicTime"), musicDuration = $("musicDuration"), musicProgress = $("musicProgress");
  const musicInquiry = $("musicInquiry");
  const showTime = (seconds) => {
    if(!Number.isFinite(seconds) || seconds < 0) return "0:00";
    const sec = Math.floor(seconds);
    return Math.floor(sec / 60) + ":" + String(sec % 60).padStart(2,"0");
  };
  const setPlayerStatus = (message) => {musicStatus.textContent=message;};
  const syncProgress = () => {
    musicTime.textContent=showTime(player.currentTime);
    musicDuration.textContent=showTime(player.duration);
    const pct=Number.isFinite(player.duration) && player.duration>0
      ? Math.max(0,Math.min(100,player.currentTime/player.duration*100)):0;
    musicProgress.style.width=pct+"%";
  };
  const stopPlayback = () => {
    player.pause();
    try {player.currentTime=0;} catch(e) {/* metadata may not be loaded */}
    syncProgress();
    setPlayerStatus("Stopped");
  };
  const closePlayer = () => {
    stopPlayback();
    player.removeAttribute("src");
    player.load();
    state.selected=null;
    if(musicDialog.open) musicDialog.close();
  };
  async function playSelected() {
    if(!state.selected) return;
    try {
      await player.play();
      setPlayerStatus("Now playing");
    } catch(err) {
      setPlayerStatus("Audio is unavailable. Check the preview server and try again.");
    }
  }
  function openPlayer(beat) {
    if(!previewReady(beat)) return;
    stopPlayback();
    state.selected=beat;
    player.src=beat.previewUrl;
    player.load();
    musicTitle.textContent=beat.title;
    musicMeta.textContent=beat.city+", "+beat.state+" · "+(beat.bpm||"—")+" BPM";
    musicInquiry.href="mailto:axezentai@gmail.com?subject="+encodeURIComponent(
      "AXEZENT — $100 ownership enquiry — "+beat.id+" — "+beat.title);
    musicInquiry.textContent="Email AXEZENT AI about $100 ownership of "+beat.title;
    setPlayerStatus("Ready to listen");
    if(!musicDialog.open) musicDialog.showModal();
    playSelected();
  }
  musicPlay.addEventListener("click",playSelected);
  musicPause.addEventListener("click",() => {player.pause();setPlayerStatus("Paused");});
  musicStop.addEventListener("click",stopPlayback);
  $("closePlayer").addEventListener("click",closePlayer);
  musicDialog.addEventListener("cancel",(event) => {event.preventDefault();closePlayer();});
  musicDialog.addEventListener("click",(event) => {
    if(event.target===musicDialog)closePlayer();
  });
  player.addEventListener("timeupdate",syncProgress);
  player.addEventListener("loadedmetadata",syncProgress);
  player.addEventListener("ended",()=>{stopPlayback();setPlayerStatus("Finished");});
  player.addEventListener("error",()=> {
    if(state.selected) setPlayerStatus("Audio unavailable. The preview file could not be opened.");
  });
  function showDetails(beat) {
    modal.replaceChildren();
    elAppend(modal,
      el("span","micro",beat.id+" · "+beat.city.toUpperCase()+", "+beat.state.toUpperCase()),
      el("h2","",beat.title),
      el("p","",beat.collection+" collection"+(beat.bpm?" · "+beat.bpm+" BPM":"")+" · "+(beat.key||"Original key pending composition")),
      el("p","",previewReady(beat)?"Click Listen to hear the selected instrumental.":beat.status==="mix_review"?"A full-length review mix exists privately; its watermarked public preview has not yet been uploaded.":"This track is still a production concept."),
      el("div","details-note","Proposed price: $100 for an exclusive transfer of an eligible beat, only after ownership review and a signed written agreement. Please use the contact section to ask about availability before sending payment.")
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
    if(sort.value==="featured") filtered.sort((a,b)=>(a.releaseRank??1000)-(b.releaseRank??1000));
    else if(sort.value==="title") filtered.sort((a,b)=>a.title.localeCompare(b.title));
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
    results.textContent = state.filtered.length+" beats · "+state.displayed+" showing";
    empty.hidden = state.filtered.length!==0;
    more.hidden=state.displayed>=state.filtered.length;
  }
  more.addEventListener("click",renderPage);
  query.addEventListener("input",applyFilters);
  region.addEventListener("change",applyFilters);
  sort.addEventListener("change",applyFilters);
  $("year").textContent=new Date().getFullYear();
  fetch("/api/catalog",{cache:"no-store"}).then(r=>{if(!r.ok)throw Error("Catalog request failed");return r.json();}).then(data=>{
    if(!Array.isArray(data) || data.length!==200)throw Error("Catalog validation failed");
    state.all=data.filter(b=>Number.isInteger(b.releaseRank) && b.releaseRank>=1 && b.releaseRank<=50);
    const reviewCount=state.all.length;
    const reviewNode=document.getElementById("reviewCount");
    if(reviewNode) reviewNode.textContent=String(reviewCount);
    const collections=[...new Set(state.all.map(x=>x.collection))].sort();
    collections.forEach(c=>{const option=el("option","",c);option.value=c;region.appendChild(option);});
    $("heroTotal").textContent=String(state.all.length);
    const liveNode=$("heroLive"); if(liveNode)liveNode.textContent=String(state.all.filter(previewReady).length);
    applyFilters();
  }).catch(err=>{results.textContent="Catalog could not load. Please refresh.";cards.replaceChildren();more.hidden=true;console.error(err);});
})();