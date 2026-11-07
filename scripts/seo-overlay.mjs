// Exact historical-test projection matching seo_overlay.py; not a runtime script.
import fs from 'node:fs';
import {createHash} from 'node:crypto';

const manifestHash = '48493194140992b186e31dda1a293286ee301f2cf61bea2441283280585f60d5';
const hash = value => createHash('sha256').update(value.replaceAll('\r\n','\n')).digest('hex');

export function historicalSource(root, path, source) {
  const file = new URL('audit/SEO_TASK_2A_SOURCE_OVERLAY.json', root);
  if (!fs.existsSync(file)) return source;
  const raw = fs.readFileSync(file, 'utf8');
  if (hash(raw) !== manifestHash) throw new Error('SEO overlay manifest differs from reviewed candidate');
  const manifest = JSON.parse(raw);
  if (manifest.schema_version !== 1 || manifest.base_revision !== '7cdd6f43800fc1ae01ee597d9bab1a7a597f7f32' || manifest.state !== 'PENDING_REVIEW_AND_DEPLOYMENT') throw new Error('SEO overlay manifest identity invalid');
  const entry = manifest.pages[path];
  if (!entry) return source;
  if (hash(source) === entry.previous_sha256) return source;
  if (hash(source) !== entry.candidate_sha256) throw new Error('Unapproved source change outside SEO Task 2A overlay: ' + path);
  if (entry.canonical !== 'https://everydaydigitalbox.com/' + path) throw new Error('Wrong SEO canonical route');
  const nl = source.includes('\r\n') ? '\r\n' : '\n';
  const inserted = '<head>' + nl + '  <link rel="canonical" href="' + entry.canonical + '">' + nl;
  if (source.split(inserted).length !== 2) throw new Error('SEO canonical insertion moved or duplicated');
  const previous = source.replace(inserted, '<head>' + (entry.head_had_newline ? nl : ''));
  if (hash(previous) !== entry.previous_sha256) throw new Error('SEO source does not reconstruct audited main');
  return previous;
}
