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
  await desktop.route("https://countapi.mileshilliard.com/api/v1/**",route=>
    route.fulfill({status:200,contentType:"application/json",body:JSON.stringify({value:17})}));
  desktop.on('pageerror',e=>out.errors.push(e.message));
  await desktop.goto(BASE,{waitUntil:'domcontentloaded',timeout:50000});
  await desktop.waitForFunction(()=>document.querySelectorAll('article.track-card').length===100,null,{timeout:40000});
  const ready=await desktop.locator('button.play-button:not([disabled])').count();
  record('All 100 unapproved songs remain unplayable',ready===0,{ready});
  await desktop.waitForFunction(()=>document.getElementById('totalVisits')?.textContent==='17',null,{timeout:15000});
  record('Public cumulative website visit counter appears in footer',
    await desktop.locator('#totalVisits').innerText()==='17');
  await desktop.locator('article.track-card').first().scrollIntoViewIfNeeded();
  await desktop.waitForFunction(()=>document.querySelector('article.track-card .track-play-count')?.textContent.includes('17'),null,{timeout:15000});
  record('Track card shows persistent count from backend read',
    (await desktop.locator('article.track-card .track-play-count').first().innerText()).includes('17'));
  await desktop.evaluate(()=>window.scrollTo(0,0));
  const heading=await desktop.locator('h1').innerText();
  const pageText=await desktop.locator('body').innerText();
  record('Uncluttered $100 exclusive offer',pageText.includes('$100')&&pageText.toLowerCase().includes('exclusive')&&heading.includes('BEATS'),{heading});
  const status=await desktop.locator('#resultsText').innerText();
  record('Catalog fully loaded, no blank/loading trap',status.includes('100 beats')&&!/loading|could not/i.test(status),{status});
  record('No unwanted repository link',await desktop.locator('a[href*="github.com"],a[href*="chatgpt.com"]').count()===0);
  const contactLinks=await desktop.locator('a[href^="mailto:axezentai@gmail.com"]').count();
  record('Contact section includes two correct public email links',contactLinks===2,{contactLinks});
  await desktop.locator('article.track-card button.detail-button').first().click();
  const trackEmail=await desktop.locator('#dialogContent .inquiry-email').getAttribute('href');
  record('Beat Details prefills correct artist inquiry email and track ID',Boolean(trackEmail&&trackEmail.startsWith('mailto:axezentai@gmail.com?subject=')&&trackEmail.includes('AXZ-')),{trackEmail});
  const durations=await desktop.locator('#dialogContent .segment-duration').allTextContents();
  record('Private song arrangement details are not exposed',
    durations.length===0,
    {count:durations.length});
  await desktop.locator('#closeDialog').click();
  const bars=await desktop.locator('.cover-soundwave').count();
  record('100 individual beat-art visuals',bars===100,{bars});
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
  await mobile.route("https://countapi.mileshilliard.com/api/v1/**",route=>
    route.fulfill({status:200,contentType:"application/json",body:JSON.stringify({value:17})}));
  mobile.on('pageerror',e=>out.errors.push('Mobile: '+e.message));
  await mobile.goto(BASE,{waitUntil:'domcontentloaded',timeout:50000});
  await mobile.waitForFunction(()=>document.querySelectorAll('article.track-card').length===100,null,{timeout:40000});
  const mWidth=await mobile.evaluate(()=>({innerWidth:innerWidth,documentWidth:document.documentElement.scrollWidth}));
  record('390px mobile no sideways scrolling',mWidth.documentWidth<=mWidth.innerWidth+2,mWidth);
  await mobile.screenshot({path:path.join(OUTPUT,'mobile-first-impression.png')});
  await mobile.locator('#catalog').scrollIntoViewIfNeeded();
  await mobile.screenshot({path:path.join(OUTPUT,'mobile-beat-catalog.png')});
  const disabledOnMobile=await mobile.locator('#tracks .play-button[disabled]').count();
  record('100 play buttons safely disabled while studio review is pending',disabledOnMobile===100,{disabledOnMobile});
  record('No public player opened accidentally',!await mobile.locator('#playerDialog').evaluate(el=>el.open));
  const narrow=await browser.newPage({viewport:{width:320,height:720},deviceScaleFactor:1,isMobile:true,hasTouch:true});
  await narrow.route("https://countapi.mileshilliard.com/api/v1/**",route=>
    route.fulfill({status:200,contentType:"application/json",body:JSON.stringify({value:17})}));
  try {
    await narrow.goto(BASE,{waitUntil:'domcontentloaded',timeout:50000});
    await narrow.waitForFunction(()=>document.querySelectorAll('article.track-card').length===100,null,{timeout:40000});
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
