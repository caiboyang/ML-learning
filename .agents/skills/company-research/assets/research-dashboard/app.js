'use strict';
const sectionTitles = {verdict:'01 阶段与决策', assets:'02 业务与起步资产', paths:'03 对标路径与机制', choices:'04 迁移与路线', validation:'05 验证与数据合同', questions:'06 证据与问答'};
const profileColumns = ['起点资产', '第一批用户', '第一个产品', '第一种收入'];
const names = {fact:'事实记录', inference:'机制解释', recommendation:'行动建议'};
const byId = id => document.getElementById(id);
function el(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}
function link(text, id) { const a = el('a', text); a.href = `#${id}`; return a; }
function pageLink(text, query = '', hash = '') {
  const a = el('a', text); a.href = `./index.html${query}${hash}`; return a;
}
async function start() {
  const response = await fetch('research.json');
  if (!response.ok) throw new Error('研究数据未能加载，请确认同目录 research.json 可访问。');
  const data = await response.json();
  const companies = new Map(data.companies.map(c => [c.id, c]));
  const records = new Map(data.records.map(r => [r.id, r]));
  const evidence = new Map(data.evidence.map(e => [e.id, e]));
  const company = byId('company'), search = byId('search'), kind = byId('kind'), sourceSearch = byId('source-search');
  const query = new URLSearchParams(location.search);
  let caseCompany = query.get('view') === 'case' ? companies.get(query.get('company')) : null;
  if (!caseCompany?.case) caseCompany = null;
  for (const c of companies.values()) {
    const option = el('option', `${c.name} · ${c.period}`); option.value = c.id; company.append(option);
    if (c.case) byId('case-links').append(pageLink(`${c.name} 四模块专题 →`, `?view=case&company=${encodeURIComponent(c.id)}`));
  }
  company.value = companies.has(query.get('company')) ? query.get('company') : 'all';
  for (const [id, value] of Object.entries({question:data.meta.question, scope:data.meta.scope, notice:data.meta.notice, date:`更新 ${data.meta.asOf}`})) byId(id).textContent = value;
  const nav = byId('navigation');
  let sourceOnly = new Set();
  function citations(ids) {
    const box = el('div', undefined, 'sources');
    for (const id of ids) box.append(link(`${id} · ${evidence.get(id).title}`, id));
    return box;
  }
  function metadata(r) {
    const box = el('div', undefined, 'meta');
    box.append(el('span', r.companyId ? companies.get(r.companyId).name : '全局'), el('span', names[r.kind], `badge ${r.kind}`), el('span', r.status));
    if (sourceOnly.has(r.id)) box.append(el('span', '仅关联来源命中', 'badge'));
    return box;
  }
  function footer(r) {
    const box = el('div', undefined, 'record-footer');
    box.append(el('p', `边界：${r.limitation}`, 'limit'), citations(r.evidenceIds));
    if (r.relatedIds.length) {
      const related = el('div', undefined, 'related');
      for (const id of r.relatedIds) related.append(link(`关联：${records.get(id).title}`, id));
      box.append(related);
    }
    return box;
  }
  function fields(r) {
    const dl = el('dl');
    for (const field of r.fields || []) {
      if (kind.value !== 'all' && field.kind && field.kind !== kind.value) continue;
      const row = el('div', undefined, 'field');
      row.append(el('dt', field.kind ? `${field.label} · ${names[field.kind]}` : field.label), el('dd', field.value)); dl.append(row);
    }
    return dl;
  }
  function shell(r, tag = 'article') {
    const node = el(tag, undefined, `record ${r.role}`); node.id = r.id; node.tabIndex = -1;
    node.append(metadata(r), el('h3', r.title)); return node;
  }
  function metric(r) {
    const node = shell(r), value = el('div', r.metric.value, 'metric-value');
    value.append(el('span', r.metric.unit)); node.append(value, el('p', r.metric.basis), el('p', r.text)); return node;
  }
  function route(r) {
    const node = shell(r); node.dataset.priority = r.route.priority;
    node.prepend(el('p', r.route.priority, 'route-priority'));
    node.append(el('p', r.text), el('p', `进入条件：${r.route.condition}`, 'route-condition')); return node;
  }
  function step(r) {
    const node = shell(r, 'li'); node.prepend(el('p', r.stage || '阶段待确认', 'stage'));
    node.append(el('p', r.text), fields(r)); return node;
  }
  function advice(r) {
    const node = shell(r); node.append(el('p', r.text)); return node;
  }
  function meeting(r) {
    const node = shell(r); node.prepend(el('p', r.meeting.confirmationType, 'eyebrow'));
    const dl = el('dl');
    for (const [key, label] of Object.entries({decision:'决定',basis:'依据',condition:'条件',owner:'确认角色',reviewAt:'复盘时间'})) {
      const row = el('div', undefined, 'field'); row.append(el('dt', label), el('dd', r.meeting[key])); dl.append(row);
    }
    node.append(dl); return node;
  }
  function action(r) {
    const node = shell(r); node.append(el('p', r.text));
    const list = el('ol', undefined, 'milestones');
    for (const item of r.milestones) {
      const li = el('li'); li.append(el('strong', item.period), el('h4', item.action), el('p', `负责：${item.owner}`), el('p', `观察：${item.observe}`), el('p', item.decision, 'limit')); list.append(li);
    }
    node.append(list, fields(r)); return node;
  }
  function tableRegion(label, headers) {
    const wrapper = el('div', undefined, 'table-scroll'); wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region'); wrapper.setAttribute('aria-label', `${label}，可横向滚动`);
    const table = el('table'); table.append(el('caption', `${label} · 窄屏可横向滚动`));
    const head = el('tr');
    for (const label of headers) { const th = el('th', label); th.scope = 'col'; head.append(th); }
    const thead = el('thead'); thead.append(head); table.append(thead);
    const body = el('tbody'); table.append(body); wrapper.append(table); return {wrapper, body};
  }
  function comparison(r) {
    const node = shell(r); node.append(el('p', r.text));
    const labels = profileColumns;
    const {wrapper, body} = tableRegion('冷启动资产对照', ['公司', ...labels]);
    for (const id of r.comparisonIds) {
      const profile = records.get(id), row = el('tr'), th = el('th'); th.scope = 'row';
      th.append(link(companies.get(profile.companyId).name, id)); row.append(th);
      for (const label of labels) row.append(el('td', profile.fields.find(f => f.label === label)?.value || '未记录'));
      body.append(row);
    }
    node.append(wrapper); return node;
  }
  function loop(r) {
    const node = shell(r); node.append(el('p', r.text));
    const list = el('ol', undefined, 'loop');
    for (const edge of r.edges) {
      const li = el('li'); li.append(el('strong', `${edge.from} → ${edge.to}`), el('p', edge.mechanism), el('small', edge.status), citations(edge.evidenceIds)); list.append(li);
    }
    node.append(list); return node;
  }
  function prose(r) { const node = shell(r); node.append(el('p', r.text), fields(r)); return node; }
  const renderers = {metric, route, step, advice, meeting, action, comparison, loop};
  function renderRecord(r) { const node = (renderers[r.role] || prose)(r); node.append(footer(r)); return node; }
  function proofTable(items) {
    const {wrapper, body} = tableRegion('证明状态：判断与证据分开', ['命题与判断', '证据与支持边界', '缺口', '下一步']);
    for (const r of items) {
      const row = el('tr'); row.id = r.id; row.tabIndex = -1;
      const name = el('th'); name.scope = 'row'; name.append(el('strong', r.proof.proposition), el('p', r.proof.state, 'proof-state'), metadata(r));
      const support = el('td'); support.append(el('p', r.proof.evidence), footer(r));
      row.append(name, support, el('td', r.proof.gap), el('td', r.proof.next)); body.append(row);
    }
    return wrapper;
  }
  function grouped(items) {
    const container = el('div', undefined, 'section-content');
    const order = {judgment:0, metric:1, proof:2};
    const roles = [...new Set(items.map(r => r.role))].sort((a,b) => (order[a] ?? 99) - (order[b] ?? 99));
    for (const role of roles) {
      const subset = items.filter(r => r.role === role);
      if (role === 'proof') { container.append(proofTable(subset)); continue; }
      if (role === 'advice') {
        const board = el('div', undefined, 'advice-board');
        for (const status of ['立即采用','带条件采用','明确删除','待确认']) {
          const matches = subset.filter(r => r.adoption === status);
          if (!matches.length) continue;
          const lane = el('div', undefined, 'advice-lane'); lane.append(el('h3', status));
          for (const r of matches) lane.append(renderRecord(r)); board.append(lane);
        }
        container.append(board); continue;
      }
      const group = el(role === 'step' ? 'ol' : 'div', undefined, role === 'step' ? 'timeline' : `${role}-group`);
      for (const r of subset) group.append(renderRecord(r)); container.append(group);
    }
    return container;
  }
  function hero() {
    const judgment = records.get(caseCompany ? caseCompany.case.verdictId : data.meta.verdictId);
    byId('title').textContent = caseCompany ? `${caseCompany.name} · ${caseCompany.period}` : data.meta.title;
    document.title = byId('title').textContent;
    byId('question').textContent = caseCompany ? `本专题服务的决策：${data.meta.question}` : data.meta.question;
    byId('scope').textContent = caseCompany ? `${caseCompany.period}；按起点资产、交易交付、取舍与回路迁移展开。` : data.meta.scope;
    for (const a of byId('case-links').querySelectorAll('a:not(#overview-link)')) a.hidden = !!caseCompany;
    byId('summary-label').textContent = caseCompany ? '公司专题 · 四模块分析' : '研究整体判断 · 不随正文公司筛选重算';
    byId('overview-link').hidden = !caseCompany;
    byId('company-control').hidden = !!caseCompany;
    const verdict = byId('hero-verdict'); verdict.replaceChildren(); verdict.hidden = kind.value === 'fact';
    if (!verdict.hidden) verdict.append(el('p', names[judgment.kind], 'eyebrow'), el('h2', judgment.title), el('p', judgment.text), citations(judgment.evidenceIds));
    byId('hero-boundary').textContent = `判断边界：${judgment.limitation}`;
    const metrics = byId('hero-metrics'); metrics.replaceChildren(); metrics.hidden = !!caseCompany;
    if (!caseCompany) for (const id of data.meta.keyMetricIds) {
      const r = records.get(id), box = el('article', undefined, 'metric-summary');
      const value = el('p', r.metric.value, 'metric-value'); value.append(el('span', r.metric.unit));
      box.append(el('h2', r.title), value, el('p', r.metric.basis), link('口径、边界与来源 →', r.id)); metrics.append(box);
    }
  }
  for (const source of evidence.values()) {
    const article = el('article', undefined, 'evidence'); article.id = source.id; article.tabIndex = -1;
    article.append(el('h3', `${source.id} · ${source.title}`), el('p', `${source.nature} · ${source.date} · ${source.locator}`), el('p', source.support), el('p', `支持边界：${source.limitation}`, 'limit'));
    if (source.url) {
      const url = new URL(source.url); if (!['https:', 'http:'].includes(url.protocol)) throw new Error('来源链接必须使用 HTTP 或 HTTPS。');
      const a = el('a', '打开原始来源'); a.href = url.href; article.append(a);
    }
    const uses = data.records.filter(r => r.evidenceIds.includes(source.id) || r.edges?.some(edge => edge.evidenceIds.includes(source.id)));
    const backlinks = el('div', undefined, 'related');
    for (const r of uses) backlinks.append(link(`返回：${r.title}`, r.id)); article.append(backlinks); byId('evidence-list').append(article);
  }
  function recordText(r) {
    const displayedFields = (r.fields || []).filter(f => kind.value === 'all' || !f.kind || f.kind === kind.value).map(f => [f.label, f.value]);
    const comparisonFields = (r.comparisonIds || []).flatMap(id => records.get(id).fields.filter(f => profileColumns.includes(f.label)).map(f => [f.label, f.value]));
    return [r.title, ['meeting','proof'].includes(r.role) ? '' : r.text, r.status, r.stage, r.adoption, r.limitation,
      displayedFields, ...['metric','proof','route','meeting'].map(key => Object.values(r[key] || {})),
      (r.milestones || []).map(item => Object.values(item)), (r.edges || []).map(e => [e.from,e.to,e.mechanism,e.status]),
      companies.get(r.companyId)?.name, comparisonFields].flat(Infinity).filter(v => v !== undefined).join(' ').toLocaleLowerCase();
  }
  function render() {
    hero(); sourceOnly = new Set();
    const term = search.value.trim().toLocaleLowerCase();
    const modules = caseCompany ? caseCompany.case.modules : data.sections;
    const caseIds = caseCompany ? new Set(modules.flatMap(m => m.recordIds)) : null;
    const visible = data.records.filter(r => {
      if (caseIds ? !caseIds.has(r.id) : company.value !== 'all' && r.companyId && r.companyId !== company.value) return false;
      if (kind.value !== 'all' && r.kind !== kind.value) return false;
      const ownMatch = !term || recordText(r).includes(term);
      const sourceIds = [...r.evidenceIds, ...(r.edges || []).flatMap(e => e.evidenceIds)];
      const sourceMatch = sourceSearch.checked && sourceIds.some(id => JSON.stringify(evidence.get(id)).toLocaleLowerCase().includes(term));
      if (!ownMatch && sourceMatch) sourceOnly.add(r.id);
      return ownMatch || sourceMatch;
    });
    const content = byId('content'); content.replaceChildren(); nav.replaceChildren();
    for (const module of modules) {
      const subset = caseIds ? module.recordIds.map(id => records.get(id)).filter(r => visible.includes(r)) : visible.filter(r => r.section === module.id);
      const title = module.title || sectionTitles[module.id]; nav.append(link(title, module.id));
      const section = el('section'); section.id = module.id; section.tabIndex = -1;
      const heading = el('header', undefined, 'section-heading'); heading.append(el('h2', title));
      if (kind.value === 'all') heading.append(el('p', module.thesis, 'section-intro'));
      section.append(heading);
      if (!subset.length) section.append(el('p', '当前组合条件下，本节没有匹配记录。'));
      else {
        section.append(grouped(subset));
        if (kind.value === 'all') {
          const conclusion = el('div', undefined, 'section-conclusion');
          conclusion.append(el('strong', caseIds ? '专题结论' : '本研究整体结论 · 不随筛选重算'), el('p', module.conclusion));
          if (module.evidenceIds) conclusion.append(citations(module.evidenceIds)); section.append(conclusion);
        }
      }
      content.append(section);
    }
    if (caseCompany) {
      const next = el('div', undefined, 'action-return'); next.append(el('strong','把借鉴条件接回下一步验证'), pageLink('返回验证与数据合同 →','','#validation')); content.append(next);
    }
    nav.append(link('证据明细','sources'));
    const scope = caseCompany ? `${caseCompany.name} 四模块专题` : `${company.value === 'all' ? '全部公司' : companies.get(company.value).name}＋全局记录`;
    byId('results').textContent = `范围：${scope}；${kind.value === 'all' ? '全部性质' : names[kind.value]}；搜索：${term || '无'}（${sourceSearch.checked ? '含关联来源' : '正文与公司名'}）。匹配 ${visible.length} / ${data.records.length} 条记录（非经营统计），其中仅来源命中 ${sourceOnly.size} 条。首屏指标为目标业务整体数据；证据明细保持完整。`;
    byId('empty').hidden = visible.length > 0; syncLayout(); updateActiveSection();
  }
  const narrow = window.matchMedia('(max-width:1000px)');
  function syncLayout() {
    const offset = narrow.matches ? 20 : 60 + byId('filters').offsetHeight + 24;
    document.documentElement.style.setProperty('--anchor-offset', `${offset}px`);
  }
  function updateActiveSection() {
    const line = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--anchor-offset')) + 2;
    const sections = [...document.querySelectorAll('main section')]; let active = sections[0];
    for (const section of sections) if (section.getBoundingClientRect().top <= line) active = section;
    for (const a of nav.querySelectorAll('a')) {
      if (a.hash === `#${active.id}`) a.setAttribute('aria-current','location'); else a.removeAttribute('aria-current');
    }
  }
  function revealHash() {
    let id; try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const record = records.get(id);
    if (record && !byId(id)) {
      if (caseCompany && !caseCompany.case.modules.some(m => m.recordIds.includes(id))) {
        caseCompany = null;
        const url = new URL(location.href); url.searchParams.delete('view'); url.searchParams.delete('company'); history.replaceState(null,'',url);
      }
      company.value = record.companyId || 'all'; search.value = ''; kind.value = 'all'; render();
    }
    const target = byId(id); if (target) { target.scrollIntoView({block:'start'}); target.focus({preventScroll:true}); }
  }
  byId('filters').addEventListener('submit', e => e.preventDefault());
  byId('filters').addEventListener('input', render);
  byId('filters').addEventListener('change', render);
  byId('filters').addEventListener('reset', e => { e.preventDefault(); company.value = caseCompany?.id || 'all'; kind.value = 'all'; search.value = ''; sourceSearch.checked = false; render(); });
  window.addEventListener('hashchange',revealHash);
  window.addEventListener('scroll',updateActiveSection,{passive:true}); window.addEventListener('resize',() => { syncLayout(); updateActiveSection(); });
  document.addEventListener('click', e => { const a = e.target.closest('a[href^="#"]'); if (a && a.hash === location.hash) { e.preventDefault(); revealHash(); } });
  function syncDirectory() { byId('directory').open = !narrow.matches; }
  narrow.addEventListener('change',syncDirectory); syncDirectory(); render(); revealHash();
}
start().catch(error => { byId('notice').textContent = `页面未完成加载：${error.message} 请按 dashboard-data.md 启动静态服务并校验 JSON 与引用。`; byId('notice').setAttribute('role','alert'); });
