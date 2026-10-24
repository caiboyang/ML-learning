// Optional integration test: build the bundled example, serve it, then pass its URL.
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs/promises');
const path = require('node:path');

(async () => {
  const url = process.argv[2];
  const output = process.argv[3];
  if (!url || !output) throw new Error('Usage: node test_browser.cjs URL EVIDENCE_DIR');
  await fs.mkdir(output, { recursive: true });
  const browser = await chromium.launch({ channel: process.env.PLAYWRIGHT_CHANNEL || undefined });
  try {
    const context = await browser.newContext({ viewport: { width: 1280, height: 720 }, acceptDownloads: true });
    const page = await context.newPage();
    const errors = [];
    context.on('page', p => p.on('pageerror', e => errors.push(e.message)));
    page.on('pageerror', e => errors.push(e.message));
    await page.clock.install({ time: new Date('2026-01-01T12:00:00Z') });
    await page.goto(`${url}/notes.html`);
    const stored = () => page.evaluate(() => JSON.parse(sessionStorage.getItem(
      Object.keys(sessionStorage).find(key => key.startsWith('presentation-timer:')))));
    const expectedPage = async (id) => {
      await page.waitForFunction(id => document.querySelector('.slide-note.is-current').id === id, id);
      await audience.waitForFunction(id => document.querySelector('.scene.is-current').id === id, id);
    };
    const popup = page.waitForEvent('popup');
    await page.getByRole('button', { name: '打开演示窗口', exact: true }).click();
    const audience = await popup;
    await audience.waitForLoadState();
    await audience.getByRole('button', { name: /准备投影/ }).click();
    await expectedPage('cover');
    await page.keyboard.press('ArrowDown');
    await expectedPage('start');
    await page.keyboard.press('t');
    await page.clock.fastForward(10000);
    await page.keyboard.press('ArrowDown');
    await expectedPage('loop');
    await page.clock.fastForward(5000);
    await page.keyboard.press('t');
    let state = await stored();
    assert.equal(state.visits.length, 1);
    const startTime = state.visits[0].elapsed_ms;
    assert.ok(startTime >= 10000 && startTime < 11000);
    const pauseTotal = state.elapsed;
    await page.clock.fastForward(20000);
    assert.equal((await stored()).elapsed, pauseTotal);
    await page.keyboard.press('ArrowUp');
    await expectedPage('start');
    assert.equal((await stored()).pageStartedAt, null);
    await page.keyboard.press('t');
    await page.clock.fastForward(3000);
    await page.keyboard.press('t');
    const beforeReload = await stored();
    await page.reload();
    assert.deepEqual(await stored(), beforeReload);
    await expectedPage('start');
    await audience.reload();
    await expectedPage('start');
    await audience.getByRole('button', { name: /准备投影/ }).click();
    const exportReport = async name => {
      await page.getByRole('button', { name: '备课总览', exact: true }).click();
      const download = page.waitForEvent('download');
      await page.getByRole('button', { name: /导出本次彩排时间/ }).click();
      const file = path.join(output, name);
      await (await download).saveAs(file);
      const report = JSON.parse(await fs.readFile(file, 'utf8'));
      await page.getByRole('button', { name: '返回逐页讲稿', exact: true }).click();
      return report;
    };
    // Overview uses #top, so its active slide must survive outside the URL hash.
    await page.getByRole('button', { name: '备课总览', exact: true }).click();
    const pausedOverview = await stored();
    await page.reload();
    assert.deepEqual(await stored(), pausedOverview);
    assert.ok(await page.locator('body').evaluate(el => el.classList.contains('notes-overview')));
    await expectedPage('start');
    await page.getByRole('button', { name: '返回逐页讲稿', exact: true }).click();
    const report = await exportReport('rehearsal.json');
    assert.deepEqual(report.visits.map(v => v.id), ['start', 'loop', 'start']);
    assert.equal(report.slides.find(s => s.id === 'start').visits, 2);
    assert.equal(report.slides.find(s => s.id === 'qa').difference_ms, null);
    assert.ok(Math.abs(report.visits.reduce((n, v) => n + v.elapsed_ms, 0) - report.total_elapsed_ms) < 100);
    const secondReport = await exportReport('rehearsal-repeat.json');
    assert.deepEqual(secondReport.visits, report.visits); // Export does not double-count.
    await page.keyboard.press('t');
    await page.clock.fastForward(2000);
    const running = await exportReport('rehearsal-running.json');
    assert.equal(running.running, true);
    assert.ok(running.total_elapsed_ms > report.total_elapsed_ms);
    await page.getByRole('button', { name: '备课总览', exact: true }).click();
    const runningOverview = await stored();
    await page.reload();
    assert.deepEqual(await stored(), runningOverview);
    assert.ok(await page.locator('body').evaluate(el => el.classList.contains('notes-overview')));
    await expectedPage('start');
    await page.clock.fastForward(1000);
    await page.getByRole('button', { name: '返回逐页讲稿', exact: true }).click();
    assert.notEqual((await stored()).startedAt, null);
    await page.keyboard.press('t');
    await page.getByRole('button', { name: '全部重置', exact: true }).click();
    const empty = await exportReport('rehearsal-reset.json');
    assert.equal(empty.total_elapsed_ms, 0);
    assert.equal(empty.visits.length, 0);
    for (const id of ['cover', 'start', 'loop', 'qa']) {
      await page.goto(`${url}/notes.html#${id}`);
      await expectedPage(id);
      await audience.waitForTimeout(800); // Smooth scroll reaches the destination.
      await audience.screenshot({ path: path.join(output, `slide-${id}.png`) });
      if (id === 'loop') {
        const flow = audience.locator('#loop .cycle-flow');
        const offset = () => flow.evaluate(el => getComputedStyle(el).strokeDashoffset);
        const before = await offset();
        await audience.waitForTimeout(400);
        assert.notEqual(await offset(), before, 'Loop path must visibly move');
        assert.deepEqual(await audience.locator('#loop .cycle-node').evaluateAll(nodes =>
          nodes.map(el => getComputedStyle(el).animationDelay)), ['0s', '2s', '4s']);
        assert.equal(await page.frameLocator('#loop iframe').locator('.cycle-flow')
          .evaluate(el => getComputedStyle(el).animationPlayState), 'paused');
        await audience.locator('#loop').evaluate(el => el.classList.add('paper'));
        assert.equal(await flow.evaluate(el => getComputedStyle(el).stroke), 'rgb(55, 111, 72)');
        await audience.screenshot({ path: path.join(output, 'loop-paper.png') });
        await audience.locator('#loop').evaluate(el => el.classList.remove('paper'));
        await audience.emulateMedia({ reducedMotion: 'reduce' });
        assert.equal(await flow.evaluate(el => getComputedStyle(el).animationName), 'none');
        assert.ok(await audience.locator('#loop .cycle-arrow').isVisible());
        await audience.emulateMedia({ reducedMotion: 'no-preference' });
      } else if (id === 'qa') {
        const flow = audience.locator('#loop .cycle-flow');
        assert.equal(await flow.evaluate(el => getComputedStyle(el).animationPlayState), 'paused');
        const before = await flow.evaluate(el => getComputedStyle(el).strokeDashoffset);
        await audience.waitForTimeout(300);
        assert.equal(await flow.evaluate(el => getComputedStyle(el).strokeDashoffset), before);
      }
    }
    await page.screenshot({ path: path.join(output, 'notes-desktop.png') });
    const narrow = await context.newPage();
    await narrow.setViewportSize({ width: 390, height: 844 });
    await narrow.goto(`${url}/notes.html`);
    await narrow.evaluate(() => document.fonts.ready);
    await narrow.screenshot({ path: path.join(output, 'notes-narrow.png') });
    assert.ok(await narrow.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 2));
    // Cold context: no external network or font cache, while the local server remains reachable.
    const localOnly = await browser.newContext({ viewport: { width: 1280, height: 720 } });
    await localOnly.route('**/*', route => new URL(route.request().url()).origin === new URL(url).origin
      ? route.continue() : route.abort());
    const fallback = await localOnly.newPage();
    await fallback.goto(`${url}/index.html#loop`);
    await fallback.evaluate(() => document.fonts.ready);
    assert.equal(await fallback.locator('.scene.is-current').getAttribute('id'), 'loop');
    await fallback.screenshot({ path: path.join(output, 'slide-local-font-fallback.png') });
    await localOnly.close();
    assert.equal(errors.length, 0, errors.join('\n'));
    console.log('PASS: popup sync/reload, rehearsal pause/revisit/reload/export/reset, loop motion/themes/thumbnail/reduced-motion, screenshots and narrow notes.');
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
