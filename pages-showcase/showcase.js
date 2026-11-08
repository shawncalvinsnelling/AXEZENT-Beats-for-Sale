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
  const segmentSeconds = s => Math.max(0,s.endSeconds-s.startSeconds);
  const segmentDuration = s => segmentSeconds(s).toFixed(1)+" seconds";
  const renderSectionTable = (track) => {
    const spec = track.arrangement;
    if (!spec || !Array.isArray(spec.sections)) {
      return el("p","", "No verified arrangement specification available.");
    }
    const pane = el("section","arrangement-detail");
    const subtitle = el("p","section-head","Track arrangement · "+spec.totalBars+" bars · "+showClock(spec.durationSeconds));
    const sound = el("p","production-direction","Rhythm: "+spec.signature+" · Palette: "+spec.soundPalette);
    const items = el("div","arrangement-sections");
    spec.sections.forEach((segment,index)=>{
      const line=el("div","arrangement-segment");
      const primary=el("div","segment-primary");
      elAppend(primary,el("strong","segment-title",segment.label),
        el("span","segment-duration",segmentDuration(segment)));
      const secondary=el("div","segment-secondary");
      elAppend(secondary,el("span","segment-bars",segment.bars+" bars"),
        el("span","segment-time",showClock(segment.startSeconds)+" – "+showClock(segment.endSeconds)));
      elAppend(line,el("span","segment-number",String(index+1).padStart(2,"0")),
        primary,secondary);
      items.appendChild(line);
    });
    elAppend(pane,subtitle,sound,items,
      el("p","arrangement-disclosure","Section times are approximate, calculated from "+track.bpm+" BPM."));
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
    const num=Number(beat.id.replace(/\D/g,"")) || beat.bpm || 1;
    const swatches=["#ddad69","#87c1cb","#9c91d5","#d28d79","#8fc59d","#d4be7b","#ba9ebc"];
    art.style.setProperty("--accent-2",swatches[num%swatches.length]);
    const bars=el("span","cover-soundwave");
    bars.setAttribute("aria-hidden","true");
    for(let k=0;k<11;k++){
      const line=el("i","");
      line.style.height=(12+Math.abs(Math.sin((num+k*17)*.37))*37)+"px";
      bars.appendChild(line);
    }
    elAppend(art,bars,el("b","",beat.id),el("small","",beat.collection));
    const body = el("div","track-content");
    const h3 = el("h3","",beat.title); h3.title = beat.title;
    const meta = el("div","track-meta",beat.city + ", " + beat.state + (beat.bpm ? " · "+beat.bpm+" BPM" : ""));
    const buttons = el("div","track-actions");
    const play = el("button","play-button","▶ Play");
    play.type = "button"; play.disabled = !previewReady(beat);
    play.title = play.disabled ? "Audio not available" : "Listen to "+beat.title;
    play.setAttribute("aria-label",play.title);
    if(!play.disabled) play.addEventListener("click",() => openPlayer(beat));
    const detail = el("button","detail-button","Details");
    detail.type = "button"; detail.addEventListener("click",()=>showDetails(beat));
    elAppend(buttons,play,detail);
    elAppend(body,h3,meta);
    body.appendChild(buttons);
    return elAppend(article,art,body);
  };
  const musicDialog = $("playerDialog");
  const musicTitle = $("musicTitle"), musicMeta = $("musicMeta");
  const musicStatus = $("musicStatus");
  const musicPlay = $("musicPlay"), musicPause = $("musicPause"), musicStop = $("musicStop");
  const musicTime = $("musicTime"), musicDuration = $("musicDuration"), musicSeek = $("musicSeek");
  const musicRepeat = $("musicRepeat");
  const musicVolume = $("musicVolume"), musicVolumeValue = $("musicVolumeValue");
  const musicBack15 = $("musicBack15"), musicForward15 = $("musicForward15");
  const musicSections = $("musicArrangement"), musicSectionNow = $("musicSectionNow");
  let sectionButtons=[];
  let scrubbing = false;
  const showTime = (seconds) => {
    if(!Number.isFinite(seconds) || seconds < 0) return "0:00";
    const sec = Math.floor(seconds);
    return Math.floor(sec / 60) + ":" + String(sec % 60).padStart(2,"0");
  };
  const setPlayerStatus = (message) => {musicStatus.textContent=message;};
  const markCurrentSection = () => {
    const sections=state.selected?.arrangement?.sections;
    if(!Array.isArray(sections)||!sections.length)return;
    const time=Number(player.currentTime)||0;
    let active=sections.findIndex((s,i)=>time>=s.startSeconds-0.01 &&
      (time<s.endSeconds-0.01||i===sections.length-1));
    active=Math.max(0,active);
    const selected=sections[active];
    musicSectionNow.textContent="Now: "+selected.label+" · "+segmentDuration(selected);
    sectionButtons.forEach((button,i)=>{
      button.classList.toggle("is-active",i===active);
      if(i===active)button.setAttribute("aria-current","true");
      else button.removeAttribute("aria-current");
    });
  };
  const buildSectionGuide = beat => {
    musicSections.replaceChildren();
    sectionButtons=[];
    for(const [index,s] of (beat.arrangement?.sections||[]).entries()){
      const block=el("div","music-section-step");
      const button=el("button","music-section-jump");
      button.type="button";
      button.setAttribute("aria-label","Jump to "+s.label+" lasting "+
        segmentDuration(s)+", beginning at "+showClock(s.startSeconds));
      const headline=el("span","music-section-heading");
      elAppend(headline,el("strong","music-section-label",s.label),
        el("span","music-section-bars",s.bars+" bars"));
      elAppend(button,headline,el("span","music-section-duration",segmentDuration(s)),
        el("span","music-section-position",showClock(s.startSeconds)+" – "+showClock(s.endSeconds)));
      button.addEventListener("click",()=>{
        if(!state.selected)return;
        try{
          const total=Number.isFinite(player.duration)&&player.duration>0 ?
            player.duration : beat.arrangement.durationSeconds;
          player.currentTime=Math.min(total,Math.max(0,s.startSeconds));
          syncProgress();
          if(player.paused)playSelected();
        }catch(err){setPlayerStatus("Still loading; try this section again.");}
      });
      block.appendChild(button);
      if(index<beat.arrangement.sections.length-1){
        const arrow=el("span","music-section-arrow","↓");
        arrow.setAttribute("aria-hidden","true");
        block.appendChild(arrow);
      }
      musicSections.appendChild(block);
      sectionButtons.push(button);
    }
    markCurrentSection();
  };
  const syncProgress = () => {
    const dur = player.duration;
    const playable = Number.isFinite(dur) && dur > 0;
    musicSeek.disabled = !playable;
    musicDuration.textContent=showTime(dur);
    musicTime.textContent=showTime(player.currentTime);
    if (!scrubbing) musicSeek.value = playable
      ? String(Math.max(0,Math.min(100,player.currentTime/dur*100)))
      : "0";
    markCurrentSection();
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
      if(err && err.name === "NotAllowedError"){
        setPlayerStatus("Your browser needs a direct tap or click. Press Play again.");
      } else if(err && err.name === "AbortError") {
        // An earlier request was interrupted by Stop, Exit or a new track.
      } else {
        setPlayerStatus("Playback could not start. Press Play to retry or check your connection.");
      }
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
    buildSectionGuide(beat);
    setPlayerStatus("Ready to listen");
    if(!musicDialog.open) musicDialog.showModal();
    playSelected();
  }
  musicPlay.addEventListener("click",playSelected);
  musicPause.addEventListener("click",() => {player.pause();setPlayerStatus("Paused");});
  musicStop.addEventListener("click",stopPlayback);
  musicSeek.addEventListener("pointerdown",() => {scrubbing=true;});
  // During dragging only preview the chosen time; seek once on release.
  // This prevents excessive overlapping HTTP Range requests on slower networks.
  musicSeek.addEventListener("input",() => {
    scrubbing=true;
    if(Number.isFinite(player.duration) && player.duration>0) {
      musicTime.textContent=showTime((Number(musicSeek.value)||0)*player.duration/100);
    }
  });
  musicSeek.addEventListener("change",() => {seekTo(musicSeek.value);scrubbing=false;});
  musicSeek.addEventListener("blur",() => {scrubbing=false;syncProgress();});
  const skip = seconds => {
    if(!state.selected || !Number.isFinite(player.duration))return;
    try{
      player.currentTime=Math.max(0,Math.min(player.duration,player.currentTime+seconds));
      syncProgress();
    }catch(error){setPlayerStatus("Skip isn't available while loading.");}
  };
  musicBack15.addEventListener("click",() => skip(-15));
  musicForward15.addEventListener("click",() => skip(15));
  musicVolume.addEventListener("input",() => {
    player.volume=Math.max(0,Math.min(1,Number(musicVolume.value)/100));
    player.muted=false;
    musicVolumeValue.textContent=Math.round(player.volume*100)+"%";
  });
  player.volume=1;
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
  player.addEventListener("loadstart",()=>{if(state.selected)setPlayerStatus("Loading audio…");});
  player.addEventListener("waiting",()=>{if(state.selected && !player.paused)setPlayerStatus("Buffering…");});
  player.addEventListener("stalled",()=>{if(state.selected)setPlayerStatus("Connection slowed. Press Play to retry if needed.");});
  player.addEventListener("canplay",()=>{if(state.selected && player.paused)setPlayerStatus("Ready. Press Play.");});
  player.addEventListener("playing",()=>{if(state.selected)setPlayerStatus("Now playing");});
  player.addEventListener("timeupdate",syncProgress);
  player.addEventListener("loadedmetadata",syncProgress);
  player.addEventListener("seeked",syncProgress);
  player.addEventListener("ended",()=>{
    if(!player.loop){stopPlayback();setPlayerStatus("Finished");}
  });
  player.addEventListener("error",()=> {
    if(state.selected) {
      const code=player.error && player.error.code;
      setPlayerStatus(code===4 ? "This audio format isn't supported by your browser." :
        "Unable to load audio. Check your connection, then press Play to retry.");
    }
  });
  function showDetails(beat) {
    modal.replaceChildren();
    const inquiry=el("a","inquiry-email","✉ Email AXEZENT about this beat");
    inquiry.href="mailto:axezentai@gmail.com?subject="+
      encodeURIComponent("AXEZENT beat inquiry: "+beat.title+" ("+beat.id+")")+
      "&body="+encodeURIComponent("Hello AXEZENT, I'm interested in the $100 exclusive ownership offer for "+
        beat.title+" ("+beat.id+"). Please confirm availability and the written ownership terms.");
    elAppend(modal,
      el("span","micro",beat.id+" · "+beat.city.toUpperCase()+", "+beat.state.toUpperCase()),
      el("h2","",beat.title),
      el("p","",beat.collection+" collection"+(beat.bpm?" · "+beat.bpm+" BPM":"")+" · "+(beat.key||"Production details")),
      el("p","",previewReady(beat)?"Press Play to listen; the section list below shows this beat’s structure.":"The beat is not currently available to play."),
      renderSectionTable(beat),
      el("div","details-note","$100 PER BEAT · EXCLUSIVE OWNERSHIP. Purchase availability and the precise rights transferred are confirmed in writing before payment."),
      inquiry
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
    const totalNode=$("heroTotal"); if(totalNode)totalNode.textContent=String(data.length);
    const reviewNode=$("reviewCount");if(reviewNode)reviewNode.textContent=String(state.all.length);
    applyFilters();
  }).catch(err=>{results.textContent="Catalog could not load. Please refresh.";cards.replaceChildren();more.hidden=true;console.error(err);});
})();