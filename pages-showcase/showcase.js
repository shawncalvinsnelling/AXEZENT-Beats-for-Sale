/* AXEZENT artist showcase. No commerce, payments, account login, or audio server. */
(() => {
"use strict";
const el = id => document.getElementById(id);
const grid=el("tracks"),query=el("query"),region=el("region"),sort=el("sort");
let catalog=[];
const accents={"Southern":"#8c643b","East Coast":"#487e9d","West Coast":"#7c589c","Midwest":"#607b87","Mountain & Southwest":"#9b7546","Pacific & Far North":"#2e847e","Appalachian":"#837c59"};
function paint(){
 const term=query.value.trim().toLowerCase();
 const selected=region.value;
 const items=catalog.filter(b=>(!selected||b.collection===selected)&&(!term||[b.id,b.title,b.city,b.state,b.collection].join(" ").toLowerCase().includes(term)));
 if(sort.value==="title")items.sort((a,b)=>a.title.localeCompare(b.title));
 else if(sort.value==="state")items.sort((a,b)=>a.state.localeCompare(b.state)||a.city.localeCompare(b.city));
 else items.sort((a,b)=>a.releaseRank-b.releaseRank);
 const fragment=document.createDocumentFragment();
 for(const beat of items){
   const article=document.createElement("article");article.className="showcase-card";
   const art=document.createElement("div");art.className="track-art";art.style.setProperty("--accent",accents[beat.collection]||"#607b87");
   const id=document.createElement("b");id.textContent=beat.id;
   const collection=document.createElement("small");collection.textContent=beat.collection;art.append(id,collection);
   const body=document.createElement("div");body.className="track-content";
   const name=document.createElement("h3");name.textContent=beat.title;
   const location=document.createElement("p");location.className="track-meta";location.textContent=[beat.city,beat.state].filter(Boolean).join(", ")+(beat.bpm?" · "+beat.bpm+" BPM":"");
   body.append(name,location);article.append(art,body);fragment.append(article);
 }
 grid.replaceChildren(fragment);
 el("resultsText").textContent=items.length+" featured selections";
}
async function init(){
 el("year").textContent=String(new Date().getFullYear());
 try{
   const response=await fetch("./data/catalog.json",{cache:"no-store"});
   if(!response.ok)throw new Error("catalog response "+response.status);
   const data=await response.json();
   if(!Array.isArray(data))throw new Error("invalid catalog");
   catalog=data.filter(b=>Number.isInteger(b.releaseRank)&&b.releaseRank>=1&&b.releaseRank<=50);
   if(catalog.length!==50)throw new Error("featured catalog incomplete");
   el("heroTotal").textContent=String(catalog.length);
   const collections=[...new Set(catalog.map(b=>b.collection))].sort();
   for(const name of collections){const opt=document.createElement("option");opt.value=name;opt.textContent=name;region.append(opt);}
   for(const control of [query,region,sort])control.addEventListener(control===query?"input":"change",paint);
   paint();
 }catch(e){console.error("AXEZENT showcase:",e);el("error").hidden=false;el("resultsText").textContent="Catalog unavailable";}
}
init();
})();
