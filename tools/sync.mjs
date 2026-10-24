// Pull the sheets and pipeline code from the working folder into this repo, then rebuild data/sheets.json.
//
//   pnpm sync                      # source = $SIMUTRANS_SOURCE or the OneDrive project folder
//   pnpm sync -- --dry             # report only, change nothing
//
// One-way: the working folder (with its 1.1 GB of raw downloads) is where pipelines run; this repo holds
// copies of the published HTML (public/sheets/), the pipeline code and docs (mirror/pipeline/, no data),
// and the catalogue the web app shows. Never copies data/raw or data/derived.
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const REPO = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const SOURCE = process.env.SIMUTRANS_SOURCE || 'D:/OneDrive/Documents/Personal/Transport Fun/Simutrans-Timetable';
const DRY = process.argv.includes('--dry');
const SHEETS_DIR = path.join(REPO, 'public', 'sheets');
const MIRROR = path.join(REPO, 'mirror', 'pipeline');

// Pipeline files worth versioning: code, configs, docs, templates. Everything under data/ stays behind.
const KEEP_EXT = new Set(['.py', '.md', '.json', '.html', '.css', '.txt', '.tsv']);
const SKIP_DIRS = new Set(['data', '__pycache__', 'legacy', 'node_modules', '.git']);
const SKIP_FILES = new Set(['vagonweb_cookies.txt']);

export function slugify(name) {
  return name
    .replace(/\.html$/i, '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/^-|-$/g, '');
}

const sha = (buf) => createHash('sha256').update(buf).digest('hex').slice(0, 16);
const readJson = (p, fallback) => (fs.existsSync(p) ? JSON.parse(fs.readFileSync(p, 'utf8')) : fallback);

function listSheets() {
  const out = [];
  for (const [dir, location] of [['', 'root'], ['archive', 'archive']]) {
    const abs = path.join(SOURCE, dir);
    if (!fs.existsSync(abs)) continue;
    for (const f of fs.readdirSync(abs)) {
      if (!f.toLowerCase().endsWith('.html')) continue;
      const full = path.join(abs, f);
      const buf = fs.readFileSync(full);
      const title = /<title>([^<]*)<\/title>/i.exec(buf.toString('utf8'))?.[1]?.trim() ?? null;
      out.push({ file: f, location, full, buf, title, bytes: buf.length, mtime: fs.statSync(full).mtime.toISOString() });
    }
  }
  return out;
}

function copyPipeline(src, dst, stats) {
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) {
      if (!SKIP_DIRS.has(entry.name)) copyPipeline(s, d, stats);
    } else if (KEEP_EXT.has(path.extname(entry.name).toLowerCase()) && !SKIP_FILES.has(entry.name)) {
      const size = fs.statSync(s).size;
      if (size > 2_000_000) { stats.skipped.push(`${path.relative(MIRROR, d)} (${(size / 1e6).toFixed(1)} MB)`); continue; }
      if (!DRY) { fs.mkdirSync(path.dirname(d), { recursive: true }); fs.copyFileSync(s, d); }
      stats.files++;
    }
  }
}

function main() {
  if (!fs.existsSync(SOURCE)) {
    console.error(`Source folder not found: ${SOURCE}\nSet SIMUTRANS_SOURCE to the Simutrans-Timetable working folder.`);
    process.exit(1);
  }
  const catalog = readJson(path.join(REPO, 'data', 'catalog.json'), { sheets: [] });
  const provenance = readJson(path.join(REPO, 'data', 'provenance.json'), { sheets: {} }).sheets;
  const previous = readJson(path.join(REPO, 'data', 'sheets.json'), { sheets: [] });
  const prevByFile = new Map(previous.sheets.map((s) => [s.file, s]));
  const byFile = new Map(catalog.sheets.map((c) => [c.file, c]));
  const syncedAt = new Date().toISOString();

  // 1. Sheets
  const found = listSheets();
  if (!DRY) {
    fs.rmSync(SHEETS_DIR, { recursive: true, force: true });
    fs.mkdirSync(SHEETS_DIR, { recursive: true });
  }
  const report = { added: [], changed: [], unchanged: 0, removed: [], uncatalogued: [] };
  const sheets = [];
  for (const s of found) {
    const cat = byFile.get(s.file);
    const slug = cat?.slug ?? slugify(s.file);
    const hash = sha(s.buf);
    if (!DRY) fs.writeFileSync(path.join(SHEETS_DIR, `${slug}.html`), s.buf);
    const prev = prevByFile.get(s.file);
    if (!prev) report.added.push(s.file);
    else if (prev.sha256 !== hash) report.changed.push(s.file);
    else report.unchanged++;
    if (!cat) report.uncatalogued.push(s.file);
    // Provenance is keyed by file name; a renamed sheet also inherits its earlier names' history.
    const provs = [s.file, ...(cat?.previousFiles ?? [])].map((f) => provenance[f]).filter(Boolean);
    const min = (k) => provs.map((p) => p[k]).filter(Boolean).sort()[0] ?? null;
    const max = (k) => provs.map((p) => p[k]).filter(Boolean).sort().at(-1) ?? null;
    sheets.push({
      slug,
      file: s.file,
      location: s.location,
      title: s.title,
      bytes: s.bytes,
      sha256: hash,
      sourceModified: s.mtime,
      contentChangedAt: prev && prev.sha256 === hash ? prev.contentChangedAt ?? syncedAt : syncedAt,
      syncedAt,
      history: provs.length
        ? {
            firstSeen: min('firstSeen'),
            firstPublished: min('firstPublished'),
            lastPublished: max('lastPublished'),
            publishCount: provs.reduce((n, p) => n + p.publishCount, 0),
            latestVersion: Math.max(0, ...provs.map((p) => p.latestVersion ?? 0)) || null,
            artifactUrls: [...new Set(provs.flatMap((p) => p.artifactUrls))],
            sessions: [...new Set(provs.flatMap((p) => p.sessions))],
          }
        : null,
      ...(cat ?? {}),
    });
  }
  const foundFiles = new Set(found.map((s) => s.file));
  report.removed = previous.sheets.filter((s) => !foundFiles.has(s.file)).map((s) => s.file);
  const missing = catalog.sheets.filter((c) => !foundFiles.has(c.file)).map((c) => c.file);

  // 2. Pipeline code and docs
  const stats = { files: 0, skipped: [] };
  const pipeSrc = path.join(SOURCE, 'pipeline');
  if (fs.existsSync(pipeSrc)) {
    if (!DRY) fs.rmSync(MIRROR, { recursive: true, force: true });
    copyPipeline(pipeSrc, MIRROR, stats);
  }

  // 3. Catalogue for the app
  sheets.sort((a, b) => a.slug.localeCompare(b.slug));
  if (!DRY) {
    fs.writeFileSync(
      path.join(REPO, 'data', 'sheets.json'),
      JSON.stringify({ _doc: 'Generated by tools/sync.mjs from data/catalog.json + data/provenance.json + the source folder. Do not edit.', source: SOURCE, syncedAt, sheets }, null, 1) + '\n',
    );
  }

  console.log(`Source: ${SOURCE}${DRY ? '  (dry run)' : ''}`);
  console.log(`Sheets: ${found.length} (${report.added.length} new, ${report.changed.length} changed, ${report.unchanged} unchanged, ${report.removed.length} gone)`);
  for (const f of report.added) console.log(`  + ${f}`);
  for (const f of report.changed) console.log(`  ~ ${f}`);
  for (const f of report.removed) console.log(`  - ${f}`);
  if (report.uncatalogued.length) console.log(`Not in data/catalog.json (add an entry):\n  ${report.uncatalogued.join('\n  ')}`);
  if (missing.length) console.log(`In catalog.json but no file in the source:\n  ${missing.join('\n  ')}`);
  console.log(`Pipeline mirror: ${stats.files} files${stats.skipped.length ? `, skipped large: ${stats.skipped.join(', ')}` : ''}`);
}

main();
