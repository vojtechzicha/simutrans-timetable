'use client';

import { useState } from 'react';
import styles from './sheet.module.css';

/** The sheet itself, untouched, in its own document so its styles and scripts stay its own. */
export default function Frame({ src, title }: { src: string; title: string }) {
  const [wide, setWide] = useState(false);
  return (
    <section className={`${styles.frameWrap} ${wide ? styles.wide : ''}`}>
      <div className={styles.frameBar}>
        <span className="mono">{src}</span>
        <span className={styles.frameActions}>
          <button onClick={() => setWide((w) => !w)}>{wide ? 'Show details' : 'Full width'}</button>
          <a href={src} target="_blank" rel="noreferrer">Open sheet ↗</a>
        </span>
      </div>
      <iframe src={src} title={title} className={styles.frame} />
    </section>
  );
}
