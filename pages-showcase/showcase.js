/* AXEZENT artist showcase for GitHub Pages. Derived from the original storefront player.
   This static frontend contains no sales, customer information, or private audio. */
(() => {
  "use strict";
  const $ = (id) => document.getElementById(id);
  const cards = $("tracks"), query = $("query"), region = $("region"), sort = $("sort");
  const more = $("more"), results = $("resultsText"), empty = $("empty");
  const dialog = $("trackDialog"), modal = $("dialogContent"), player = $("player");
  const state = { all: [], filtered: [], displayed: 0, playing: null, selected: null };
  const PAGE = 50;
  // All timing here is sourced from each producer-selected 4/4 arrangement
  // blueprint, never inferred from an existing/unverified recording.
  const showClock = secs => {
    if (!Number.isFinite(secs)) return "—";
    const s = Math.round(secs);
    return Math.floor(s/60)+":"+String(s%60).padStart(2,"0");
  };
  const renderSectionTable = (track) => {
    const spec = track.arrangement;
    if (!spec || !Array.isArray(spec.sections)) {
      return el("p","", "No verified arrangement specification available.");
    }
    const pane = el("section","arrangement-detail");
    const subtitle = el("p","section-head","Proposed full instrumental structure · "+spec.totalBars+" bars · "+showClock(spec.durationSeconds));
    const sound = el("p","production-direction","Rhythm: "+spec.signature+" · Palette: "+spec.soundPalette);
    const items = el("div","arrangement-sections");
    spec.sections.forEach((segment,index)=>{
      const line=el("div","arrangement-segment");
      elAppend(line,
        el("span","segment-number",String(index+1).padStart(2,"0")),
        el("strong","segment-title",segment.label),
        el("span","segment-bars",segment.bars+" bars"),
        el("span","segment-time",showClock(segment.startSeconds)+" – "+showClock(segment.endSeconds))
      );
      items.appendChild(line);
    });
    elAppend(pane,subtitle,sound,items,
      el("p","arrangement-disclosure","Production blueprint — calculated from "+track.bpm+" BPM in 4/4. Not yet verified against a finished MP3. Sections and durations may change during mastering."));
    return pane;
  };
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
  // One real approved source per beat; never synthesize substitute audio in-browser.
  // Same-origin relative URLs are allowed so tagged preview files or HTTPS audio
  // endpoints can be used without changing the listening interface.
  const approvedPreviewUrl = b => {
    if (typeof b.previewUrl !== "string" || !b.previewUrl.trim()) return null;
    try {
      const url = new URL(b.previewUrl, document.baseURI);
      if (url.protocol !== "https:" || url.username || url.password) return null;
      return url.href;
    } catch { return null; }
  };
  const previewReady = b => approvedPreviewUrl(b) !== null;
  const elAppend = (parent, ...nodes) => { nodes.forEach(n => parent.appendChild(n)); return parent; };
  const trackCard = (beat) => {
    const article = el("article","track-card");
    const art = el("div","track-art");
    art.style.setProperty("--accent", accents[beat.collection] || "#7d8795");
    elAppend(art,el("b","",beat.id),el("small","",beat.collection));
    const body = el("div","track-content");
    const h3 = el("h3","",beat.title); h3.title = beat.title;
    const meta = el("div","track-meta",beat.city + ", " + beat.state + (beat.bpm ? " · "+beat.bpm+" BPM" : ""));
    const status = previewReady(beat) ? el("span","status ready","Full-length review audio") : null;
    const buttons = el("div","track-actions");
    const play = el("button","play-button","▶ Play");
    play.type = "button"; play.disabled = !previewReady(beat);
    play.title = play.disabled ? "Audio review mix not connected yet" : "Listen to full-length review mix: "+beat.title;
    play.setAttribute("aria-label",play.title);
    if(!play.disabled) play.addEventListener("click",() => openPlayer(beat));
    const detail = el("button","detail-button","Details");
    detail.type = "button"; detail.addEventListener("click",()=>showDetails(beat));
    elAppend(buttons,play,detail);
    elAppend(body,h3,meta);
    if(status) body.appendChild(status);
    body.appendChild(buttons);
    return elAppend(article,art,body);
  };
  const musicDialog = $("playerDialog");
  const musicTitle = $("musicTitle"), musicMeta = $("musicMeta");
  const musicStatus = $("musicStatus");
  const musicPlay = $("musicPlay"), musicPause = $("musicPause"), musicStop = $("musicStop");
  const musicTime = $("musicTime"), musicDuration = $("musicDuration"), musicSeek = $("musicSeek");
  const musicRepeat = $("musicRepeat");
  let scrubbing = false;
  const showTime = (seconds) => {
    if(!Number.isFinite(seconds) || seconds < 0) return "0:00";
    const sec = Math.floor(seconds);
    return Math.floor(sec / 60) + ":" + String(sec % 60).padStart(2,"0");
  };
  const setPlayerStatus = (message) => {musicStatus.textContent=message;};
  const syncProgress = () => {
    const dur = player.duration;
    const playable = Number.isFinite(dur) && dur > 0;
    musicSeek.disabled = !playable;
    musicDuration.textContent=showTime(dur);
    musicTime.textContent=showTime(player.currentTime);
    if (!scrubbing) musicSeek.value = playable
      ? String(Math.max(0,Math.min(100,player.currentTime/dur*100)))
      : "0";
  };
  const seekTo = (percentage) => {
    if(!state.selected) return;
    const dur=player.duration;
    if(!Number.isFinite(dur) || dur <= 0) return;
    const target=Math.max(0,Math.min(100,Number(percentage)||0))*dur/100;
    try {player.currentTime=target;} catch(error) {
      setPlayerStatus("Seeking is not available yet.");
      return;
    }
    musicTime.textContent=showTime(target);
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
      setPlayerStatus("Audio could not be played. Check the connection and try again.");
    }
  }
  function openPlayer(beat) {
    if(!previewReady(beat)) return;
    stopPlayback();
    state.selected=beat;
    player.src=approvedPreviewUrl(beat);
    player.load();
    musicTitle.textContent=beat.title;
    musicMeta.textContent=beat.city+", "+beat.state+" · "+(beat.bpm||"—")+" BPM";
    const caption=$("musicArrangement");
    if(caption)caption.textContent=beat.arrangement && Array.isArray(beat.arrangement.sections)
      ? "Arrangement: "+beat.arrangement.sections.map(s=>s.label).join(" → ")
      : "Full-length review mix";
    setPlayerStatus("Ready to listen");
    if(!musicDialog.open) musicDialog.showModal();
    playSelected();
  }
  musicPlay.addEventListener("click",playSelected);
  musicPause.addEventListener("click",() => {player.pause();setPlayerStatus("Paused");});
  musicStop.addEventListener("click",stopPlayback);
  musicSeek.addEventListener("pointerdown",() => {scrubbing=true;});
  musicSeek.addEventListener("input",() => {scrubbing=true;seekTo(musicSeek.value);});
  musicSeek.addEventListener("change",() => {seekTo(musicSeek.value);scrubbing=false;});
  musicSeek.addEventListener("blur",() => {scrubbing=false;syncProgress();});
  musicRepeat.addEventListener("click",() => {
    player.loop = !player.loop;
    musicRepeat.setAttribute("aria-pressed",String(player.loop));
    musicRepeat.textContent = player.loop ? "↻ Repeat On" : "↻ Repeat Off";
    setPlayerStatus(player.loop ? "Repeat enabled" : "Repeat disabled");
  });
  $("closePlayer").addEventListener("click",closePlayer);
  musicDialog.addEventListener("cancel",(event) => {event.preventDefault();closePlayer();});
  musicDialog.addEventListener("click",(event) => {
    if(event.target===musicDialog)closePlayer();
  });
  player.addEventListener("timeupdate",syncProgress);
  player.addEventListener("loadedmetadata",syncProgress);
  player.addEventListener("seeked",syncProgress);
  player.addEventListener("ended",()=>{stopPlayback();setPlayerStatus("Finished");});
  player.addEventListener("error",()=> {
    if(state.selected) setPlayerStatus("Audio unavailable. The preview file could not be opened.");
  });
  function showDetails(beat) {
    modal.replaceChildren();
    elAppend(modal,
      el("span","micro",beat.id+" · "+beat.city.toUpperCase()+", "+beat.state.toUpperCase()),
      el("h2","",beat.title),
      el("p","",beat.collection+" collection"+(beat.bpm?" · "+beat.bpm+" BPM":"")+" · "+(beat.key||"Production details")),
      el("p","",previewReady(beat)?"Play the NEW full-length review arrangement. It is not a verified copy of the earlier private finished mix or a delivered paid master.":"Audio is pending producer review and hosting; this is the planned beat structure."),
      renderSectionTable(beat),
      el("div","details-note","$100 EXCLUSIVE FULL INSTRUMENTAL — intended price for an eligible, approved beat. The purchase version is the complete arrangement shown above. Rights transfer, audio delivery and availability must be confirmed by AXEZENT in writing. No payment is collected on this page.")
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
  const catalogRequest = fetch("./data/catalog.json",{cache:"no-store"}).then(r=>{
    if(!r.ok) throw Error("Catalog request failed");
    return r.json();
  });
  const publicPreviewsRequest = fetch("./data/public-preview-manifest.json",{cache:"no-store"})
    .then(r=>r.ok?r.json():{}).catch(()=>({}));
  const arrangementRequest = fetch("./data/arrangements.json",{cache:"no-store"}).then(r=>{
    if (!r.ok) throw Error("Arrangement data unavailable");
    return r.json();
  });
  Promise.all([catalogRequest,publicPreviewsRequest,arrangementRequest]).then(([data,previewManifest,arrangements])=>{
    if(!Array.isArray(data) || data.length!==200)throw Error("Catalog validation failed");
    const urls=previewManifest && typeof previewManifest==="object" && !Array.isArray(previewManifest) ? previewManifest : {};
    if(!arrangements||typeof arrangements!=="object"||Array.isArray(arrangements)||Object.keys(arrangements).length!==50)throw Error("Expected 50 proposed arrangements");
    state.all=data.filter(b=>Number.isInteger(b.releaseRank) && b.releaseRank>=1 && b.releaseRank<=50)
      .map(b=>({...b,previewUrl:typeof urls[b.id]==="string" ? urls[b.id] : null,arrangement:arrangements[b.id]}));
    if(state.all.length!==50 || state.all.some(b=>!b.arrangement || b.arrangement.bpm!==b.bpm))throw Error("Featured arrangement validation failed");
    const collections=[...new Set(state.all.map(x=>x.collection))].sort();
    collections.forEach(c=>{const option=el("option","",c);option.value=c;region.appendChild(option);});
    $("heroTotal").textContent=String(data.length);
    const reviewNode=$("reviewCount");if(reviewNode)reviewNode.textContent=String(state.all.length);
    applyFilters();
  }).catch(err=>{results.textContent="Catalog could not load. Please refresh.";cards.replaceChildren();more.hidden=true;console.error(err);});
})();