import assert from "node:assert/strict";
import {readFileSync} from "node:fs";
import vm from "node:vm";
const src=readFileSync(new URL("../pages-showcase/counters.js",import.meta.url),"utf8");
const elements={totalVisits:{textContent:"",title:""}};
const storage=new Map();
const counterStore=new Map();
const req=[];
const fetchFake=async url=>{
  const parts=url.split("/");
  const action=parts.at(-2), key=decodeURIComponent(parts.at(-1));
  req.push({action,key});
  if(action==="get"&&!counterStore.has(key)) return {ok:false,status:404};
  if(action==="hit") counterStore.set(key,(counterStore.get(key)||0)+1);
  return {ok:true,status:200,json:async()=>({key,value:counterStore.get(key)||0})};
};
const sessionStorage={getItem:k=>storage.get(k)||null,setItem:(k,v)=>storage.set(k,v)};
const window={};
const ctx={window,document:{getElementById:id=>elements[id]||null},
  fetch:fetchFake,sessionStorage,Promise,Map,Set,Number,
  IntersectionObserver:undefined,setTimeout:(fn)=>{fn();return 1},
  console,encodeURIComponent};
vm.runInNewContext(src,ctx);
assert.equal(typeof window.AXEZENT_COUNTERS.recordFirstPlay,"function");
const flush=()=>new Promise(resolve=>setTimeout(resolve,15));
await flush();
assert.equal(elements.totalVisits.textContent,"1","Site visited once");
const element={isConnected:true,dataset:{},textContent:""};
window.AXEZENT_COUNTERS.registerCard("AXZ-169",element);
await flush();
assert.equal(element.textContent,"Plays: 0","Uninitialized counter displays zero");
await Promise.all([window.AXEZENT_COUNTERS.recordFirstPlay("AXZ-169"),
 window.AXEZENT_COUNTERS.recordFirstPlay("AXZ-169")]);
await flush();
assert.equal(element.textContent,"Plays: 1","Only first confirmed playback is counted per session");
await window.AXEZENT_COUNTERS.recordFirstPlay("AXZ-169");
await flush();
assert.equal(element.textContent,"Plays: 1");
assert.equal(req.filter(x=>x.action==="hit").length,2,"One visitor hit plus one successful player hit");
const second={};
const ctx2={...ctx,window:second};
vm.runInNewContext(src,ctx2);
await flush();
assert.equal(elements.totalVisits.textContent,"1","Reload in same tab does not add visit");
assert.equal(req.filter(x=>x.action==="hit").length,2);
await second.AXEZENT_COUNTERS.recordFirstPlay("AXZ-169");
await flush();
assert.equal(req.filter(x=>x.action==="hit").length,2,"Same tab refresh cannot repeat play count");
console.log("PASS: persistent site and successful first-play per session counters, no duplicate resume increments");
