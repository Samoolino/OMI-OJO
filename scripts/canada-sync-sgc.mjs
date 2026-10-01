import fs from 'node:fs/promises';
import crypto from 'node:crypto';

const manifestPath = new URL('../data/canada/sgc-2021-manifest.json', import.meta.url);
const manifest = JSON.parse(await fs.readFile(manifestPath, 'utf8'));
const outDir = new URL('../data/canada/generated/', import.meta.url);
await fs.mkdir(outDir, { recursive: true });

async function fetchText(url) {
  const response = await fetch(url, { headers: { 'user-agent': 'OMI-OJO-Canada-SGC-Sync/1.0' } });
  if (!response.ok) throw new Error(`SGC download failed ${response.status}: ${url}`);
  return response.text();
}

function sha256(text) {
  return crypto.createHash('sha256').update(text).digest('hex');
}

function parseCsv(text) {
  const rows = [];
  let row = [], cell = '', quoted = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i], n = text[i + 1];
    if (c === '"' && quoted && n === '"') { cell += '"'; i++; continue; }
    if (c === '"') { quoted = !quoted; continue; }
    if (c === ',' && !quoted) { row.push(cell); cell = ''; continue; }
    if ((c === '\n' || c === '\r') && !quoted) {
      if (c === '\r' && n === '\n') i++;
      row.push(cell); cell = '';
      if (row.some(v => v.length)) rows.push(row);
      row = [];
      continue;
    }
    cell += c;
  }
  if (cell.length || row.length) { row.push(cell); rows.push(row); }
  const headers = rows.shift().map(v => v.trim());
  return rows.map(values => Object.fromEntries(headers.map((h, i) => [h, (values[i] ?? '').trim()])));
}

function pick(row, names) {
  for (const name of names) if (row[name] !== undefined) return row[name];
  return '';
}

const [structureCsv, elementsCsv] = await Promise.all([
  fetchText(manifest.source_urls.classification_structure_csv),
  fetchText(manifest.source_urls.elements_csv)
]);

const structure = parseCsv(structureCsv);
const elements = parseCsv(elementsCsv);
const elementsByCode = new Map();
for (const row of elements) {
  const code = pick(row, ['SGCUID','SGC code','SGC_CODE','Code']);
  if (code) elementsByCode.set(code, row);
}

const nodes = [];
for (const row of structure) {
  const code = pick(row, ['SGC code','SGC_CODE','Code','SGCUID']);
  const name = pick(row, ['Name','name','Geographical region of Canada','Province or territory','Census division','Census subdivision']);
  const type = pick(row, ['Type','type','Geographic unit','Geographic level']);
  if (!code || !name) continue;
  const digits = code.replace(/\D/g, '');
  let level = 'UNKNOWN';
  if (digits.length === 1) level = 'REGION';
  else if (digits.length === 2) level = 'PR';
  else if (digits.length === 4) level = 'CD';
  else if (digits.length === 7) level = 'CSD';
  nodes.push({
    id: level === 'REGION' ? `CA/R/${digits}` : `CA/${level}/${digits}`,
    code,
    level,
    name,
    type,
    parent_id: level === 'CSD' ? `CA/CD/${digits.slice(0,4)}` : level === 'CD' ? `CA/PR/${digits.slice(0,2)}` : level === 'PR' ? `CA/R/${digits.slice(0,1)}` : 'CA',
    source: 'Statistics Canada SGC 2021',
    source_version: manifest.release
  });
}

const counts = Object.fromEntries(['REGION','PR','CD','CSD'].map(level => [level, nodes.filter(n => n.level === level).length]));
const errors = [];
for (const node of nodes) {
  if (node.level !== 'REGION' && !nodes.some(parent => parent.id === node.parent_id)) errors.push(`Missing parent for ${node.id}`);
}

const snapshot = {
  schema_id: 'OMI-OJO-CA-SGC-GRAPH-1',
  generated_at: new Date().toISOString(),
  source: manifest.source_urls.classification_structure_csv,
  source_sha256: sha256(structureCsv),
  elements_sha256: sha256(elementsCsv),
  counts,
  validation: { expected: manifest.expected_counts, errors, valid: errors.length === 0 },
  nodes
};

await fs.writeFile(new URL('sgc-2021-graph.json', outDir), JSON.stringify(snapshot, null, 2));
await fs.writeFile(new URL('sgc-2021-source-manifest.json', outDir), JSON.stringify({
  ...manifest,
  retrieved_at: snapshot.generated_at,
  source_sha256: snapshot.source_sha256,
  elements_sha256: snapshot.elements_sha256,
  generated_file: 'sgc-2021-graph.json'
}, null, 2));

console.log(JSON.stringify({ status: errors.length ? 'INVALID' : 'VALID', counts, errors }, null, 2));
if (errors.length) process.exitCode = 1;
