#!/usr/bin/env node
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const Ajv = require('ajv');
const addFormats = require('ajv-formats');
const assets = path.resolve(__dirname, '../assets/research-dashboard');
const schema = JSON.parse(fs.readFileSync(path.join(assets,'research.schema.json'),'utf8'));
const validate = addFormats(new Ajv({allErrors:true})).compile(schema);
const coverageItems = schema.properties.coverage.items.properties.item.enum;

// Editorial warning only: identical boundaries may be legitimate, but need review.
function limitationWarnings(records) {
  const groups = new Map();
  for (const r of records) {
    const text = r.limitation.trim().replace(/\s+/g,' ');
    if (!text) continue;
    if (!groups.has(text)) groups.set(text,[]);
    groups.get(text).push(r.id);
  }
  return [...groups].filter(([,ids]) => ids.length >= 5).map(([text,recordIds]) => ({
    code:'repeated-limitation', text, recordIds
  }));
}

function validateReport(d) {
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
  return limitationWarnings(d.records);
}

module.exports = {validateReport, validate, limitationWarnings};
if (require.main === module) {
  if (process.argv.length !== 3) {
    console.error('Usage: node scripts/validate-report.cjs /path/to/research.json');
    process.exitCode = 2;
  } else {
    try {
      const warnings = validateReport(JSON.parse(fs.readFileSync(process.argv[2],'utf8')));
      for (const w of warnings) console.warn(`WARNING ${w.code} (${w.recordIds.length} records): ${w.text}\n  IDs: ${w.recordIds.join(', ')}`);
      console.log('PASS: schema, IDs, references, main deliverables, coverage and case structure. Review evidence quality and warnings separately.');
    } catch (error) {
      console.error(`FAIL: ${error.message}`);
      process.exitCode = 1;
    }
  }
}
