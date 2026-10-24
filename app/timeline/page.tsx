import type { Metadata } from 'next';
import Link from 'next/link';
import { createdAt, fmtDate, REGION_ORDER, sheetName, sheets, updatedAt } from '@/lib/data';
import styles from './timeline.module.css';

export const metadata: Metadata = { title: 'Timeline' };

const DAY = 86_400_000;
const day = (iso: string) => Date.UTC(+iso.slice(0, 4), +iso.slice(5, 7) - 1, +iso.slice(8, 10));

export default function Timeline() {
  const rows = sheets
    .map((s) => ({ s, start: createdAt(s), end: updatedAt(s) }))
    .filter((r): r is typeof r & { start: string } => !!r.start)
    .map((r) => ({ ...r, end: r.end && r.end > r.start ? r.end : r.start }));
  const min = Math.min(...rows.map((r) => day(r.start)));
  const max = Math.max(...rows.map((r) => day(r.end)), min + DAY);
  const span = (max - min) / DAY + 1;
  const pct = (iso: string) => (((day(iso) - min) / DAY) / span) * 100;
  const weeks: number[] = [];
  for (let t = min; t <= max; t += DAY) if (new Date(t).getUTCDay() === 1) weeks.push(t);
  const regions = REGION_ORDER.filter((g) => rows.some((r) => r.s.region === g));

  return (
    <main className="wrap">
      <header className={`${styles.head} rise`}>
        <h1 className="display">Timeline</h1>
        <p>
          Each bar runs from the day a sheet first appeared (first write or publish in a recorded session, or the catalogue date) to its
          last publish. The number on a bar is the artifact&apos;s latest version. Faded bars are archived sheets.
        </p>
      </header>
      <div className={styles.chart}>
        <div className={styles.axis}>
          {weeks.map((t) => (
            <span key={t} style={{ left: `${(((t - min) / DAY) / span) * 100}%` }} className="mono">
              {fmtDate(new Date(t).toISOString()).replace(/ \d{4}$/, '')}
            </span>
          ))}
        </div>
        {regions.map((g) => (
          <section key={g}>
            <h2 className="display">{g}</h2>
            {rows.filter((r) => r.s.region === g).sort((a, b) => a.start.localeCompare(b.start)).map(({ s, start, end }) => (
              <Link key={s.slug} href={`/sheet/${s.slug}`} className={styles.row} data-status={s.status}>
                <span className={styles.label}>{sheetName(s)}</span>
                <span className={styles.track}>
                  {weeks.map((t) => <i key={t} style={{ left: `${(((t - min) / DAY) / span) * 100}%` }} />)}
                  <span
                    className={`${styles.bar} ${styles[s.modes?.[0] ?? 'bus'] ?? ''}`}
                    style={{ left: `${pct(start)}%`, width: `max(8px, ${pct(end) - pct(start) + 100 / span}%)` }}
                    title={`${fmtDate(start)} → ${fmtDate(end)}`}
                  >
                    {s.history?.latestVersion ? <b className="mono">v{s.history.latestVersion}</b> : null}
                  </span>
                </span>
              </Link>
            ))}
          </section>
        ))}
      </div>
    </main>
  );
}
