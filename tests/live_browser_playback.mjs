import { chromium } from 'playwright';
import assert from 'node:assert/strict';

const BASE = 'https://shawncalvinsnelling.github.io/AXEZENT-Beats-for-Sale/';
const browser = await chromium.launch({
  headless: true,
  args: ['--autoplay-policy=no-user-gesture-required', '--no-sandbox']
});

try {
  const page = await browser.newPage({ viewport: {width: 1300, height: 900} });
  page.on('pageerror', e => console.error('BROWSER ERROR:',e.message));
  await page.goto(BASE, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForFunction(() => document.querySelectorAll('article.track-card').length===50, null, { timeout: 30000 });
  const disabled=await page.locator('button.play-button:disabled').count();
  assert.equal(disabled,0, 'All 50 new review tracks must be playable');
  const title=await page.locator('article.track-card h3').first().textContent();
  assert.equal(title.trim(),'Diamond in the Dirt','Expected first featured beat');
  await page.locator('article.track-card button.detail-button').first().click();
  await page.waitForFunction(() => document.getElementById('trackDialog').open);
  const details=await page.locator('#dialogContent').innerText();
  assert.match(details,/0:00/,'The actual track sections must have timecodes');
  assert.match(details,/Verse 2/,'The full arrangement must include a second verse');
  assert.match(details,/\$100/,'The intended $100 full instrumental price must show');
  await page.locator('#closeDialog').click();

  await page.locator('article.track-card button.play-button').first().click();
  await page.waitForFunction(() => {
    const p=document.querySelector('#player');
    return document.querySelector('#playerDialog').open && p && p.readyState>=2 && Number.isFinite(p.duration) && p.duration>60;
  }, null, { timeout: 30000 });
  await page.waitForFunction(() => document.querySelector('#player').currentTime>0.25, null, { timeout: 10000 });
  const before=await page.locator('#player').evaluate(el=>({duration:el.duration,currentTime:el.currentTime,paused:el.paused}));
  assert.ok(before.duration>60 && !before.paused,'Audio must actually run, not just open a modal');
  console.log('LIVE AUDIO STARTED:',title,before);

  await page.locator('#musicSeek').evaluate(el=>{
    el.value='50';el.dispatchEvent(new Event('input',{bubbles:true}));el.dispatchEvent(new Event('change',{bubbles:true}));
  });
  await page.waitForFunction(() => {
    const p=document.querySelector('#player');return p.currentTime>p.duration*.45;
  },null,{timeout:10000});
  const after=await page.locator('#player').evaluate(el=>({currentTime:el.currentTime,duration:el.duration}));
  console.log('SEEK WORKS:',after);

  // A listener should be able to adjust loudness without changing device settings.
  await page.locator('#musicVolume').evaluate(el=>{
    el.value='40';el.dispatchEvent(new Event('input',{bubbles:true}));
  });
  assert.ok(Math.abs(await page.locator('#player').evaluate(el=>el.volume)-0.4)<0.01,
    'Volume slider must set browser audio volume');
  assert.equal((await page.locator('#musicVolumeValue').innerText()).trim(),'40%');
  await page.locator('#musicVolume').evaluate(el=>{
    el.value='100';el.dispatchEvent(new Event('input',{bubbles:true}));
  });
  const beforeBack=await page.locator('#player').evaluate(el=>el.currentTime);
  await page.locator('#musicBack15').click();
  const afterBack=await page.locator('#player').evaluate(el=>el.currentTime);
  assert.ok(beforeBack-afterBack>13,'Rewind control must seek ~15 seconds');
  await page.locator('#musicForward15').click();
  const afterForward=await page.locator('#player').evaluate(el=>el.currentTime);
  assert.ok(afterForward-afterBack>13,'Forward control must seek ~15 seconds');
  console.log('VOLUME AND +/-15 SEC SKIP WORK');

  await page.locator('#musicPause').click();
  assert.equal(await page.locator('#player').evaluate(el=>el.paused),true,'Pause must work');
  await page.locator('#musicRepeat').click();
  assert.equal(await page.locator('#player').evaluate(el=>el.loop),true,'Repeat must work');
  await page.locator('#musicStop').click();
  assert.ok((await page.locator('#player').evaluate(el=>el.currentTime))<.5,'Stop must reset timeline');
  await page.locator('#closePlayer').click();
  assert.equal(await page.locator('#playerDialog').evaluate(el=>el.open),false,'Exit must close');

  // Check more than the first track: late-catalog sources must decode in-browser.
  for(const index of [8,24,49]) {
    const card=page.locator('article.track-card').nth(index);
    const other=await card.locator('h3').textContent();
    await card.locator('button.play-button').click();
    await page.waitForFunction(() => {
      const a=document.querySelector('#player');
      return a && a.readyState>=2 && Number.isFinite(a.duration) && a.duration>60;
    },null,{timeout:30000});
    await page.waitForFunction(() => document.querySelector('#player').currentTime>0.1,null,{timeout:10000});
    console.log('ADDITIONAL BROWSER AUDIO PLAY:',index+1,other.trim());
    await page.locator('#closePlayer').click();
  }

  await page.locator('#region').selectOption({label:'Midwest'});
  await page.waitForFunction(() => {
    const cards=[...document.querySelectorAll('article.track-card')];
    return cards.length>0 && cards.length<50 && cards.every(c=>c.textContent.includes('Midwest'));
  },null,{timeout:10000});
  console.log('PASS: browser verifies four actual MP3s, play, pause, +/-15s, volume, drag seek, repeat, stop, catalog and Details.');
} finally {
  await browser.close();
}
