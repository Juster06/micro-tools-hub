import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const read = file => fs.readFileSync(path.join(root, file), 'utf8');
const exists = file => fs.existsSync(path.join(root, file));
const implemented = new Set(['IMPLEMENTED', 'TESTED', 'RELEASED']);
const backlog = new Set(['IDEA', 'PLANNED', 'READY', 'BLOCKED']);
export const normalizedHash = text => crypto.createHash('sha256').update(text.replace(/\r\n/g, '\n').trimEnd()).digest('hex');

export function summarize(registry) {
  const byStatus = Object.fromEntries(Object.keys(registry.status_definitions).map(s => [s, registry.tools.filter(t => t.status === s).length]));
  return { total:registry.tools.length, released:byStatus.RELEASED, implemented_unverified:byStatus.IMPLEMENTED, tested_unpublished:byStatus.TESTED, in_progress:byStatus.IN_PROGRESS, planned:registry.tools.filter(t => backlog.has(t.status)).length, blocked:byStatus.BLOCKED, ready:byStatus.READY, by_status:byStatus };
}

export function validateRegistry(r) {
  const errors = [];
  const require = (ok, message) => { if (!ok) errors.push(message); };
  if (!r || !Array.isArray(r.tools) || !Array.isArray(r.categories) || !Array.isArray(r.proposal_resolutions) || !r.status_definitions || !r.project?.website) return ['Missing registry root fields'];
  const statuses = ['IDEA','PLANNED','READY','IN_PROGRESS','BLOCKED','IMPLEMENTED','TESTED','RELEASED','DEPRECATED'];
  const date = value => typeof value === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(value) && Number.isFinite(Date.parse(value)) && new Date(value).toISOString().slice(0,10) === value;
  require(r.schema_version === 1, 'Unsupported schema_version');
  require(date(r.updated_on), 'Invalid updated_on');
  require(JSON.stringify(Object.keys(r.status_definitions).sort()) === JSON.stringify([...statuses].sort()), 'Status definitions must contain exactly the supported statuses');
  const categories = new Set(r.categories.map(c => c.id));
  require(categories.size === r.categories.length, 'Duplicate category');
  const ids = new Set(), names = new Set(), dirs = new Set(), ranks = new Set();
  const required = ['id','name','category','description','directory_path','status','priority','implementation_complexity','dependencies','required_features','testing_status','last_verification_date','notes','sequence_rank','related_tools','verification'];
  for (const t of r.tools) {
    for (const key of required) require(Object.hasOwn(t,key), `${t.id}: missing ${key}`);
    if (required.some(key=>!Object.hasOwn(t,key))) continue;
    require(typeof t.id === 'string' && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(t.id), `${t.id}: invalid id`);
    require(!ids.has(t.id), `${t.id}: duplicate id`); ids.add(t.id);
    const name = String(t.name).normalize('NFKC').toLowerCase().trim();
    require(!names.has(name), `${t.id}: duplicate name`); names.add(name);
    require(typeof t.directory_path === 'string' && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(t.directory_path), `${t.id}: directory must be one safe relative slug`);
    require(!dirs.has(t.directory_path), `${t.id}: duplicate directory`); dirs.add(t.directory_path);
    require(categories.has(t.category), `${t.id}: unknown category`);
    require(statuses.includes(t.status), `${t.id}: unknown status`);
    require(['P1','P2','P3'].includes(t.priority), `${t.id}: invalid priority`);
    require(['S','M','L','XL'].includes(t.implementation_complexity), `${t.id}: invalid complexity`);
    for (const key of ['name','description','notes']) require(typeof t[key] === 'string' && t[key].trim().length > 0, `${t.id}: empty ${key}`);
    for (const key of ['dependencies','required_features','related_tools']) require(Array.isArray(t[key]) && t[key].every(s => typeof s === 'string' && s.trim()), `${t.id}: invalid ${key}`);
    require(t.required_features?.length > 0, `${t.id}: no acceptance features`);
    require(['NOT_STARTED','SMOKE_PASSED','REQUIRED_PASSED','FAILED','PARTIAL'].includes(t.testing_status), `${t.id}: invalid testing_status`);
    require(t.last_verification_date === null || date(t.last_verification_date), `${t.id}: invalid last_verification_date`);
    require(!t.last_verification_date || t.last_verification_date <= r.updated_on, `${t.id}: verification is after registry date`);
    if (backlog.has(t.status)) {
      require(t.testing_status === 'NOT_STARTED', `${t.id}: planned tool cannot claim tests`);
      require(t.verification === null && t.last_verification_date === null, `${t.id}: planned tool cannot claim verification`);
    }
    if (t.sequence_rank !== null) {
      require(Number.isInteger(t.sequence_rank) && t.sequence_rank > 0, `${t.id}: invalid sequence rank`);
      require(!ranks.has(t.sequence_rank), `${t.id}: duplicate sequence rank`); ranks.add(t.sequence_rank);
      require(t.priority === 'P1', `${t.id}: sequenced tool must be P1`);
    }
    if (['TESTED','RELEASED'].includes(t.status)) {
      require(['SMOKE_PASSED','REQUIRED_PASSED'].includes(t.testing_status), `${t.id}: tested status requires passing test evidence`);
      require(Boolean(t.verification?.source_revision && /^[a-f0-9]{64}$/.test(t.verification?.source_sha256 || '') && t.verification?.evidence_path && t.verification?.test_scope?.length && t.last_verification_date), `${t.id}: missing verification evidence`);
    }
    if (t.status === 'RELEASED') {
      const p = t.verification?.publication;
      require(Boolean(p && p.http_status === 200 && p.source_matches === true && p.checked_at && p.url?.startsWith(r.project.website)), `${t.id}: RELEASED requires verified publication`);
    }
  }
  for (const t of r.tools) for (const related of t.related_tools || []) require(ids.has(related) && related !== t.id, `${t.id}: invalid related tool ${related}`);
  require(ranks.size === 0 || Math.max(...ranks) === ranks.size, 'Sequence ranks must be contiguous from 1');
  const proposals = new Set();
  for (const p of r.proposal_resolutions) {
    require(!proposals.has(p.proposed_name), `Duplicate proposal: ${p.proposed_name}`); proposals.add(p.proposed_name);
    require(ids.has(p.tool_id), `Proposal references unknown tool: ${p.tool_id}`);
    require(['NEW_TOOL','COMBINED','EXISTING_FEATURE'].includes(p.disposition) && Boolean(p.reason), `Invalid proposal resolution: ${p.proposed_name}`);
    if (p.disposition === 'EXISTING_FEATURE') require(implemented.has(r.tools.find(t => t.id === p.tool_id)?.status), `Existing feature is not implemented: ${p.proposed_name}`);
  }
  return errors;
}

function generated(r) {
  const s = summarize(r);
  const ordered = r.tools.filter(t => t.sequence_rank !== null).sort((a,b) => a.sequence_rank-b.sequence_rank);
  const ready = ordered.filter(t => t.status === 'READY');
  const active = r.tools.filter(t => t.status === 'IN_PROGRESS');
  const milestone = [25,50,100,200,300,500,1000].find(n=>n>s.released);
  const stats = `| Metric | Count |\n| --- | ---: |\n| Total registered utilities | ${s.total} |\n| Released (dated smoke and publication evidence) | ${s.released} |\n| Implemented but unverified | ${s.implemented_unverified} |\n| Tested, publication unverified | ${s.tested_unpublished} |\n| In development | ${s.in_progress} |\n| Backlog (IDEA + PLANNED + READY + BLOCKED) | ${s.planned} |\n| Ready to start (subset of backlog) | ${s.ready} |\n| Blocked (subset of backlog) | ${s.blocked} |\n\nStatus breakdown: ${Object.entries(s.by_status).map(([k,v]) => `${k}: ${v}`).join('; ')}.\n\nCurrent growth milestone: **${milestone || 'Review the next milestone after 1,000'} released tools**${milestone ? ` (${s.released}/${milestone})` : ''}. Growth targets are not delivery promises.\n\nCurrent implementation task: **${active.map(t=>t.name).join(', ') || 'none'}**. Resolve unfinished work and review the handoff before beginning another utility.\n\nNext ready tool: **${ready[0]?.name || 'Select the next task'}** (${ready[0]?.id || 'unassigned'}).`;
  const sequence = '| Order | Tool ID | Name | Category | Complexity | Status |\n| ---: | --- | --- | --- | --- | --- |\n' + ordered.map(t => `| ${t.sequence_rank} | ${t.id} | ${t.name} | ${r.categories.find(c=>c.id===t.category).name} | ${t.implementation_complexity} | ${t.status} |`).join('\n');
  const catalog = r.categories.map(c => `### ${c.name}\n\n| Tool ID | Utility | Status | Priority | Complexity | Dependencies / gate |\n| --- | --- | --- | --- | --- | --- |\n` + r.tools.filter(t=>t.category===c.id).map(t=>`| ${t.id} | ${t.name} | ${t.status} | ${t.priority} | ${t.implementation_complexity} | ${t.dependencies.filter(d=>!d.startsWith('Tailwind')).join('; ') || 'Browser-native approach; scope review before implementation'} |`).join('\n')).join('\n\n');
  const resolutions = '| Proposed utility | Canonical tool ID | Resolution | Reason |\n| --- | --- | --- | --- |\n' + r.proposal_resolutions.map(p=>`| ${p.proposed_name} | ${p.tool_id} | ${p.disposition} | ${p.reason} |`).join('\n');
  return {'PROGRESS_TRACKER.md':{COUNTS:stats,NEXT:ready.slice(0,5).map(t=>`${t.sequence_rank}. **${t.name}** — ${t.description}`).join('\n') || 'No sequenced READY tool; review the handoff and select a bounded task.'},'ROADMAP.md':{SEQUENCE:sequence,CATALOG:catalog},'audit/BACKLOG_RECONCILIATION.md':{RESOLUTIONS:resolutions}};
}

function replaceBlock(text,key,value) {
  const start=`<!-- GENERATED:${key}:START -->`, end=`<!-- GENERATED:${key}:END -->`;
  if (!text.includes(start) || !text.includes(end)) throw new Error(`Missing generated markers: ${key}`);
  const a=text.indexOf(start)+start.length,b=text.indexOf(end,a);
  return text.slice(0,a)+'\n'+value+'\n'+text.slice(b);
}

export function validateProject(r) {
  const errors = validateRegistry(r);
  if (errors.length) return errors;
  const require = (ok,message) => { if (!ok) errors.push(message); };
  const homepage = read('index.html');
  const links = [...homepage.matchAll(/<a\b[^>]*href="([^"]+)"[^>]*data-title=/g)].map(m=>m[1]);
  const catalog = r.tools.filter(t=>implemented.has(t.status));
  require(links.length===catalog.length, 'Homepage card count differs from implemented registry tools');
  require(new Set(links).size===links.length, 'Duplicate homepage tool link');
  require(homepage.includes(`>${links.length} tools ready to use</p>`), 'Initial homepage count is stale');
  for (const t of r.tools) {
    const file=`${t.directory_path}/index.html`;
    if (implemented.has(t.status)) {
      require(exists(file),`${t.id}: missing implementation`);
      require(links.includes(file),`${t.id}: missing homepage card`);
      if (exists(file)) {
        const html=read(file);
        require(html.includes('href="../index.html"'),`${t.id}: missing Back to Hub link`);
        if (['TESTED','RELEASED'].includes(t.status)) {
          require(normalizedHash(html)===t.verification?.source_sha256,`${t.id}: source changed since verification; retest and update evidence`);
          const evidencePath=t.verification?.evidence_path;
          require(Boolean(evidencePath && exists(evidencePath)),`${t.id}: missing evidence file`);
          if (evidencePath && exists(evidencePath)) {
            const report=JSON.parse(read(evidencePath)),page=report.pages.find(p=>p.path===file);
            require(report.result==='PASS' && page?.source_sha256===t.verification.source_sha256,`${t.id}: evidence does not match source`);
            require(report.source_revision===t.verification.source_revision && report.verified_on===t.last_verification_date,`${t.id}: evidence revision/date mismatch`);
            if (t.status==='RELEASED') require(JSON.stringify(page?.publication)===JSON.stringify(t.verification.publication),`${t.id}: publication evidence mismatch`);
          }
        }
      }
    } else if (backlog.has(t.status)) require(!exists(file),`${t.id}: source exists but registry still claims a planned utility`);
  }
  for (const entry of fs.readdirSync(root,{withFileTypes:true})) {
    if (entry.isDirectory() && exists(`${entry.name}/index.html`)) require(r.tools.some(t=>t.directory_path===entry.name),`Unregistered utility directory: ${entry.name}`);
  }
  for(const file of ['AGENTS.md','PROJECT_MASTER_PLAN.md','PROGRESS_TRACKER.md','ROADMAP.md','ARCHITECTURE.md','DECISIONS.md','CHANGELOG.md','SESSION_HANDOFF.md','README.md']) require(exists(file),`Missing documentation: ${file}`);
  const initial=JSON.parse(read('audit/INITIAL_BACKLOG.json')).proposed_names;
  const mapped=r.proposal_resolutions.map(p=>p.proposed_name);
  require(initial.every(name=>mapped.includes(name)), 'Initial backlog proposals are missing mappings');
  for(const [file,blocks]of Object.entries(generated(r))) {
    if (!exists(file)) { errors.push(`Missing generated document: ${file}`);continue; }
    let expected=read(file);for(const [key,value]of Object.entries(blocks))expected=replaceBlock(expected,key,value);
    require(expected===read(file),`${file}: generated data is stale; run node scripts/project.mjs sync`);
  }
  return errors;
}

function main() {
  const command=process.argv[2] || 'check';
  const registry=JSON.parse(read('TOOL_REGISTRY.json'));
  if(command==='summary') { console.log(JSON.stringify(summarize(registry),null,2));return; }
  if(command==='sync') {
    const errors=validateRegistry(registry);if(errors.length)throw new Error(errors.join('\n'));
    for(const [file,blocks]of Object.entries(generated(registry))) { let text=read(file);for(const [key,value]of Object.entries(blocks))text=replaceBlock(text,key,value);fs.writeFileSync(path.join(root,file),text); }
    console.log('Generated counts, sequence, catalog, and proposal mappings synchronized.');return;
  }
  if(command!=='check')throw new Error('Usage: node scripts/project.mjs [check|sync|summary]');
  const errors=validateProject(registry);
  if(errors.length)throw new Error(errors.join('\n'));
  console.log(`PASS: ${registry.tools.length} unique tools; schema, statuses, references, source evidence, homepage integration and generated documents agree.`);
}
if(process.argv[1] && path.resolve(process.argv[1])===fileURLToPath(import.meta.url)) {
  try {main();}catch(error){console.error(error.message);process.exitCode=1;}
}
