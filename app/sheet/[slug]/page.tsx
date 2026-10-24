import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import {
  artifactUrl, createdAt, fmtDate, getSheet, MODE_LABEL, repoFileUrl, sheetName, sheets, STATUS_LABEL, type Mode, type Status,
} from '@/lib/data';
import { docHref, listDocs } from '@/lib/docs';
import Frame from './frame';
import styles from './sheet.module.css';

export function generateStaticParams() {
  return sheets.map((s) => ({ slug: s.slug }));
}

export async function generateMetadata({ params }: PageProps<'/sheet/[slug]'>): Promise<Metadata> {
  const s = getSheet((await params).slug);
  return s ? { title: sheetName(s), description: s.summary ?? undefined } : {};
}

export default async function SheetPage({ params }: PageProps<'/sheet/[slug]'>) {
  const s = getSheet((await params).slug);
  if (!s) notFound();
  const docs = listDocs();
  const docIds = new Set(docs.map((d) => d.id));
  const readme = s.pipeline ? `mirror/${s.pipeline}/README` : null;
  const notes = (s.kbNotes ?? []).filter((n) => docIds.has(`kb/notes/${n}`));
  const url = artifactUrl(s);
  const superseded = s.supersededBy ? sheets.find((x) => x.slug === s.supersededBy) : null;
  const h = s.history;

  return (
    <main className={styles.layout}>
      <aside className={styles.panel}>
        <Link href="/" className={styles.back}>← All sheets</Link>
        <div className={styles.badges}>
          {(s.modes ?? []).map((m) => <span key={m} className={`badge ${m}`}>{MODE_LABEL[m as Mode] ?? m}</span>)}
          <span className={`status ${s.status ?? 'active'}`}>{STATUS_LABEL[(s.status ?? 'active') as Status]}</span>
        </div>
        <h1 className="display">{sheetName(s)}</h1>
        {s.summary && <p className={styles.summary}>{s.summary}</p>}
        {superseded && (
          <p className={styles.callout}>Superseded by <Link href={`/sheet/${superseded.slug}`}>{sheetName(superseded)}</Link>.</p>
        )}

        <h2>Dates</h2>
        <dl className={styles.facts}>
          {s.vehicleDay && (<><dt>Vehicles</dt><dd>{s.vehicleDay}</dd></>)}
          {s.networkDate && (<><dt>Network</dt><dd>{s.networkDate}</dd></>)}
          <dt>Created</dt>
          <dd className="mono">{fmtDate(createdAt(s))}{s.createdNote && <small>{s.createdNote}</small>}</dd>
          <dt>Published</dt>
          <dd className="mono">
            {h?.firstPublished ? <>{fmtDate(h.firstPublished)} → {fmtDate(h.lastPublished)}<small>{h.publishCount} publishes, artifact v{h.latestVersion}</small></> : url ? 'published as an artifact; no publish record on this machine' : 'never published'}
          </dd>
          <dt>File</dt>
          <dd className="mono">{fmtDate(s.sourceModified, true)}<small>{s.location === 'archive' ? 'archive/' : ''}{s.file} · {(s.bytes / 1024).toFixed(0)} kB</small></dd>
          <dt>Synced</dt>
          <dd className="mono">{fmtDate(s.syncedAt, true)}</dd>
        </dl>

        {!!s.refreshTriggers?.length && (
          <>
            <h2>Refresh when</h2>
            <ul className={styles.list}>{s.refreshTriggers.map((t) => <li key={t}>{t}</li>)}</ul>
          </>
        )}

        <h2>Sources</h2>
        {s.sources?.length ? (
          <ul className={styles.sources}>
            {s.sources.map((src) => (
              <li key={src.name + (src.url ?? '')}>
                <span className={styles.role}>{src.role ?? 'source'}</span>
                {src.url ? <a href={src.url.startsWith('http') ? src.url : `https://${src.url}`} target="_blank" rel="noreferrer">{src.name}</a> : <b>{src.name}</b>}
                {src.note && <small>{src.note}</small>}
              </li>
            ))}
          </ul>
        ) : <p className={styles.muted}>Not recorded.</p>}

        <h2>How it is kept in sync</h2>
        {s.sync && <p className={styles.p}>{s.sync}</p>}
        <dl className={styles.facts}>
          <dt>Pipeline</dt>
          <dd>{s.pipeline ? <a href={repoFileUrl(`mirror/${s.pipeline}`).replace('/blob/', '/tree/')} target="_blank" rel="noreferrer" className="mono">{s.pipeline}</a> : 'none'}</dd>
          {s.build && (<><dt>Rebuild</dt><dd><code className={styles.code}>{s.build}</code></dd></>)}
          {s.fetch && (<><dt>Fetch</dt><dd><code className={styles.code}>{s.fetch}</code></dd></>)}
          {!!s.dependsOn?.length && (<><dt>Shares</dt><dd className="mono">{s.dependsOn.join(', ')}</dd></>)}
          {!!s.rawSnapshots?.length && (<><dt>Raw data</dt><dd className="mono">{s.rawSnapshots.join(' · ')}<small>stored in the working folder, not in this repo</small></dd></>)}
          {s.builtBy && (<><dt>Built by</dt><dd>{s.builtBy}</dd></>)}
          <dt>Artifact</dt>
          <dd>{url ? <a href={url} target="_blank" rel="noreferrer" className="mono">{url.replace('https://', '')}</a> : '—'}</dd>
        </dl>
        {!!s.updateRecipe?.length && (
          <ol className={styles.recipe}>{s.updateRecipe.map((step, i) => <li key={i}>{step}</li>)}</ol>
        )}
        {s.notes && (<><h2>Notes</h2><p className={styles.p}>{s.notes}</p></>)}

        <h2>Read more</h2>
        <ul className={styles.list}>
          {readme && docIds.has(readme) && <li><Link href={docHref(readme)}>Pipeline README — decisions and update recipe</Link></li>}
          {notes.map((n) => <li key={n}><Link href={docHref(`kb/notes/${n}`)}>Note: {n}</Link></li>)}
          <li><Link href={docHref('kb/workflow')}>Workflow: refreshing a sheet</Link></li>
        </ul>
      </aside>
      <Frame src={`/sheets/${s.slug}.html`} title={sheetName(s)} />
    </main>
  );
}
