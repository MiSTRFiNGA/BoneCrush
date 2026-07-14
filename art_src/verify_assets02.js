/* Playwright verification for asset drop 02. Evidence -> F:\OneDrive\Desktop\Tests\BoneCrush_assets02 */
const { chromium } = require('playwright');
const EVID = 'F:/OneDrive/Desktop/Tests/BoneCrush_assets02/';
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 900, height: 900 } });
  const errors = [], logs = [];
  page.on('console', m => { const t = m.text();
    if (m.type() === 'error') errors.push(t); else if (t.startsWith('[sfx]')) logs.push(t); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));

  // 1. splash (no ?test so it stays on the menu)
  await page.goto('http://localhost:8379/');
  await page.waitForTimeout(1200);
  await page.screenshot({ path: EVID + '01_splash_logo.png' });

  // 2. gameplay with bot + sfx log
  await page.goto('http://localhost:8379/?test=1&sfxlog');
  await page.waitForTimeout(3000);
  await page.screenshot({ path: EVID + '02_board_early.png' });
  await page.waitForTimeout(15000);
  await page.screenshot({ path: EVID + '03_board_mid.png' });
  // zoom on canvas top-left quadrant for icon integrity
  const cvBox = await page.locator('#game').boundingBox();
  await page.screenshot({ path: EVID + '04_zoom_topleft.png',
    clip: { x: cvBox.x, y: cvBox.y, width: cvBox.width / 2, height: cvBox.height / 2 } });
  await page.waitForTimeout(45000);   // total 60s+ of bot play
  await page.screenshot({ path: EVID + '05_board_late.png' });
  await page.screenshot({ path: EVID + '06_zoom_bottomright.png',
    clip: { x: cvBox.x + cvBox.width / 2, y: cvBox.y + cvBox.height / 2, width: cvBox.width / 2, height: cvBox.height / 2 } });
  const dbg = await page.evaluate(() => window.__dbg());
  console.log('DBG', JSON.stringify(dbg).slice(0, 600));
  console.log('CONSOLE_ERRORS', errors.length, JSON.stringify(errors.slice(0, 10)));
  console.log('SFX_EVENTS', logs.length);
  const counts = {}; logs.forEach(l => { const n = l.split(' ')[1]; counts[n] = (counts[n] || 0) + 1; });
  console.log('SFX_COUNTS', JSON.stringify(counts));
  await browser.close();
  process.exit(errors.length ? 1 : 0);
})();
