(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const lessons = [...document.querySelectorAll('.lesson')];
  let current = 0;
  const market = [-6, -4, -2, 0, 2, 4, 6];
  const residual = [1, -1, -1, 2, -1, -1, 1];
  const mean = xs => xs.reduce((a, b) => a + b, 0) / xs.length;
  function regress(x, y) {
    const mx = mean(x), my = mean(y);
    const beta = x.reduce((sum, v, i) => sum + (v - mx) * (y[i] - my), 0) /
      x.reduce((sum, v) => sum + (v - mx) ** 2, 0);
    const alpha = my - beta * mx;
    const total = y.reduce((sum, v) => sum + (v - my) ** 2, 0);
    const error = y.reduce((sum, v, i) => sum + (v - alpha - beta * x[i]) ** 2, 0);
    return {beta, alpha, r2: total < 1e-20 ? null : 1 - error / total};
  }
  const signed = n => (n >= 0 ? '+' : '') + n.toFixed(2);
  function svgEl(name, attrs, text) {
    const el = document.createElementNS('http://www.w3.org/2000/svg', name);
    Object.entries(attrs || {}).forEach(([key, value]) => el.setAttribute(key, String(value)));
    if (text !== undefined) el.textContent = text;
    return el;
  }
  function drawBeta() {
    const b = Number($('beta-slider').value), a = Number($('alpha-slider').value);
    const noise = Number($('noise-slider').value);
    const yValues = market.map((v, i) => a + b * v + noise * residual[i]);
    const fit = regress(market, yValues);
    $('beta-label').textContent = b.toFixed(1);
    $('alpha-label').textContent = signed(a) + '% / 月';
    $('noise-label').textContent = noise.toFixed(1);
    $('fit-beta').textContent = fit.beta.toFixed(2);
    $('fit-alpha').textContent = signed(fit.alpha) + '%';
    $('fit-r2').textContent = fit.r2 === null ? '未定义' : (fit.r2 * 100).toFixed(1) + '%';
    $('sample-rows').replaceChildren(...market.map((x, i) => {
      const row = document.createElement('tr');
      [String(i + 1), signed(x), signed(a + b * x), signed(noise * residual[i]), signed(yValues[i])].forEach(value => {
        const cell = document.createElement('td'); cell.textContent = value; row.append(cell);
      });
      return row;
    }));
    const host = $('beta-chart'), width = Math.floor(host.getBoundingClientRect().width);
    if (width < 100) return;
    const height = 300, left = 43, right = 16, top = 30, bottom = 46;
    const px = v => left + (v + 7) / 14 * (width - left - right);
    const py = v => top + (18 - v) / 36 * (height - top - bottom);
    const svg = svgEl('svg', {viewBox: `0 0 ${width} ${height}`, role: 'img', 'aria-label': `合成散点：beta ${b}，月度 alpha ${a}%，残差幅度 ${noise}`});
    svg.append(svgEl('title', {}, '市场与策略月度超额收益的线性回归'));
    svg.append(svgEl('text', {x: left, y: 15}, '策略超额收益 y（% / 月）'));
    [-15, 0, 15].forEach(v => svg.append(
      svgEl('line', {x1: left, x2: width - right, y1: py(v), y2: py(v), stroke: '#d4ded5'}),
      svgEl('text', {x: left - 8, y: py(v) + 4, 'text-anchor': 'end'}, String(v))));
    [-6, -3, 0, 3, 6].forEach(v => svg.append(
      svgEl('line', {x1: px(v), x2: px(v), y1: top, y2: height - bottom, stroke: '#e5eee5'}),
      svgEl('text', {x: px(v), y: height - 27, 'text-anchor': 'middle'}, String(v))));
    svg.append(svgEl('text', {x: width - right, y: height - 6, 'text-anchor': 'end'}, '市场超额收益 x（% / 月）'));
    svg.append(svgEl('line', {x1: px(0), x2: px(0), y1: top, y2: height - bottom, stroke: '#9bb0a6'}));
    svg.append(svgEl('line', {x1: px(-7), x2: px(7), y1: py(a - b * 7), y2: py(a + b * 7), stroke: '#176957', 'stroke-width': 3}));
    market.forEach((x, i) => {
      svg.append(svgEl('line', {x1: px(x), x2: px(x), y1: py(a + b * x), y2: py(yValues[i]), stroke: '#a13a4c', 'stroke-width': 2, 'stroke-dasharray': '3 3'}));
      const dot = svgEl('circle', {cx: px(x), cy: py(yValues[i]), r: 4.5, fill: '#182f2b'});
      dot.append(svgEl('title', {}, `第 ${i + 1} 个月：市场 ${signed(x)}%，策略 ${signed(yValues[i])}%`));
      svg.append(dot);
    });
    host.replaceChildren(svg);
  }
  function show(index, scroll = true, updateHash = true) {
    current = Math.min(lessons.length - 1, Math.max(0, index));
    lessons.forEach((lesson, i) => { lesson.hidden = i !== current; });
    document.querySelectorAll('[data-go]').forEach(button => {
      if (Number(button.dataset.go) === current) button.setAttribute('aria-current', 'step');
      else button.removeAttribute('aria-current');
    });
    $('chapter-select').value = String(current);
    $('prev').disabled = current === 0;
    $('next').disabled = current === lessons.length - 1;
    $('lesson-position').textContent = `第 ${current + 1} / ${lessons.length} 节`;
    if (updateHash) history.replaceState(null, '', '#' + lessons[current].id);
    if (lessons[current].id === 'beta') drawBeta();
    if (scroll) $('lesson-content').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth', block: 'start'});
  }
  document.querySelectorAll('[data-go]').forEach(button => button.addEventListener('click', () => show(Number(button.dataset.go))));
  $('chapter-select').addEventListener('change', e => show(Number(e.target.value), false));
  $('prev').addEventListener('click', () => show(current - 1));
  $('next').addEventListener('click', () => show(current + 1));
  ['beta-slider', 'alpha-slider', 'noise-slider'].forEach(id => $(id).addEventListener('input', drawBeta));
  const loadHash = () => {
    const index = lessons.findIndex(lesson => '#' + lesson.id === location.hash);
    show(index < 0 ? 0 : index, false, false);
  };
  new ResizeObserver(() => { if (lessons[current].id === 'beta') drawBeta(); }).observe($('lesson-content'));
  window.addEventListener('hashchange', loadHash);
  window.addEventListener('beforeprint', () => { lessons.forEach(lesson => { lesson.hidden = false; }); drawBeta(); });
  window.addEventListener('afterprint', () => show(current, false, false));
  loadHash();
})();
