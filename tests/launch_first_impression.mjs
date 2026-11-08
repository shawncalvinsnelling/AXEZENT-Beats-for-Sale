import {chromium} from 'playwright';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const BASE='https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/';
const OUTPUT='launch-qa';
fs.mkdirSync(OUTPUT,{recursive:true});
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
const out={website:BASE,checks:[],errors:[]};
const record=(name,ok,details={})=>{out.checks.push({name,ok,...details});if(!ok)throw Error('LAUNCH QA FAIL: '+name+' '+JSON.stringify(details));};
try {
  const desktop=await browser.newPage({viewport:{width:1440,height:900}});
  desktop.on('pageerror',e=>out.errors.push(e.message));
  await desktop.goto(BASE,{waitUntil:'domcontentloaded',timeout:50000});
  await desktop.waitForFunction(()=>document.querySelectorAll('article.track-card').length===50,null,{timeout:40000});
  const ready=await desktop.locator('button.play-button:not([disabled])').count();
  record('50 individually playable buttons',ready===50,{ready});
  const heading=await desktop.locator('h1').innerText();
  const pageText=await desktop.locator('body').innerText();
  record('Uncluttered $100 exclusive offer',pageText.includes('$100')&&pageText.toLowerCase().includes('exclusive')&&heading.includes('BEATS'),{heading});
  const status=await desktop.locator('#resultsText').innerText();
  record('Catalog fully loaded, no blank/loading trap',status.includes('50 beats')&&!/loading|could not/i.test(status),{status});
  record('No unwanted repository link',await desktop.locator('a[href*="github.com"],a[href*="chatgpt.com"]').count()===0);
  const contactLinks=await desktop.locator('a[href^="mailto:axezentai@gmail.com"]').count();
  record('Contact section includes two correct public email links',contactLinks===2,{contactLinks});
  await desktop.locator('article.track-card button.detail-button').first().click();
  const trackEmail=await desktop.locator('#dialogContent .inquiry-email').getAttribute('href');
  record('Beat Details prefills correct artist inquiry email and track ID',Boolean(trackEmail&&trackEmail.startsWith('mailto:axezentai@gmail.com?subject=')&&trackEmail.includes('AXZ-')),{trackEmail});
  const durations=await desktop.locator('#dialogContent .segment-duration').allTextContents();
  record('Every song section displays exact seconds underneath its title',
    durations.length===7&&durations[0].trim()==='11.4 seconds',
    {count:durations.length,first:durations[0]});
  await desktop.locator('#closeDialog').click();
  const bars=await desktop.locator('.cover-soundwave').count();
  record('50 individual beat-art visuals',bars===50,{bars});
  const og=await desktop.locator('meta[property="og:image"]').getAttribute('content');
  record('Absolute correct Facebook preview URL',Boolean(og&&og.startsWith(BASE)&&og.endsWith('.png')),{og});
  const img=await desktop.request.get(og,{timeout:30000});
  const ib=img.ok()?await img.body():Buffer.alloc(0);
  const dims=(ib.length>24&&ib.subarray(0,8).equals(Buffer.from([137,80,78,71,13,10,26,10])))?{width:ib.readUInt32BE(16),height:ib.readUInt32BE(20)}:{width:0,height:0};
  record('Open Graph image loads 1200x630 as PNG',img.ok()&&dims.width===1200&&dims.height===630,{status:img.status(),bytes:ib.length,...dims});
  fs.writeFileSync(path.join(OUTPUT,'facebook-social-card.png'),ib);
  await desktop.screenshot({path:path.join(OUTPUT,'desktop-first-impression.png')});
  await desktop.locator('#catalog').scrollIntoViewIfNeeded();
  await desktop.screenshot({path:path.join(OUTPUT,'desktop-beat-catalog.png')});
  const desktopOverflow=await desktop.evaluate(()=>({innerWidth:innerWidth,documentWidth:document.documentElement.scrollWidth}));
  record('Desktop has no horizontal overflow',desktopOverflow.documentWidth<=desktopOverflow.innerWidth+2,desktopOverflow);
  const mobile=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  mobile.on('pageerror',e=>out.errors.push('Mobile: '+e.message));
  await mobile.goto(BASE,{waitUntil:'domcontentloaded',timeout:50000});
  await mobile.waitForFunction(()=>document.querySelectorAll('article.track-card').length===50,null,{timeout:40000});
  const mWidth=await mobile.evaluate(()=>({innerWidth:innerWidth,documentWidth:document.documentElement.scrollWidth}));
  record('390px mobile no sideways scrolling',mWidth.documentWidth<=mWidth.innerWidth+2,mWidth);
  await mobile.screenshot({path:path.join(OUTPUT,'mobile-first-impression.png')});
  await mobile.locator('#catalog').scrollIntoViewIfNeeded();
  await mobile.screenshot({path:path.join(OUTPUT,'mobile-beat-catalog.png')});
  await mobile.locator('#tracks .play-button').first().click();
  await mobile.waitForFunction(()=>{let a=document.querySelector('#player');return a&&document.querySelector('#playerDialog').open&&a.readyState>=2&&a.currentTime>.1},null,{timeout:30000});
  record('Touch-sized Play button decodes real audio',true);
  const chapters=mobile.locator('#musicArrangement .music-section-jump');
   const chapterCount=await chapters.count();
   record('Full section list and seconds visible while beat plays',
     chapterCount===7 && await mobile.locator('.music-section-duration').count()===chapterCount &&
     (await chapters.first().innerText()).includes('11.4 seconds'),{chapterCount});
   await chapters.nth(3).click();
   await mobile.waitForFunction(()=>Math.abs(document.querySelector('#player').currentTime-68.571)<2,
     null,{timeout:12000});
   const current=(await mobile.locator('.music-section-jump.is-active .music-section-label').innerText()).trim();
   record('Section click seeks to Hook 2 and highlights it',current==='Hook 2',{current});
   await mobile.locator('#closePlayer').click();
  const narrow=await browser.newPage({viewport:{width:320,height:720},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  try {
    await narrow.goto(BASE,{waitUntil:'domcontentloaded',timeout:50000});
    await narrow.waitForFunction(()=>document.querySelectorAll('article.track-card').length===50,null,{timeout:40000});
    const width=await narrow.evaluate(()=>({innerWidth:innerWidth,documentWidth:document.documentElement.scrollWidth}));
    record('320px compact-phone no horizontal overflow',width.documentWidth<=width.innerWidth+2,width);
    await narrow.screenshot({path:path.join(OUTPUT,'compact-phone-first-impression.png')});
  } finally { await narrow.close(); }
  record('No JavaScript errors',out.errors.length===0,{errors:out.errors});
  out.checkedAt=new Date().toISOString();
  fs.writeFileSync(path.join(OUTPUT,'report.json'),JSON.stringify(out,null,2)+'\n');
  console.log('PASS PREMIUM LAUNCH QA:',JSON.stringify(out));
} finally {
  await browser.close();
  if(!fs.existsSync(path.join(OUTPUT,'report.json')))fs.writeFileSync(path.join(OUTPUT,'error.json'),JSON.stringify(out,null,2)+'\n');
}
