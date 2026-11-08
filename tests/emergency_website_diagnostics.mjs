import {chromium} from 'playwright';
import fs from 'node:fs';
import process from 'node:process';
const BASE='https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/';
const browser=await chromium.launch({headless:true,args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});
const report={url:BASE,at:new Date().toISOString(),errors:[],failedRequests:[],relevantResponses:[],states:[]};
try {
 const page=await browser.newPage({viewport:{width:1280,height:800}});
 page.on('pageerror',e=>report.errors.push({type:'pageerror',message:e.message,stack:e.stack}));
 page.on('console',e=>{if(e.type()==='error'||e.type()==='warning')report.errors.push({type:e.type(),message:e.text()})});
 page.on('requestfailed',r=>report.failedRequests.push({url:r.url(),failure:r.failure()}));
 page.on('response',r=>{if(/catalog[.]json|arrangements[.]json|public-preview-manifest[.]json|showcase[.]js|index[.]html|axezent-social-share|Beats-for-Sale\/$/.test(r.url()))report.relevantResponses.push({url:r.url(),status:r.status(),type:r.headers()['content-type'],length:r.headers()['content-length'],cache:r.headers()['cache-control']})});
 const response=await page.goto(BASE,{waitUntil:'domcontentloaded',timeout:40000});
 report.initialStatus=response?.status(); report.initialUrl=page.url();
 for(const pause of [500,2500,6000,13000]){
   await page.waitForTimeout(pause);
   report.states.push(await page.evaluate(()=>{
      const cats=Array.from(document.querySelectorAll('#tracks article.track-card'));
      return {time:Date.now(),readyState:document.readyState,catalogCards:cats.length,results:document.querySelector('#resultsText')?.textContent,
      scripts:Array.from(document.querySelectorAll('script')).map(s=>({src:s.src,loaded:s.readyState})),
      network:performance.getEntriesByType('resource').filter(r=>/showcase|catalog|manifest|arrangements/.test(r.name)).map(r=>({url:r.name,duration:r.duration,responseStatus:r.responseStatus,transfer:r.transferSize}))};
   }));
   if(report.states.at(-1).catalogCards===50)break;
 }
 report.ok=report.states.at(-1).catalogCards===50;
 await page.screenshot({path:'emergency-website-screen.png',fullPage:false});
 console.log('SITE_EMERGENCY_BROWSER_DIAG='+JSON.stringify(report));
} catch(e){report.exception=String(e);console.log('SITE_EMERGENCY_EXCEPTION='+String(e))}
finally{
 fs.writeFileSync('emergency-website-report.json',JSON.stringify(report,null,2)+'\n');
 await browser.close();
}
if(!report.ok)process.exitCode=1;
