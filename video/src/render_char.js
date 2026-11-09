const { chromium } = require('playwright'); const fs=require('fs'); const path=require('path');
(async()=>{const dir=path.resolve(__dirname,'../assets/char');const b=await chromium.launch();
 for(const f of fs.readdirSync(dir).filter(f=>f.endsWith('.html'))){
  const svg=fs.readFileSync(path.join(dir,f),'utf8'); const m=svg.match(/width="(\d+)" height="(\d+)"/);
  const p=await b.newPage({viewport:{width:+m[1],height:+m[2]}}); await p.setContent(svg);
  await p.screenshot({path:path.join(dir,f.replace('.html','.png')),omitBackground:true}); await p.close();}
 await b.close();})();
