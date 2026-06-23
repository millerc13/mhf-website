const { chromium } = require('playwright');

const targets = [
  { name: 'yalick-farms', url: 'https://www.yalickfarms.com/', clip: { x: 0, y: 60, width: 1280, height: 520 } },
  { name: 'yalick-shoppes', url: 'https://www.yalickfarms.com/shoppes/', clip: { x: 0, y: 60, width: 1280, height: 520 } },
  { name: 'virginia-car-wash', url: 'https://virginiacarwashco.com/', clip: { x: 0, y: 300, width: 1280, height: 500 } },
  { name: 'burger-king', url: 'https://www.bk.com/', clip: { x: 0, y: 60, width: 1280, height: 460 } },
];

const OUT = '/home/ubuntu-cj/Developer/john-website/site/assets/screenshots';

(async () => {
  const browser = await chromium.launch();
  const ctx = await browser.newContext({
    viewport: { width: 1280, height: 800 },
    userAgent:
      'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0',
  });
  for (const t of targets) {
    const page = await ctx.newPage();
    try {
      await page.goto(t.url, { waitUntil: 'load', timeout: 45000 });
      await page.waitForTimeout(4000);
      // dismiss cookie banners / popups
      const dismissers = [
        'button:has-text("Accept")',
        '#onetrust-accept-btn-handler',
        'button[aria-label="Close" i]',
        'button[aria-label*="close" i]',
        '[class*="close" i] >> visible=true',
      ];
      for (const sel of dismissers) {
        try { await page.locator(sel).first().click({ timeout: 1200 }); await page.waitForTimeout(600); } catch {}
      }
      await page.waitForTimeout(1200);
      await page.screenshot({ path: `${OUT}/${t.name}.jpg`, type: 'jpeg', quality: 82, clip: t.clip });
      console.log(`captured ${t.name}`);
    } catch (e) {
      console.log(`FAILED ${t.name}: ${e.message.split('\n')[0]}`);
    }
    await page.close();
  }
  await browser.close();
})();
