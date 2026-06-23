// Renders an aerial (satellite) image for each pinned property using
// Leaflet + Esri World Imagery, screenshotted via Playwright.
// Run from anywhere: node tools/capture-aerials.js
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const ROOT = path.join(__dirname, '..');
const OUT = path.join(ROOT, 'site', 'assets', 'locations');

// Load the property data (a browser global) in a sandbox
const sandbox = { window: {} };
vm.runInNewContext(fs.readFileSync(path.join(ROOT, 'site/js/properties.js'), 'utf8'), sandbox);
const props = sandbox.window.MHF_PROPERTIES.filter((p) => p.coords);

const slug = (name) =>
  name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');

// Wider zoom for land parcels, tight for buildings
const zoomFor = (p) => (p.category === 'land' ? 15 : 17);

const pageHtml = `<!DOCTYPE html><html><head>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>html,body,#m{margin:0;width:900px;height:560px}</style>
</head><body><div id="m"></div><script>
const map = L.map('m', { zoomControl: false, attributionControl: true });
L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
  maxZoom: 18,
  attribution: 'Imagery &copy; Esri',
}).addTo(map);
window.show = (lat, lng, z) => new Promise((resolve) => {
  let pending = 0, started = false;
  const layer = map.eachLayer ? null : null;
  map.setView([lat, lng], z);
  setTimeout(resolve, 4500); // settle: tiles load fast; fixed wait keeps it simple
});
</script></body></html>`;

(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 560 } });
  await page.setContent(pageHtml, { waitUntil: 'networkidle' });
  for (const p of props) {
    if (p.name === '22 Burger King Locations') continue; // generic pin — uses brand image instead
    const s = slug(p.name);
    await page.evaluate(
      ([lat, lng, z]) => window.show(lat, lng, z),
      [p.coords[0], p.coords[1], zoomFor(p)]
    );
    await page.waitForTimeout(5000);
    await page.screenshot({ path: path.join(OUT, `${s}.jpg`), type: 'jpeg', quality: 80 });
    console.log(`aerial: ${s}`);
  }
  await browser.close();
})();
