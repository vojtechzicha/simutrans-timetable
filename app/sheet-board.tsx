'use client';

import Link from 'next/link';
import { useMemo, useState } from 'react';
import styles from './sheet-board.module.css';

export interface BoardRow {
  slug: string;
  name: string;
  file: string;
  summary: string | null;
  region: string;
  modes: string[];
  status: string;
  dataDay: string | null;
  created: string | null;
  createdLabel: string;
  updated: string | null;
  updatedLabel: string;
  publishCount: number;
  pipeline: string | null;
  sourceCount: number;
}

const MODES = ['tram', 'trolleybus', 'bus', 'metro', 'rail'] as const;
const STATUSES = ['active', 'reference', 'archived', 'superseded'] as const;
type Sort = 'region' | 'created' | 'updated';

export default function SheetBoard({ rows, regions }: { rows: BoardRow[]; regions: string[] }) {
  const [q, setQ] = useState('');
  const [modes, setModes] = useState<string[]>([]);
  const [statuses, setStatuses] = useState<string[]>(['active', 'reference']);
  const [sort, setSort] = useState<Sort>('region');

  const toggle = (list: string[], set: (v: string[]) => void, v: string) =>
    set(list.includes(v) ? list.filter((x) => x !== v) : [...list, v]);

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
    return rows.filter((r) => {
      if (statuses.length && !statuses.includes(r.status)) return false;
      if (modes.length && !r.modes.some((m) => modes.includes(m))) return false;
      if (!needle) return true;
      const hay = `${r.name} ${r.file} ${r.summary ?? ''} ${r.region} ${r.pipeline ?? ''}`.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '');
      return hay.includes(needle);
    });
  }, [rows, q, modes, statuses]);

  const groups = useMemo(() => {
    if (sort !== 'region') {
      const key = sort === 'created' ? 'created' : 'updated';
      return [{ title: sort === 'created' ? 'Newest first' : 'Recently updated', rows: [...filtered].sort((a, b) => (b[key] ?? '').localeCompare(a[key] ?? '')) }];
    }
    return regions
      .map((title) => ({ title, rows: filtered.filter((r) => r.region === title) }))
      .filter((g) => g.rows.length);
  }, [filtered, regions, sort]);

  return (
    <div className={styles.board}>
      <div className={styles.controls}>
        <input
          className={styles.search}
          type="search"
          placeholder="Search sheets, lines, places…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          aria-label="Search sheets"
        />
        <div className={styles.chips} role="group" aria-label="Mode">
          {MODES.map((m) => (
            <button key={m} className={`${styles.chip} ${modes.includes(m) ? styles.on : ''}`} data-mode={m} onClick={() => toggle(modes, setModes, m)}>
              {m}
            </button>
          ))}
        </div>
        <div className={styles.chips} role="group" aria-label="Status">
          {STATUSES.map((s) => (
            <button key={s} className={`${styles.chip} ${statuses.includes(s) ? styles.on : ''}`} onClick={() => toggle(statuses, setStatuses, s)}>
              {s}
            </button>
          ))}
        </div>
        <label className={styles.sort}>
          <span>Order</span>
          <select value={sort} onChange={(e) => setSort(e.target.value as Sort)}>
            <option value="region">by region</option>
            <option value="created">by creation date</option>
            <option value="updated">by last update</option>
          </select>
        </label>
      </div>

      <div className={styles.head} aria-hidden>
        <span>Sheet</span>
        <span>Data as of</span>
        <span>Created</span>
        <span>Last updated</span>
      </div>

      {groups.map((g) => (
        <section key={g.title} className={styles.group}>
          <h2 className={`display ${styles.groupTitle}`}>
            {g.title} <span className="mono">{g.rows.length}</span>
          </h2>
          {g.rows.map((r) => (
            <Link key={r.slug} href={`/sheet/${r.slug}`} className={styles.row}>
              <span className={styles.main}>
                <span className={styles.badges}>
                  {r.modes.map((m) => (
                    <span key={m} className={`badge ${m}`}>{m}</span>
                  ))}
                  {r.status !== 'active' && <span className={`status ${r.status}`}>{r.status}</span>}
                </span>
                <span className={`display ${styles.name}`}>{r.name}</span>
                {r.summary && <span className={styles.summary}>{r.summary}</span>}
              </span>
              <span className={styles.cell} data-label="Data as of">{r.dataDay ?? '—'}</span>
              <span className={`mono ${styles.cell}`} data-label="Created">{r.createdLabel}</span>
              <span className={`mono ${styles.cell}`} data-label="Last updated">
                {r.updatedLabel}
                {r.publishCount > 0 && <small> · v{r.publishCount}</small>}
              </span>
            </Link>
          ))}
        </section>
      ))}
      {!groups.length && <p className={styles.empty}>No sheet matches these filters.</p>}
    </div>
  );
}
