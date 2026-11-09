const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
const only=process.argv[2]||'';
(async()=>{ const dir=path.resolve(__dirname,'../assets'); const b=await chromium.launch();
 const bf=path.join(dir,'boxes.json'); const out=fs.existsSync(bf)?JSON.parse(fs.readFileSync(bf)):{};
 for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html')&&f.startsWith(only))){
  const name=f.replace('.html','');
  const sz= name.startsWith('bg_')?[1080,1920]: name.startsWith('scr_')?[1512,1020]: name.startsWith('card_')?[1100,1560]: name.startsWith('ic_')?[256,256]:[600,1260];
  const p=await b.newPage({viewport:{width:sz[0],height:sz[1]},deviceScaleFactor:1});
  await p.goto('file://'+path.join(dir,f)); await p.waitForTimeout(150);
  out[name]=await p.evaluate(()=>Object.fromEntries([...document.querySelectorAll('[data-hl]')].map(e=>{const r=e.getBoundingClientRect();return [e.dataset.hl,[r.x,r.y,r.width,r.height]]})));
  await p.screenshot({path:path.join(dir,name+'.png'),omitBackground:name.startsWith('ic_')}); await p.close(); }
 fs.writeFileSync(bf,JSON.stringify(out,null,1)); await b.close(); })();
