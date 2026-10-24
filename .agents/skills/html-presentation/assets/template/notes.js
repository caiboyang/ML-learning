(() => {
  const notes = [...document.querySelectorAll('.slide-note')];
  const toolbar = document.createElement('div');
  toolbar.className = 'notes-toolbar';
  toolbar.innerHTML = '<span class="notes-position" aria-live="polite"></span><span class="notes-keys">↑ 上一页 · ↓ 下一页 <span>／ 两栏按先左后右阅读</span></span><span class="sync-status" role="status">演示窗口未连接</span><button class="open-presentation" type="button">打开演示窗口</button><button class="toggle-overview" type="button">备课总览</button>';
  document.body.prepend(toolbar);
  const position = toolbar.querySelector('.notes-position');
  const toggle = toolbar.querySelector('.toggle-overview');
  let current = 0;
  let overview = false;

  const timer = document.createElement('div');
  timer.className = 'speaker-timer';
  timer.setAttribute('aria-label', '演讲计时');
  timer.innerHTML = '<div class="timer-total"><span>总用时</span><span class="timer-elapsed" role="timer" aria-label="总用时">00:00</span><span class="timer-budget"></span></div><div class="timer-page"><span>本页用时</span><span class="page-elapsed" role="timer" aria-label="本页用时">00:00</span><span class="page-budget"></span></div><button class="timer-toggle" type="button" aria-keyshortcuts="T">开始计时</button><button class="timer-reset" type="button">全部重置</button><span class="timer-help">T 开始／暂停</span>';
  toolbar.after(timer);
  const deckKey = `${document.body.dataset.deckId}:${location.pathname.replace(/[^/]*$/, '')}`;
  const timerKey = `presentation-timer:${deckKey}`;
  timer.querySelector('.timer-budget').textContent = document.body.dataset.budgetLabel;
  let clock = JSON.parse(sessionStorage.getItem(timerKey)) || { elapsed: 0, startedAt: null, pageId: null, pageElapsed: 0, pageStartedAt: null };
  clock.visits ||= [];
  let timerReady = false;
  const timerToggle = timer.querySelector('.timer-toggle');
  function elapsedTime(page = false, now = Date.now()) {
    const startedAt = page ? clock.pageStartedAt : clock.startedAt;
    return (page ? clock.pageElapsed : clock.elapsed) + (startedAt === null ? 0 : now - startedAt);
  }
  function formatTime(seconds) {
    return `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`;
  }
  function renderTimer() {
    const totalSeconds = Math.floor(elapsedTime() / 1000);
    const pageSeconds = Math.floor(elapsedTime(true) / 1000);
    const proposed = notes[current].dataset.budgetSeconds;
    const budget = proposed === '' ? null : Number(proposed);
    timer.querySelector('.timer-elapsed').textContent = formatTime(totalSeconds);
    timer.querySelector('.page-elapsed').textContent = formatTime(pageSeconds);
    timer.querySelector('.page-budget').textContent = budget === null ? '未设预算' : `预算 ${formatTime(budget)}${pageSeconds > budget ? ` · 超时 ${formatTime(pageSeconds - budget)}` : ''}`;
    timer.querySelector('.timer-page').dataset.timing = budget !== null && pageSeconds > budget ? 'over' : 'normal';
    timerToggle.textContent = clock.startedAt !== null ? '暂停' : clock.elapsed ? '继续' : '开始计时';
  }
  function saveTimer() {
    sessionStorage.setItem(timerKey, JSON.stringify(clock));
    renderTimer();
  }
  function updatePageTimer() {
    if (!timerReady) return;
    if (clock.pageId !== notes[current].id) {
      const elapsed = elapsedTime(true);
      if (clock.pageId && elapsed > 0) clock.visits.push({ id: clock.pageId, elapsed_ms: elapsed });
      clock.pageId = notes[current].id;
      clock.pageElapsed = 0;
      clock.pageStartedAt = clock.startedAt === null ? null : Date.now();
    }
    saveTimer();
  }
  function toggleTimer() {
    if (clock.startedAt === null) {
      clock.startedAt = Date.now();
      clock.pageStartedAt = clock.startedAt;
    } else {
      clock.elapsed = elapsedTime();
      clock.pageElapsed = elapsedTime(true);
      clock.startedAt = null;
      clock.pageStartedAt = null;
    }
    saveTimer();
  }
  timerToggle.addEventListener('click', toggleTimer);
  timer.querySelector('.timer-reset').addEventListener('click', () => {
    clock = { elapsed: 0, startedAt: null, pageId: notes[current].id, pageElapsed: 0, pageStartedAt: null, visits: [] };
    saveTimer();
  });
  setInterval(renderTimer, 250);

  // Kept in the overview so live notes and projection remain uncluttered.
  const exportButton = document.createElement('button');
  exportButton.type = 'button';
  exportButton.className = 'export-rehearsal';
  exportButton.textContent = '导出本次彩排时间（重置前保存）';
  document.querySelector('.quick').prepend(exportButton);
  exportButton.addEventListener('click', () => {
    const now = Date.now();
    const visits = [...clock.visits];
    const active = elapsedTime(true, now);
    if (clock.pageId && active > 0) visits.push({ id: clock.pageId, elapsed_ms: active });
    const report = {
      deck_id: document.body.dataset.deckId,
      exported_at: new Date(now).toISOString(),
      running: clock.startedAt !== null,
      total_elapsed_ms: elapsedTime(false, now),
      visits,
      slides: notes.map(note => {
        const matching = visits.filter(visit => visit.id === note.id);
        const elapsed = matching.reduce((sum, visit) => sum + visit.elapsed_ms, 0);
        const budget = note.dataset.budgetSeconds === '' ? null : Number(note.dataset.budgetSeconds) * 1000;
        return { id: note.id, title: note.querySelector('h2').textContent,
          visits: matching.length, elapsed_ms: elapsed, budget_ms: budget,
          difference_ms: budget === null || !matching.length ? null : elapsed - budget };
      })
    };
    const url = URL.createObjectURL(new Blob([JSON.stringify(report, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = `${document.body.dataset.deckId}-rehearsal.json`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  });

  const status = toolbar.querySelector('.sync-status');
  const sessionKey = `presentation-session:${deckKey}`;
  const session = sessionStorage.getItem(sessionKey) || crypto.randomUUID();
  sessionStorage.setItem(sessionKey, session);
  const channel = new BroadcastChannel(`presentation-${deckKey}-${session}`);
  let lastSeen = 0;
  let openedAt = 0;
  function syncSlide() {
    channel.postMessage({ type: 'slide', id: notes[current].id });
  }
  channel.addEventListener('message', ({ data }) => {
    if (!data || !['ready', 'state'].includes(data.type)) return;
    const index = notes.findIndex(note => note.id === data.id);
    if (index < 0) return;
    lastSeen = Date.now();
    status.dataset.connected = 'true';
    const screen = data.fullscreenFailed ? ' · 请在演示窗手动全屏' : '';
    const video = data.id === 'video' ? (data.blocked ? ' · 请在演示窗按 V 启用声音' : data.playing ? ' · 视频播放中' : ' · 视频已暂停') : '';
    status.textContent = `已连接 · 第 ${index + 1} 页${video}${screen}`;
    if (data.type === 'ready') syncSlide();
  });
  toolbar.querySelector('.open-presentation').addEventListener('click', () => {
    const url = new URL('index.html', location.href);
    url.searchParams.set('presenter', session);
    url.hash = notes[current].id;
    const audience = window.open(url.href, `presentation-${session}`, 'popup,width=1280,height=720');
    if (!audience) status.textContent = '弹窗被拦截，请允许后重新打开';
    else { openedAt = Date.now(); status.textContent = '正在连接 · 请将新窗口拖到扩展屏'; syncSlide(); }
  });
  setInterval(() => {
    channel.postMessage({ type: 'ping' });
    if ((lastSeen || openedAt) && Date.now() - (lastSeen || openedAt) > 6500) {
      status.dataset.connected = 'false';
      status.textContent = '未连接 · 请用同一 Chrome 浏览器重新打开';
    }
  }, 2000);

  notes.forEach(note => {
    const spoken = note.querySelector('.spoken');
    const content = document.createElement('div');
    content.className = 'script-content';
    [...spoken.children].filter(child => !child.classList.contains('label')).forEach(child => content.append(child));
    spoken.append(content);
  });

  function fit() {
    if (overview) return;
    const note = notes[current];
    const content = note.querySelector('.script-content');
    note.classList.remove('script-scroll');
    let size = 30;
    note.style.setProperty('--script-size', `${size}px`);
    while (size > 20 && (content.scrollWidth > content.clientWidth + 2 || content.scrollHeight > content.clientHeight + 2)) {
      size -= 1;
      note.style.setProperty('--script-size', `${size}px`);
    }
    // Small windows retain every word at a readable size instead of clipping.
    if (content.scrollWidth > content.clientWidth + 2 || content.scrollHeight > content.clientHeight + 2) {
      note.classList.add('script-scroll');
    }
  }

  function show(index, updateHash = true) {
    current = Math.max(0, Math.min(notes.length - 1, index));
    notes.forEach((note, i) => {
      note.classList.toggle('is-current', i === current);
      if (!overview && i !== current) note.setAttribute('aria-hidden', 'true');
      else note.removeAttribute('aria-hidden');
    });
    position.textContent = `${String(current + 1).padStart(2, '0')} / ${notes.length}`;
    document.title = `${current + 1}. ${notes[current].querySelector('h2').textContent} · 讲稿`;
    if (updateHash) history.replaceState(null, '', `#${notes[current].id}`);
    notes[current].querySelector('.script-content').scrollTop = 0;
    fit();
    updatePageTimer();
    syncSlide();
  }

  function setOverview(value) {
    overview = value;
    document.body.classList.toggle('notes-deck', !overview);
    document.body.classList.toggle('notes-overview', overview);
    toggle.textContent = overview ? '返回逐页讲稿' : '备课总览';
    show(current, false);
    if (overview) {
      history.replaceState(null, '', '#top');
      window.scrollTo({ top: 0, behavior: 'instant' });
    } else {
      history.replaceState(null, '', `#${notes[current].id}`);
      window.scrollTo({ top: 0, behavior: 'instant' });
      fit();
    }
  }

  function readHash() {
    const id = location.hash.slice(1);
    const index = notes.findIndex(note => note.id === id);
    if (index >= 0) {
      if (overview) {
        current = index;
        setOverview(false);
      }
      show(index, false);
    } else if (id === 'top') setOverview(true);
  }

  toggle.addEventListener('click', () => setOverview(!overview));
  window.addEventListener('hashchange', readHash);
  window.addEventListener('resize', fit);
  document.addEventListener('keydown', event => {
    if (event.altKey || event.ctrlKey || event.metaKey || event.shiftKey || event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
    if (event.key.toLowerCase() === 't') {
      event.preventDefault();
      if (!event.repeat) toggleTimer();
      return;
    }
    if (overview) return;
    if (notes[current].id === 'video' && ['v', 'r'].includes(event.key.toLowerCase())) {
      event.preventDefault();
      if (!event.repeat) channel.postMessage({ type: 'video', action: event.key.toLowerCase() === 'r' ? 'restart' : 'toggle' });
      return;
    }
    const changes = { ArrowDown: 1, PageDown: 1, ArrowUp: -1, PageUp: -1 };
    if (!(event.key in changes) && event.key !== 'Home' && event.key !== 'End') return;
    event.preventDefault();
    if (event.repeat) return;
    show(event.key === 'Home' ? 0 : event.key === 'End' ? notes.length - 1 : current + changes[event.key]);
  });

  document.body.classList.add('notes-deck');
  // #top identifies overview mode, not the slide currently being presented.
  const initialId = location.hash === '#top' ? clock.pageId : location.hash.slice(1);
  const initialIndex = notes.findIndex(note => note.id === initialId);
  show(Math.max(0, initialIndex), false);
  readHash();
  timerReady = true;
  updatePageTimer();
  document.fonts.ready.then(fit);
  channel.postMessage({ type: 'hello' });
})();
