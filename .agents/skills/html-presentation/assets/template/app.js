'use strict';
const viewport = document.getElementById('presentation');
const scenes = [...document.querySelectorAll('.scene')];
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
let current = 0;
let presenterChannel = null;
let playbackBlocked = false;
let fullscreenFailed = false;
let scrollFrame = false;
let wheelTotal = 0;
let lastWheel = 0;
let navigationUntil = 0;

const film = document.getElementById('demo-film');
const deckKey = `${document.body.dataset.deckId}:${location.pathname.replace(/[^/]*$/, '')}`;
const filmHint = document.getElementById('film-hint');
function playFilm() {
  if (!film) return;
  if (film.ended) film.currentTime = 0;
  film.play().catch(() => {
    playbackBlocked = true;
    reportState();
    filmHint.textContent = 'Press V to play with sound';
    filmHint.hidden = false;
  });
}
film?.addEventListener('play', () => { filmHint.hidden = true; playbackBlocked = false; reportState(); });
film?.addEventListener('pause', () => {
  filmHint.textContent = film.ended ? 'Press ↓ to continue · R to replay' : 'Press V to resume';
  filmHint.hidden = false;
  reportState();
});
film?.addEventListener('ended', () => {
  filmHint.textContent = 'Press ↓ to continue · R to replay';
  filmHint.hidden = false;
  reportState();
});
function markCurrent(index) {
  const changed = current !== index;
  current = index;
  if (changed && scenes[index].id === 'video') playFilm();
  else if (scenes[index].id !== 'video') film?.pause();
  scenes.forEach((scene, i) => {
    scene.classList.toggle('is-current', i === index);
    if (i === index) scene.classList.add('has-entered');
  });
  document.getElementById('progressFill').style.width = `${(index + 1) / scenes.length * 100}%`;
  document.title = `${scenes[index].dataset.title} · ${document.body.dataset.speaker}`;
  const hash = `#${scenes[index].id}`;
  if (location.hash !== hash) history.replaceState(null, '', hash);
  reportState();
}
function go(index, smooth = true) {
  const next = Math.max(0, Math.min(scenes.length - 1, index));
  navigationUntil = Date.now() + (smooth && !reducedMotion.matches ? 650 : 80);
  markCurrent(next);
  viewport.scrollTo({top: scenes[next].offsetTop, behavior: smooth && !reducedMotion.matches ? 'smooth' : 'instant'});
}
viewport.addEventListener('scroll', () => {
  if (scrollFrame) return;
  scrollFrame = true;
  requestAnimationFrame(() => {
    scrollFrame = false;
    if (Date.now() < navigationUntil) return;
    const top = viewport.scrollTop;
    let nearest = 0;
    for (let i = 1; i < scenes.length; i++) {
      if (Math.abs(scenes[i].offsetTop - top) < Math.abs(scenes[nearest].offsetTop - top)) nearest = i;
    }
    if (nearest !== current) markCurrent(nearest);
  });
}, {passive: true});

// A wheel gesture moves one scene. Taller mobile layouts retain native scrolling.
viewport.addEventListener('wheel', event => {
  if (event.ctrlKey || Math.abs(event.deltaX) > Math.abs(event.deltaY)) return;
  if (scenes[current].offsetHeight > viewport.clientHeight + 4) return;
  event.preventDefault();
  const now = Date.now();
  if (now < navigationUntil) { lastWheel = now; return; }
  if (now - lastWheel > 180) wheelTotal = 0;
  lastWheel = now;
  wheelTotal += event.deltaY * (event.deltaMode === 1 ? 16 : event.deltaMode === 2 ? viewport.clientHeight : 1);
  if (Math.abs(wheelTotal) >= 24) {
    go(current + Math.sign(wheelTotal));
    wheelTotal = 0;
  }
}, {passive: false});

document.addEventListener('keydown', event => {
  if (event.altKey || event.ctrlKey || event.metaKey || event.target.closest('input, textarea, select, [contenteditable="true"]')) return;
  if (scenes[current].id === 'video' && ['v', 'r'].includes(event.key.toLowerCase())) {
    event.preventDefault();
    if (event.repeat) return;
    if (event.key.toLowerCase() === 'r') { film.currentTime = 0; playFilm(); }
    else if (film.paused) playFilm();
    else film?.pause();
    return;
  }
  const forward = ['ArrowDown', 'ArrowRight', 'PageDown', ' '].includes(event.key);
  const back = ['ArrowUp', 'ArrowLeft', 'PageUp'].includes(event.key) || (event.key === ' ' && event.shiftKey);
  if (!forward && !back && event.key !== 'Home' && event.key !== 'End') return;
  event.preventDefault();
  if (event.repeat && Date.now() < navigationUntil) return;
  if (event.key === 'Home') go(0);
  else if (event.key === 'End') go(scenes.length - 1);
  else go(current + (back ? -1 : 1));
});
window.addEventListener('hashchange', () => {
  const index = scenes.findIndex(scene => scene.id === location.hash.slice(1));
  if (index >= 0) go(index, false);
});
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => go(current, false), 100);
});
if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
const initial = scenes.findIndex(scene => scene.id === location.hash.slice(1));
go(initial < 0 ? 0 : initial, false);

// Only a window opened by this speaker guide joins its private local session.
function reportState(type = 'state') {
  presenterChannel?.postMessage({ type, id: scenes[current].id, playing: Boolean(film && !film.paused), blocked: playbackBlocked, fullscreenFailed });
}
const presenterSession = new URLSearchParams(location.search).get('presenter');
if (presenterSession && /^[a-f0-9-]{36}$/.test(presenterSession)) {
  presenterChannel = new BroadcastChannel(`presentation-${deckKey}-${presenterSession}`);
  presenterChannel.addEventListener('message', ({ data }) => {
    if (!data) return;
    if (data.type === 'slide') {
      const index = scenes.findIndex(scene => scene.id === data.id);
      if (index >= 0 && index !== current) go(index);
    } else if (data.type === 'hello') reportState('ready');
    else if (data.type === 'ping') reportState();
    else if (data.type === 'video' && scenes[current].id === 'video') {
      if (data.action === 'restart') { film.currentTime = 0; playFilm(); }
      else if (data.action === 'toggle') { if (film.paused) playFilm(); else film?.pause(); }
    }
  });
  reportState('ready');
  const setup = document.createElement('div');
  setup.className = 'projection-setup';
  setup.innerHTML = '<p>先将这个窗口拖到扩展屏，再点击下方按钮。之后回到讲稿，用 ↑ ↓ 翻页；视频页用 V 暂停、R 重播。</p><button type="button">准备投影 · 全屏并启用视频</button>';
  document.body.append(setup);
  setup.querySelector('button').addEventListener('click', () => {
    if (document.documentElement.requestFullscreen) {
      document.documentElement.requestFullscreen().catch(() => { fullscreenFailed = true; reportState(); });
    } else { fullscreenFailed = true; reportState(); }
    if (scenes[current].id === 'video') playFilm();
    else if (film) {
      // Activate this media element once, silently, before remote playback.
      const volume = film.volume;
      film.volume = 0;
      film.play().then(() => {
        if (scenes[current].id !== 'video') { film?.pause(); film.currentTime = 0; }
      }).catch(() => { playbackBlocked = true; }).finally(() => { film.volume = volume; reportState(); });
    }
    setup.remove();
  });
}
