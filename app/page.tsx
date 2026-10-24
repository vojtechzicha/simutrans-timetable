import { createdAt, fmtDate, REGION_ORDER, sheetName, sheets, shortDay, sourceFolder, syncedAt, updatedAt } from '@/lib/data';
import SheetBoard, { type BoardRow } from './sheet-board';
import styles from './page.module.css';

export default function Home() {
  const rows: BoardRow[] = sheets.map((s) => ({
    slug: s.slug,
    name: sheetName(s),
    file: s.file,
    summary: s.summary ?? null,
    region: s.region ?? 'Other',
    modes: s.modes ?? [],
    status: s.status ?? 'active',
    dataDay: [shortDay(s.vehicleDay) && `vehicles ${shortDay(s.vehicleDay)}`, shortDay(s.networkDate) && `network ${shortDay(s.networkDate)}`]
      .filter(Boolean).join(' · ') || null,
    created: createdAt(s),
    createdLabel: fmtDate(createdAt(s)),
    updated: updatedAt(s),
    updatedLabel: fmtDate(updatedAt(s)),
    publishCount: s.history?.latestVersion ?? 0,
    pipeline: s.pipeline ?? null,
    sourceCount: s.sources?.length ?? 0,
  }));
  const regions = [...REGION_ORDER, ...new Set(rows.map((r) => r.region).filter((r) => !REGION_ORDER.includes(r)))];
  const count = (st: string) => rows.filter((r) => r.status === st).length;
  const pipelines = new Set(sheets.map((s) => s.pipeline).filter(Boolean)).size;
  const publishes = sheets.reduce((n, s) => n + (s.history?.publishCount ?? 0), 0);

  return (
    <main className="wrap">
      <section className={`${styles.hero} rise`}>
        <div>
          <p className={styles.kicker}>Jízdní řády pro Simutrans</p>
          <h1 className="display">
            Every timetable sheet,<br />with where it came from.
          </h1>
          <p className={styles.lede}>
            Real Czech timetables and vehicle allocations, turned into the values typed into the Simutrans fork — one sheet per city,
            mode or rail corridor. Each sheet keeps its own design; this board adds its sources, how it is rebuilt, and its dates.
          </p>
        </div>
        <dl className={styles.stats}>
          <div><dt>Sheets</dt><dd className="mono">{rows.length}</dd></div>
          <div><dt>Active</dt><dd className="mono">{count('active')}</dd></div>
          <div><dt>Archived</dt><dd className="mono">{count('archived') + count('superseded')}</dd></div>
          <div><dt>Pipelines</dt><dd className="mono">{pipelines}</dd></div>
          <div><dt>Publishes</dt><dd className="mono">{publishes}</dd></div>
          <div className={styles.wide}>
            <dt>Last sync</dt>
            <dd className="mono" title={sourceFolder}>{fmtDate(syncedAt, true)}</dd>
          </div>
        </dl>
      </section>
      <SheetBoard rows={rows} regions={regions} />
    </main>
  );
}
