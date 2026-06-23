// Generates branded placeholder slide images (one per property category)
// into site/assets/photos/placeholder-<category>.jpg.
// Run: NODE_PATH=<dir with playwright> node tools/make-placeholders.js
const { chromium } = require('playwright');
const path = require('path');

const OUT = path.join(__dirname, '..', 'site', 'assets', 'photos');

const CATEGORIES = {
  residential: { label: 'Residential', a: '#1b3527', b: '#2c5243' },
  operations: { label: 'Operations', a: '#6b4f1d', b: '#a87f31' },
  retail: { label: 'Retail', a: '#41301f', b: '#7a5c33' },
  land: { label: 'Vacant Land', a: '#2c5243', b: '#5d7d5a' },
};

const html = (c) => `<!DOCTYPE html><html><head><style>
  @import url('https://fonts.googleapis.com/css2?family=Archivo:wght@600;700&family=Fraunces:ital@1&display=swap');
  body { margin:0; width:1200px; height:675px; display:flex; align-items:center; justify-content:center;
    background:
      repeating-conic-gradient(from -90deg at 50% -30%, rgba(247,241,226,0.05) 0deg 5deg, transparent 5deg 11deg),
      radial-gradient(900px 500px at 80% -10%, rgba(200,151,58,0.25), transparent 60%),
      linear-gradient(160deg, ${c.a} 0%, ${c.b} 100%);
    font-family: 'Archivo', sans-serif; }
  .inner { text-align:center; color:#f7f1e2; }
  .frame { border:1.5px solid rgba(247,241,226,0.35); padding:54px 84px; }
  .cat { font-size:15px; font-weight:700; letter-spacing:7px; color:#e2c179; margin-top:30px; }
  .soon { font-family:'Fraunces', serif; font-style:italic; font-size:30px; margin-top:10px; opacity:.92; }
</style></head><body>
  <div class="frame"><div class="inner">
    <svg viewBox="0 0 64 60" width="120" height="112" xmlns="http://www.w3.org/2000/svg">
      <path d="M32 4 C17 4 6.5 15 4.5 28.5 C8.5 24 15 24 18.5 28.5 C22 24 28.5 24 32 28.5 C35.5 24 42 24 45.5 28.5 C49 24 55.5 24 59.5 28.5 C57.5 15 47 4 32 4 Z" fill="#c8973a"/>
      <rect x="30.6" y="6" width="2.8" height="40" rx="1.4" fill="#f7f1e2"/>
      <path d="M33.4 46 c0 7 -10.5 7 -10.5 0" fill="none" stroke="#f7f1e2" stroke-width="2.8" stroke-linecap="round"/>
    </svg>
    <div class="cat">${c.label.toUpperCase()}</div>
    <div class="soon">Photograph coming soon</div>
  </div></div>
</body></html>`;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 675 } });
  for (const [key, c] of Object.entries(CATEGORIES)) {
    await page.setContent(html(c), { waitUntil: 'networkidle' });
    await page.waitForTimeout(800);
    await page.screenshot({ path: path.join(OUT, `placeholder-${key}.jpg`), type: 'jpeg', quality: 82 });
    console.log(`placeholder-${key}.jpg`);
  }
  await browser.close();
})();
