// Build the bundled deck into forest/, blue/, plum/ under one HTTP root first.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');

(async () => {
  const [url, output] = process.argv.slice(2);
  if (!url || !output) throw new Error('Usage: node test_palettes.cjs ROOT_URL EVIDENCE_DIR');
  await fs.mkdir(output, { recursive: true });
  const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || undefined });
  const rgb = hex => `rgb(${hex.match(/\w\w/g).map(n => parseInt(n, 16)).join(', ')})`;
  let baseline;
  try {
    for (const name of ['forest', 'blue', 'plum']) {
      const context = await browser.newContext({ viewport: { width: 1280, height: 720 } });
      // Keep font availability identical across themes, including offline use.
      await context.route(/fonts\.googleapis\.com|fonts\.gstatic\.com/, route => route.abort());
      const page = await context.newPage();
      await page.goto(`${url}/${name}/index.html#loop`);
      await page.waitForSelector('#loop.is-current');
      const role = key => page.evaluate(key => getComputedStyle(document.documentElement).getPropertyValue(key).trim(), key);
      const dark = rgb(await role('--dark-surface'));
      const light = rgb(await role('--light-surface'));
      const accent = rgb(await role('--dark-accent'));
      assert.equal(await page.locator('#loop .cycle-flow').evaluate(el => getComputedStyle(el).stroke), accent);
      const box = await page.locator('#loop .cycle').boundingBox();
      if (baseline) assert.deepEqual(box, baseline); else baseline = box;
      await page.screenshot({ path: `${output}/${name}-loop.png` });
      // Exercise paper colors on the same shared component, without per-theme CSS.
      await page.locator('#loop').evaluate(el => el.classList.add('paper'));
      assert.equal(await page.locator('#loop').evaluate(el => getComputedStyle(el).backgroundColor), light);
      assert.equal(await page.locator('#loop .cycle-flow').evaluate(el => getComputedStyle(el).stroke), rgb(await role('--light-accent')));
      await page.screenshot({ path: `${output}/${name}-paper-loop.png` });
      await page.goto(`${url}/${name}/notes.html#loop`);
      await page.waitForSelector('#loop.is-current');
      const spoken = page.locator('#loop .spoken');
      if (name !== 'forest') assert.equal(await spoken.evaluate(el => getComputedStyle(el).backgroundColor), dark);
      assert.equal(await page.locator('#loop .delivery-cue').first().evaluate(el => getComputedStyle(el).backgroundColor), 'rgb(255, 226, 168)');
      const iframe = page.frameLocator('#loop iframe');
      await iframe.locator('.cycle').waitFor();
      assert.equal(await iframe.locator('.cycle-flow').evaluate(el => getComputedStyle(el).stroke), accent);
      assert.equal(await iframe.locator('.cycle-flow').evaluate(el => getComputedStyle(el).animationPlayState), 'paused');
      await page.screenshot({ path: `${output}/${name}-notes.png` });
      await context.close();
    }
    console.log('PASS: three palettes, unchanged loop layout, paper/dark roles, notes, cues and thumbnails');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
