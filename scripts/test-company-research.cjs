// Run with Node and AJV 8: node scripts/test-company-research.cjs [path-to-ajv] [extra-data.json]
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Ajv = require(process.argv[2] || 'ajv');
const root = path.resolve(__dirname, '..');
const assets = path.join(root, '.agents/skills/company-research/assets/research-dashboard');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const data = read(path.join(assets, 'research.json'));
const validate = new Ajv({allErrors:true}).compile(read(path.join(assets, 'research.schema.json')));
const copy = value => JSON.parse(JSON.stringify(value));

function checkReferences(d) {
  assert(validate(d), JSON.stringify(validate.errors));
  const records = new Map(d.records.map(r => [r.id,r]));
  const companies = new Set(d.companies.map(c => c.id));
  const sources = new Set(d.evidence.map(e => e.id));
  const views = [...d.topics, ...d.companies.filter(c => c.case).map(c => c.case)];
  const ids = [...d.records, ...d.companies, ...d.evidence, ...d.sections, ...d.topics, ...views.flatMap(v => v.modules)].map(item => item.id).filter(Boolean);
  assert.equal(new Set(ids).size, ids.length, 'Duplicate data IDs');
  const fixedIds = [...fs.readFileSync(path.join(assets,'index.html'),'utf8').matchAll(/\bid="([^"]+)"/g)].map(m => m[1]);
  assert(!ids.some(id => fixedIds.includes(id)), 'Reserved DOM ID');
  const sections = ['verdict','assets','paths',...(d.meta.taskType === 'external-company' ? ['decisions'] : []),'choices','validation','questions'];
  assert.deepEqual(d.sections.map(s => s.id), sections);
  const checkSources = ids => ids.forEach(id => assert(sources.has(id), `Missing source ${id}`));
  assert.equal(records.get(d.meta.verdictId)?.role,'judgment');
  d.meta.keyMetricIds.forEach(id => assert.equal(records.get(id)?.role,'metric'));
  d.sections.forEach(s => checkSources(s.evidenceIds));
  for (const r of d.records) {
    assert(!r.companyId || companies.has(r.companyId));
    assert(sections.includes(r.section));
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
    assert.equal(records.get(view.verdictId)?.role,'judgment');
    const used = view.modules.flatMap(m => m.recordIds);
    assert.equal(new Set(used).size,used.length,'A record occurs twice in one view');
    used.forEach(id => assert(records.has(id), `Missing view record ${id}`));
  }
}
checkReferences(data);
if (process.argv[3]) checkReferences(read(process.argv[3]));

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
console.log('Schema regressions, N/A, custom/default columns, references and view integrity passed.');
