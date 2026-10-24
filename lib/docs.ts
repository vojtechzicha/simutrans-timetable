import fs from 'node:fs';
import path from 'node:path';
import { Marked, type Tokens } from 'marked';

const ROOT = process.cwd();
// Documents the app renders: the KB and the pipeline docs mirrored from the working folder.
const DOC_ROOTS = ['kb', 'mirror/pipeline'];

export interface Doc {
  id: string; // repo-relative path without .md, e.g. "kb/rules/fork-schedule"
  file: string; // repo-relative path
  title: string;
  description: string | null;
  group: string;
}

function walk(dir: string, out: string[]) {
  if (!fs.existsSync(dir)) return;
  for (const e of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, e.name);
    if (e.isDirectory()) walk(p, out);
    else if (e.name.endsWith('.md')) out.push(path.relative(ROOT, p).split(path.sep).join('/'));
  }
}

function splitFrontmatter(src: string) {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?/.exec(src);
  if (!m) return { meta: {} as Record<string, string>, body: src };
  const meta: Record<string, string> = {};
  for (const line of m[1].split(/\r?\n/)) {
    const kv = /^([a-zA-Z_]+):\s*(.*)$/.exec(line);
    if (kv && kv[2]) meta[kv[1]] = kv[2].replace(/^"(.*)"$/, '$1').replace(/\\"/g, '"');
  }
  return { meta, body: src.slice(m[0].length) };
}

function groupOf(file: string) {
  if (file.startsWith('kb/rules/')) return 'Rules';
  if (file.startsWith('kb/notes/')) return 'Notes';
  if (file.startsWith('kb/')) return 'Knowledge base';
  if (/^mirror\/pipeline\/[^/]+\.md$/.test(file)) return 'Methods';
  return 'Pipelines';
}

let cache: Doc[] | null = null;
export function listDocs(): Doc[] {
  if (cache) return cache;
  const files: string[] = [];
  for (const r of DOC_ROOTS) walk(path.join(/*turbopackIgnore: true*/ ROOT, r), files);
  cache = files.sort().map((file) => {
    const { meta, body } = splitFrontmatter(fs.readFileSync(path.join(/*turbopackIgnore: true*/ ROOT, file), 'utf8'));
    const h1 = /^#\s+(.+)$/m.exec(body)?.[1]?.trim();
    const pipelineName = /^mirror\/pipeline\/([^/]+)\/(.+)\.md$/.exec(file);
    const title =
      h1 ?? meta.name ?? (pipelineName ? `${pipelineName[1]} — ${pipelineName[2]}` : path.basename(file, '.md'));
    return { id: file.replace(/\.md$/, ''), file, title, description: meta.description ?? null, group: groupOf(file) };
  });
  return cache;
}

export const docHref = (id: string) => `/docs/${id.split('/').map(encodeURIComponent).join('/')}`;

/** Resolve a link target written in a doc (relative .md path, repo path, or [[note]]) to a doc id. */
function resolveDoc(target: string, fromFile: string): string | null {
  const ids = new Set(listDocs().map((d) => d.id));
  const clean = target.replace(/#.*$/, '').replace(/\.md$/, '');
  const candidates = [
    path.posix.normalize(path.posix.join(path.posix.dirname(fromFile), clean)),
    clean.replace(/^\/+/, ''),
    `mirror/${clean.replace(/^\/+/, '')}`,
    `mirror/pipeline/${clean.replace(/^pipeline\//, '')}`,
    `kb/${clean}`,
  ];
  return candidates.find((c) => ids.has(c)) ?? null;
}

export function renderDoc(id: string) {
  const doc = listDocs().find((d) => d.id === id);
  if (!doc) return null;
  const { body } = splitFrontmatter(fs.readFileSync(path.join(/*turbopackIgnore: true*/ ROOT, doc.file), 'utf8'));
  // [[note-name]] wiki links from the memory notes
  const withWiki = body.replace(/\[\[([a-z0-9-]+)\]\]/g, (_, n: string) =>
    resolveDoc(`kb/notes/${n}`, doc.file) ? `[${n}](/${'kb/notes/' + n}.md)` : `*${n}*`,
  );
  const marked = new Marked({ gfm: true });
  marked.use({
    renderer: {
      link(this: { parser: { parseInline: (t: Tokens.Generic[]) => string } }, token: Tokens.Link) {
        const text = this.parser.parseInline(token.tokens);
        const href = token.href;
        if (/^https?:/.test(href)) return `<a href="${href}" target="_blank" rel="noreferrer">${text}</a>`;
        const id = resolveDoc(href.replace(/^\//, ''), doc.file);
        if (id) return `<a href="${docHref(id)}${href.includes('#') ? href.slice(href.indexOf('#')) : ''}">${text}</a>`;
        return `<a href="${href}">${text}</a>`;
      },
      codespan(token: Tokens.Codespan) {
        const raw = token.text;
        const decoded = raw.replace(/&amp;/g, '&').replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&quot;/g, '"').replace(/&#39;/g, "'");
        if (/\.md$/.test(decoded)) {
          const id = resolveDoc(decoded, doc.file);
          if (id) return `<a class="code-link" href="${docHref(id)}"><code>${raw}</code></a>`;
        }
        return `<code>${raw}</code>`;
      },
    },
  });
  return { doc, html: marked.parse(withWiki) as string };
}
