import Link from 'next/link';
import { docHref, listDocs } from '@/lib/docs';
import styles from './docs.module.css';

const GROUPS = ['Knowledge base', 'Rules', 'Methods', 'Pipelines', 'Notes'];
const KB_ORDER = ['kb/README', 'kb/workflow', 'kb/sources', 'kb/lessons', 'kb/related-projects'];

export default function DocShell({ current, html, description, sourceUrl, file }: {
  current: string; html: string; description: string | null; sourceUrl: string; file: string;
}) {
  const docs = listDocs();
  const ordered = (g: string) => {
    const list = docs.filter((d) => d.group === g);
    if (g !== 'Knowledge base') return list;
    const rank = (id: string) => (KB_ORDER.includes(id) ? KB_ORDER.indexOf(id) : 99);
    return [...list].sort((a, b) => rank(a.id) - rank(b.id));
  };
  const label = (id: string, title: string, g: string) => {
    if (g === 'Pipelines') return id.replace(/^mirror\/pipeline\//, '').replace(/\/README$/, '');
    if (g === 'Notes') return id.replace(/^kb\/notes\//, '');
    return title;
  };
  return (
    <main className={styles.layout}>
      <nav className={styles.nav} aria-label="Documents">
        {GROUPS.map((g) => (
          <details key={g} open={g !== 'Notes' && g !== 'Pipelines' ? true : docs.some((d) => d.group === g && d.id === current)}>
            <summary className="display">{g} <span className="mono">{docs.filter((d) => d.group === g).length}</span></summary>
            <ul>
              {ordered(g).map((d) => (
                <li key={d.id}>
                  <Link href={docHref(d.id)} aria-current={d.id === current ? 'page' : undefined} title={d.description ?? d.title}>
                    {label(d.id, d.title, g)}
                  </Link>
                </li>
              ))}
            </ul>
          </details>
        ))}
      </nav>
      <article className={styles.article}>
        <div className={styles.meta}>
          <span className="mono">{file}</span>
          <a href={sourceUrl} target="_blank" rel="noreferrer">View on GitHub ↗</a>
        </div>
        {description && <p className={styles.description}>{description}</p>}
        <div className="prose" dangerouslySetInnerHTML={{ __html: html }} />
      </article>
    </main>
  );
}
