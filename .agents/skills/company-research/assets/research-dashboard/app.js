'use strict';
const sections = [
  ['verdict', '01 阶段与决策', '先区分已证明、有信号和未证明，说明当前判断的边界。'],
  ['assets', '02 业务与起步资产', '把产品、渠道、资源与责任连到可调用的启动资产。'],
  ['paths', '03 对标路径与机制', '按实际动作标阶段；事实、机制判断与未验证的反馈分开。'],
  ['choices', '04 迁移与路线', '学动作顺序，区分现在、以后、谨慎和暂不迁移，并检查决策门槛。'],
  ['validation', '05 验证与数据合同', '明确试验、记录口径、负责角色、观察窗口与复盘条件。'],
  ['questions', '06 证据与问答', '把新回答接回阶段、路线和动作；完整来源见下方证据明细。'],
];
const names = {fact:'事实记录', inference:'机制解释', recommendation:'行动建议'};
const byId = id => document.getElementById(id);
function el(tag, text, className) {
  const element = document.createElement(tag);
  if (text !== undefined) element.textContent = text;
  if (className) element.className = className;
  return element;
}
function link(text, id) {
  const a = el('a', text); a.href = `#${id}`; return a;
}
async function start() {
  const response = await fetch('research.json');
  if (!response.ok) throw new Error('研究数据未能加载，请确认同目录 research.json 可访问。');
  const data = await response.json();
  const companies = new Map(data.companies.map(c => [c.id, c]));
  const records = new Map(data.records.map(r => [r.id, r]));
  const evidence = new Map(data.evidence.map(e => [e.id, e]));
  const company = byId('company'), search = byId('search'), kind = byId('kind');
  document.title = data.meta.title;
  for (const [id, value] of Object.entries({title:data.meta.title, question:data.meta.question, scope:data.meta.scope, notice:data.meta.notice, date:`更新 ${data.meta.asOf}`})) byId(id).textContent = value;
  for (const c of companies.values()) {
    const option = el('option', `${c.name} · ${c.period}`); option.value = c.id; company.append(option);
  }
  const nav = byId('navigation');
  for (const [id, title] of sections) nav.append(link(title, id));
  nav.append(link('证据明细', 'sources'));
  function citations(ids) {
    const box = el('div', undefined, 'sources');
    for (const id of ids) box.append(link(`${id} · ${evidence.get(id).title}`, id));
    return box;
  }
  function card(r) {
    const article = el('article', undefined, `record ${r.role === 'step' ? 'step' : ''} ${(r.fields && r.role !== 'step') || r.edges || r.comparisonIds ? 'wide' : ''}`);
    article.id = r.id; article.tabIndex = -1;
    const meta = el('div', undefined, 'meta');
    meta.append(el('span', r.companyId ? companies.get(r.companyId).name : '全局 · 不随公司筛选隐藏'));
    meta.append(el('span', names[r.kind], `badge ${r.kind}`), el('span', r.status));
    if (r.stage) meta.append(el('span', r.stage));
    article.append(meta, el('h3', r.title));
    if (r.metric) {
      const value = el('div', r.metric.value, 'metric'); value.append(el('span', r.metric.unit));
      article.append(value, el('p', r.metric.basis));
    }
    article.append(el('p', r.text));
    if (r.fields) {
      const dl = el('dl');
      for (const field of r.fields) {
        if (kind.value !== 'all' && field.kind && field.kind !== kind.value) continue;
        const row = el('div', undefined, 'field'); row.append(el('dt', field.kind ? `${field.label} · ${names[field.kind]}` : field.label), el('dd', field.value)); dl.append(row);
      }
      article.append(dl);
    }
    if (r.comparisonIds) {
      const wrapper = el('div', undefined, 'table-scroll'); wrapper.tabIndex = 0;
      wrapper.setAttribute('role', 'region'); wrapper.setAttribute('aria-label', '起点资产对照表，可横向滚动');
      const table = el('table'); table.append(el('caption', '同字段对照 · 窄屏可横向滚动'));
      const labels = ['起点资产', '第一批用户', '第一个产品', '第一种收入'];
      const header = el('tr');
      for (const label of ['公司', ...labels]) { const th = el('th', label); th.scope = 'col'; header.append(th); }
      const thead = el('thead'); thead.append(header); table.append(thead);
      const tbody = el('tbody');
      for (const id of r.comparisonIds) {
        const profile = records.get(id), row = el('tr'), th = el('th'); th.scope = 'row';
        th.append(link(companies.get(profile.companyId).name, id)); row.append(th);
        for (const label of labels) row.append(el('td', profile.fields.find(f => f.label === label)?.value || '未记录'));
        tbody.append(row);
      }
      table.append(tbody); wrapper.append(table); article.append(wrapper);
    }
    if (r.edges) {
      const list = el('ol', undefined, 'loop');
      for (const edge of r.edges) {
        const item = el('li'); item.append(el('strong', `${edge.from} → ${edge.to}`), el('p', edge.mechanism), el('small', edge.status), citations(edge.evidenceIds)); list.append(item);
      }
      article.append(list);
    }
    article.append(el('p', `边界：${r.limitation}`, 'limit'), citations(r.evidenceIds));
    if (r.relatedIds.length) {
      const related = el('div', undefined, 'related');
      for (const id of r.relatedIds) related.append(link(`关联：${records.get(id).title}`, id));
      article.append(related);
    }
    return article;
  }
  // Source details stay visible even in facts-only mode, including their limitations.
  for (const source of evidence.values()) {
    const article = el('article', undefined, 'evidence'); article.id = source.id; article.tabIndex = -1;
    article.append(el('h3', `${source.id} · ${source.title}`), el('p', `${source.nature} · ${source.date} · ${source.locator}`), el('p', source.support), el('p', `支持边界：${source.limitation}`, 'limit'));
    if (source.url) {
      const url = new URL(source.url);
      if (!['https:', 'http:'].includes(url.protocol)) throw new Error('来源链接必须使用 HTTP 或 HTTPS。');
      const a = el('a', '打开原始来源'); a.href = url.href; article.append(a);
    }
    const uses = data.records.filter(r => r.evidenceIds.includes(source.id) || r.edges?.some(edge => edge.evidenceIds.includes(source.id)));
    const backlinks = el('div', undefined, 'related');
    for (const r of uses) backlinks.append(link(`返回：${r.title}`, r.id));
    article.append(backlinks); byId('evidence-list').append(article);
  }
  function render() {
    const term = search.value.trim().toLocaleLowerCase();
    const visible = data.records.filter(r => {
      const sourceIds = [...r.evidenceIds, ...(r.edges || []).flatMap(edge => edge.evidenceIds)];
      const haystack = JSON.stringify([r, ...(r.comparisonIds || []).map(id => records.get(id)), companies.get(r.companyId)?.name, ...sourceIds.map(id => evidence.get(id))]).toLocaleLowerCase();
      return (company.value === 'all' || !r.companyId || r.companyId === company.value) && (kind.value === 'all' || r.kind === kind.value) && (!term || haystack.includes(term));
    });
    const content = byId('content'); content.replaceChildren();
    for (const [id, title, intro] of sections) {
      const subset = visible.filter(r => r.section === id);
      const section = el('section'); section.id = id; section.tabIndex = -1;
      section.append(el('h2', title), el('p', intro, 'section-intro'));
      if (!subset.length) section.append(el('p', '当前组合条件下，本节没有匹配记录。'));
      const grid = el('div', undefined, 'grid'); for (const r of subset) grid.append(card(r));
      section.append(grid); content.append(section);
    }
    const companyName = company.value === 'all' ? '全部公司' : companies.get(company.value).name;
    byId('results').textContent = `范围：${companyName}＋全局记录；${kind.value === 'all' ? '全部性质' : names[kind.value]}；搜索：${term || '无'}。匹配 ${visible.length} / ${data.records.length} 条记录（非经营统计）。证据明细保持完整。`;
    byId('empty').hidden = visible.length > 0;
    updateActiveSection();
  }
  function updateActiveSection() {
    const readingLine = window.matchMedia('(max-width:1000px)').matches ? 30 : byId('filters').getBoundingClientRect().bottom + 40;
    const candidates = [...document.querySelectorAll('main section')];
    let active = candidates[0];
    for (const section of candidates) {
      if (section.getBoundingClientRect().top <= readingLine) active = section;
    }
    for (const a of nav.querySelectorAll('a')) {
      if (a.hash === `#${active.id}`) a.setAttribute('aria-current', 'location');
      else a.removeAttribute('aria-current');
    }
  }

  function revealHash() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const record = records.get(id);
    if (record && !byId(id)) {
      company.value = record.companyId || 'all'; search.value = ''; kind.value = 'all'; render();
    }
    const target = byId(id);
    if (target) { target.scrollIntoView({block:'start'}); target.focus({preventScroll:true}); }
  }
  byId('filters').addEventListener('submit', event => event.preventDefault());
  byId('filters').addEventListener('input', render);
  byId('filters').addEventListener('change', render);
  byId('filters').addEventListener('reset', event => {
    event.preventDefault(); company.value = 'all'; kind.value = 'all'; search.value = ''; render();
  });
  window.addEventListener('hashchange', revealHash);
  window.addEventListener('scroll', updateActiveSection, {passive:true});
  window.addEventListener('resize', updateActiveSection);
  // A repeated click on the same hash must also reveal a filtered-out record.
  document.addEventListener('click', event => {
    const a = event.target.closest('a[href^="#"]');
    if (a && a.hash === location.hash) { event.preventDefault(); revealHash(); }
  });
  if (window.matchMedia('(max-width:1000px)').matches) byId('directory').open = false;
  render(); revealHash();
}
start().catch(error => {
  byId('notice').textContent = `页面未完成加载：${error.message} 请按 dashboard-data.md 启动本地静态服务，并先校验 JSON 与引用。`;
  byId('notice').setAttribute('role', 'alert');
});
