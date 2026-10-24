// Install validator dependencies: npm ci --prefix .agents/skills/company-research/scripts --ignore-scripts
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const os = require('node:os');
const {spawnSync} = require('node:child_process');
const root = path.resolve(__dirname, '..');
const assets = path.join(root, '.agents/skills/company-research/assets/research-dashboard');
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const data = read(path.join(assets, 'research.json'));
const schema = read(path.join(assets, 'research.schema.json'));
const {validateReport:checkReferences, validate, limitationWarnings} = require(path.join(assets,'../../scripts/validate-report.cjs'));
const copy = value => JSON.parse(JSON.stringify(value));
const coverageItems = schema.properties.coverage.items.properties.item.enum;
const contract = fs.readFileSync(path.join(root,'.agents/skills/company-research/references/research-contract.md'),'utf8');
const contractItems = [...contract.split('## 内容覆盖清单：交付时逐项填写')[1].matchAll(/^\| ([^|]+) \|/gm)].map(m => m[1]).filter(item => !['检查对象','---'].includes(item));
assert.deepEqual(coverageItems,contractItems,'Schema coverage must match every contract row');


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

// Mixed-kind records and comparison cells must survive the outer record filter.
const recordMatchesKind = vm.runInNewContext(appPrelude + '\nrecordMatchesKind;');
const selectedFields = vm.runInNewContext(appPrelude + '\nselectedFields;');
for (const [fixture, ids, kind] of [[data,['s-one','s-two'],'inference'], [external,['roomguild-tradeoff'],'recommendation']]) {
  const records = new Map(fixture.records.map(r => [r.id,r]));
  for (const id of ids) {
    const record = records.get(id);
    assert.notEqual(record.kind,kind);
    assert(recordMatchesKind(record,kind,records),`${id} lost matching child fields`);
    assert(selectedFields(record,kind).every(f => (f.kind || record.kind) === kind));
  }
}
const profiles = new Map([['profile',{role:'profile',kind:'fact',fields:[
  {label:'起点资产',value:'asset'}, {label:'启示',kind:'recommendation',value:'next step'}
]}]]);
const matrix = {role:'comparison',kind:'inference',comparisonIds:['profile'],columns:['起点资产','启示']};
assert(recordMatchesKind(matrix,'fact',profiles));
assert(recordMatchesKind(matrix,'recommendation',profiles));
assert(!recordMatchesKind({...matrix,columns:['起点资产']},'recommendation',profiles),'Hidden columns must not match');
assert(!recordMatchesKind({role:'metric',kind:'fact',fields:[{kind:'inference'}]},'inference',profiles),'Renderer-ignored fields must not match');
assert(!recordMatchesKind({role:'asset',kind:'fact'},'inference',profiles));

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
// The warning is advisory and includes every affected record; whitespace is immaterial.
const repeated = Array.from({length:5}, (_,i) => ({id:`r-${i}`,limitation:i % 2 ? 'same  boundary' : ' same boundary '}));
assert.deepEqual(limitationWarnings(repeated.slice(0,4)),[]);
assert.deepEqual(limitationWarnings(repeated),[{code:'repeated-limitation',text:'same boundary',recordIds:repeated.map(r => r.id)}]);
assert.deepEqual(limitationWarnings(repeated.map((r,i) => ({...r,limitation:`boundary ${i}`}))),[]);

// Copy only the skill plus its installed dependencies: no repository tests or fixtures needed.
const isolated = fs.mkdtempSync(path.join(os.tmpdir(),'company-research-validator-'));
try {
  const skill = path.join(isolated,'skill');
  fs.cpSync(path.resolve(assets,'../..'),skill,{recursive:true});
  for (const name of ['research.json','external-research.json']) fs.unlinkSync(path.join(skill,'assets/research-dashboard',name));
  const input = path.join(isolated,'report.json');
  const cli = path.join(skill,'scripts/validate-report.cjs');
  const run = args => spawnSync(process.execPath,[cli,...args],{cwd:isolated,encoding:'utf8'});
  for (const fixture of [data,external]) {
    fs.writeFileSync(input,JSON.stringify(fixture));
    const result = run([input]);
    assert.equal(result.status,0,result.stderr);
    assert(result.stdout.includes('PASS:'));
    assert(result.stderr.includes('WARNING repeated-limitation'));
  }
  const broken = copy(data); broken.records[0].relatedIds.push('missing-record');
  fs.writeFileSync(input,JSON.stringify(broken));
  const invalid = run([input]); assert.equal(invalid.status,1); assert.match(invalid.stderr,/Missing record missing-record/);
  fs.writeFileSync(input,'{'); assert.equal(run([input]).status,1);
  fs.writeFileSync(input,'{}'); assert.equal(run([input]).status,1);
  assert.equal(run([path.join(isolated,'absent.json')]).status,1);
  assert.equal(run([]).status,2);
} finally {
  fs.rmSync(isolated,{recursive:true,force:true});
}
console.log('Both examples: schema, semantics, regression cases, portable CLI and advisory warnings passed.');
