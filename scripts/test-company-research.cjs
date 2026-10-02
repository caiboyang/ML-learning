// Install pinned development dependencies: npm ci --prefix scripts
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const root = path.resolve(__dirname, '..');
const assets = path.join(root, '.agents/skills/company-research/assets/research-dashboard');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const data = read(path.join(assets, 'research.json'));
const schema = read(path.join(assets, 'research.schema.json'));
const validate = addFormats(new Ajv({allErrors:true})).compile(schema);
const copy = value => JSON.parse(JSON.stringify(value));
const coverageItems = schema.properties.coverage.items.properties.item.enum;
const contract = fs.readFileSync(path.join(root,'.agents/skills/company-research/references/research-contract.md'),'utf8');
const contractItems = [...contract.split('## 内容覆盖清单：交付时逐项填写')[1].matchAll(/^\| ([^|]+) \|/gm)].map(m => m[1]).filter(item => !['检查对象','---'].includes(item));
assert.deepEqual(coverageItems,contractItems,'Schema coverage must match every contract row');

function checkReferences(d) {
  assert(validate(d), JSON.stringify(validate.errors));
  const records = new Map(d.records.map(r => [r.id,r]));
  assert.equal(new Set(d.coverage.map(c => c.item)).size,coverageItems.length,'Duplicate or missing coverage item');
  for (const c of d.coverage) {
    c.recordIds.forEach(id => assert(records.has(id),`Missing coverage record ${id}`));
    if (c.status === '有实质依据' && c.item !== '可交付性') assert(c.recordIds.length,'Substantiated coverage needs records');
  }
  const companies = new Set(d.companies.map(c => c.id));
  const sources = new Set(d.evidence.map(e => e.id));
  const views = [...d.topics, ...d.companies.filter(c => c.case).map(c => c.case)];
  const ids = [...d.records, ...d.companies, ...d.evidence, ...d.sections, ...d.topics, ...views.flatMap(v => v.modules)].map(item => item.id).filter(Boolean);
  assert.equal(new Set(ids).size, ids.length, 'Duplicate data IDs');
  const fixedIds = [...fs.readFileSync(path.join(assets,'index.html'),'utf8').matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
  assert(!ids.some(id => fixedIds.includes(id)), 'Reserved DOM ID');
  const sections = new Map(d.sections.map(s => [s.id,s]));
  assert(companies.has(d.meta.subjectCompanyId), 'Missing subject company');
  assert.equal(sections.get(d.meta.actionSectionId)?.part,'validation','Action link must lead to investigation/validation');
  const parts = new Set(d.sections.map(s => s.part));
  for (const part of ['verdict','assets','paths','choices','validation',...(d.meta.taskType === 'external-company' ? ['decisions'] : [])]) assert(parts.has(part), `Missing research coverage ${part}`);
  const checkSources = ids => ids.forEach(id => assert(sources.has(id), `Missing source ${id}`));
  assert.equal(records.get(d.meta.verdictId)?.role,'judgment');
  d.meta.keyMetricIds.forEach(id => assert.equal(records.get(id)?.role,'metric'));
  const reachable = new Set();
  d.sections.forEach(s => {
    checkSources(s.evidenceIds);
    s.overviewIds.forEach(id => {
      assert.equal(records.get(id)?.section,s.id,'Overview record belongs to another section');
      assert(!reachable.has(id),'Duplicate overview record'); reachable.add(id);
    });
  });
  // Reachability through a detail page is insufficient for a main deliverable.
  const mainRoles = new Set(['proof','step','decision','loop','advice','route','action','contract','transfer']);
  for (const r of d.records) {
    const subject = r.companyId === null || r.companyId === d.meta.subjectCompanyId;
    const sectionCompanies = new Set(d.records.filter(item => item.section === r.section && item.companyId).map(item => item.companyId));
    const standaloneCaseStep = r.role === 'step' && sectionCompanies.size === 1;
    if (r.role === 'comparison' || (subject && mainRoles.has(r.role)) || standaloneCaseStep) {
      assert(reachable.has(r.id), `Main deliverable hidden in detail: ${r.id}`);
    }
  }
  for (const c of d.companies.filter(c => c.case)) {
    assert.equal(c.case.modules.length,4,'A company case needs four analysis modules');
    for (const id of c.case.modules.flatMap(m => m.recordIds)) {
      if (records.get(id)?.role === 'step') assert(reachable.has(id),`Main deliverable hidden in detail: ${id}`);
    }
  }
  const hasTransfer = d.records.some(r => r.role === 'transfer');
  const hasBenchmarkCase = d.companies.some(c => c.id !== d.meta.subjectCompanyId && c.case);
  if (hasTransfer && !hasBenchmarkCase) assert.equal(d.coverage.find(c => c.item === '重点案例').status,'关键缺口','Missing benchmark case must be declared as a critical gap');
  for (const r of d.records) {
    assert(!r.companyId || companies.has(r.companyId));
    assert(sections.has(r.section), `Missing parent section for ${r.id}`);
    r.relatedIds.forEach(id => assert(records.has(id), `Missing record ${id}`));
    checkSources(r.evidenceIds);
    for (const items of [r.edges, r.people, r.series?.points, r.funnel?.nodes]) (items || []).forEach(item => checkSources(item.evidenceIds));
    for (const id of r.comparisonIds || []) {
      assert.equal(records.get(id)?.role,'profile');
      const labels = records.get(id).fields.map(f => f.label);
      assert.equal(new Set(labels).size, labels.length);
      (r.columns || ['起点资产','第一批用户','第一个产品','第一种收入']).forEach(label => assert(labels.includes(label)));
    }
    if (r.funnel) {
      const nodes = new Map(r.funnel.nodes.map(n => [n.id,n]));
      assert.equal(nodes.size,r.funnel.nodes.length);
      for (const node of nodes.values()) {
        assert(node.count === null || node.denominator === null || node.count <= node.denominator);
        const seen = new Set([node.id]); let parent = node.parentId;
        while (parent) { assert(nodes.has(parent) && !seen.has(parent), 'Missing or cyclic funnel parent'); seen.add(parent); parent = nodes.get(parent).parentId; }
      }
    }
  }
  for (const view of views) {
    assert(sections.has(view.parentSectionId),'Missing detail parent');
    assert.equal(records.get(view.verdictId)?.role,'judgment');
    const used = view.modules.flatMap(m => m.recordIds);
    assert.equal(new Set(used).size,used.length,'A record occurs twice in one view');
    used.forEach(id => { assert(records.has(id), `Missing view record ${id}`); reachable.add(id); });
  }
  d.records.forEach(r => assert(reachable.has(r.id), `No overview or detail route to ${r.id}`));
}
checkReferences(data);
const external = read(path.join(assets, 'external-research.json'));
checkReferences(external);
if (process.argv[2]) checkReferences(read(process.argv[2]));

for (const mutate of [
  d => { delete d.coverage; },
  d => { d.coverage.pop(); },
  d => { d.coverage[1].item = d.coverage[0].item; },
  d => { d.coverage[0].recordIds = ['absent']; },
  d => { d.coverage[0].gap = '   '; },
  d => { d.coverage.find(c => c.status === '不适用').gap = ''; },
  d => { d.coverage[0].status = '有实质依据'; d.coverage[0].recordIds = []; },
  d => { d.companies.forEach(c => delete c.case); d.coverage.find(c => c.item === '重点案例').status = '有实质依据'; }
]) {
  const broken = copy(data); mutate(broken); assert.throws(() => checkReferences(broken));
}
const fallback = copy(data), alternative = fallback.records.find(r => r.route?.priority === '备选');
assert(alternative,'Missing conditional fallback fixture');
alternative.route.condition = ''; assert(!validate(fallback),'Fallback without switching condition passed');

// Exercise the same field-kind rule used by rendering and comparison search.
const appPrelude = fs.readFileSync(path.join(assets,'app.js'),'utf8').split('async function start()')[0];
const fieldVisible = vm.runInNewContext(appPrelude + '\nfieldVisible;');
assert.equal(fieldVisible({value:'fact'},'fact','inference'),false);
assert.equal(fieldVisible({value:'fact'},'fact','fact'),true);
assert.equal(fieldVisible({kind:'inference'},'fact','inference'),true);
assert.equal(fieldVisible({kind:'inference'},'fact','fact'),false);
assert.equal(fieldVisible({kind:'recommendation'},'fact','all'),true);

// Reproduce the renderer crash: every required payload must fail schema validation if absent.
const payloads = {metric:'metric',loop:'edges',comparison:'comparisonIds',profile:'fields',proof:'proof',meeting:'meeting',route:'route',advice:'adoption',action:'milestones',team:'people',decision:'decision',series:'series',funnel:'funnel',change:'change'};
for (const [role,key] of Object.entries(payloads)) {
  const broken = copy(data), record = broken.records.find(r => r.role === role);
  assert(record, `No regression fixture for ${role}`); delete record[key];
  assert(!validate(broken), `${role} without ${key} passed`);
  assert(validate.errors.some(e => e.keyword === 'required' && e.params.missingProperty === key));
}
const noReason = copy(data);
delete noReason.records.find(r => r.proof?.state === '不适用').proof.naReason;
assert(!validate(noReason),'N/A without explanation passed');
const badColumns = copy(data);
badColumns.records.find(r => r.role === 'comparison').columns = [3];
assert(!validate(badColumns),'Non-text comparison column passed');
const defaultColumns = copy(data);
delete defaultColumns.records.find(r => r.role === 'comparison').columns;
checkReferences(defaultColumns);
for (const url of ['https://', 'https:///path', 'javascript:alert(1)', 'https://bad host/a']) {
  const broken = copy(data); broken.evidence[0].url = url;
  assert(!validate(broken), `Invalid source URL passed: ${url}`);
}
for (const url of [null, 'https://example.com/path?q=1#x', 'http://localhost:8765/']) {
  const valid = copy(data); valid.evidence[0].url = url; checkReferences(valid);
}
const noMissingReason = copy(data);
delete noMissingReason.records.find(r => r.series).series.points.find(p => p.value === null).missingReason;
assert(!validate(noMissingReason),'Missing time series reason passed');
for (const mutate of [d => { delete d.sections[0].title; }, d => { delete d.sections[0].part; }, d => { d.sections[0].overviewIds = []; }, d => { d.topics[0].id = 'case'; }, d => { d.topics[0].modules = d.topics[0].modules.slice(0,2); }]) {
  const broken = copy(data); mutate(broken); assert(!validate(broken),'Invalid section or detail structure passed');
}
// A nonempty main section must still contain every item, even if detail remains reachable.
for (const [fixture, ids] of [[data, ['p-payment','adopt-scope','c-route-standard','d-contract','c-matrix']], [external, ['x-first','x-open-decision','x-loop','x-investigation']]]) {
  for (const id of ids) {
    const broken = copy(fixture), record = broken.records.find(r => r.id === id);
    const section = broken.sections.find(s => s.id === record.section);
    section.overviewIds = section.overviewIds.filter(item => item !== id);
    if (!section.overviewIds.length) {
      broken.records.push({...copy(broken.records.find(r => r.role === 'judgment')), id:'test-summary', section:section.id});
      section.overviewIds.push('test-summary');
    }
    if (!broken.topics.some(t => t.modules.some(m => m.recordIds.includes(id)))) broken.topics[0].modules[0].recordIds.push(id);
    assert.throws(() => checkReferences(broken), /Main deliverable hidden in detail/);
  }
}
const standaloneCase = copy(data);
checkReferences(standaloneCase);
standaloneCase.sections.find(s => s.id === 'featured-benchmark').overviewIds = standaloneCase.sections.find(s => s.id === 'featured-benchmark').overviewIds.filter(id => id !== 's-three');
assert.throws(() => checkReferences(standaloneCase), /Main deliverable hidden in detail: s-three/);
const renamed = copy(data), oldId = renamed.sections[0].id;
renamed.sections[0].id = 'another-deliverable';
renamed.records.filter(r => r.section === oldId).forEach(r => { r.section = 'another-deliverable'; });
renamed.topics.filter(t => t.parentSectionId === oldId).forEach(t => { t.parentSectionId = 'another-deliverable'; });
checkReferences(renamed);
for (const mutate of [d => { d.sections[0].overviewIds = ['absent']; }, d => { d.topics[0].parentSectionId = 'absent'; }, d => { d.records[0].section = 'absent'; }]) {
  const broken = copy(data); mutate(broken); assert.throws(() => checkReferences(broken));
}
console.log('Both examples: schema, main-deliverable coverage, URL/missing-data regressions, arbitrary sections, reachability and references passed.');
