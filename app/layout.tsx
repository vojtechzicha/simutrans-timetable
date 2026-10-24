import type { Metadata } from 'next';
import { Big_Shoulders, JetBrains_Mono, Public_Sans } from 'next/font/google';
import Link from 'next/link';
import './globals.css';

const display = Big_Shoulders({ variable: '--font-display', subsets: ['latin', 'latin-ext'], weight: ['600', '700', '800'] });
const body = Public_Sans({ variable: '--font-body', subsets: ['latin', 'latin-ext'] });
const mono = JetBrains_Mono({ variable: '--font-mono', subsets: ['latin', 'latin-ext'] });

export const metadata: Metadata = {
  title: { default: 'Simutrans Timetables', template: '%s · Simutrans Timetables' },
  description:
    'Every Simutrans timetable and fleet sheet for Czech trams, trolleybuses, buses and trains — with its sources, how it is kept in sync, and when it was made.',
};

export default function RootLayout({ children }: LayoutProps<'/'>) {
  return (
    <html lang="en" className={`${display.variable} ${body.variable} ${mono.variable}`}>
      <body>
        <header className="topbar">
          <Link href="/" className="brand">
            <b>Simutrans Timetables</b>
            <span>CZ · fork 122.0 · pak128 VZ</span>
          </Link>
          <nav>
            <Link href="/">Sheets</Link>
            <Link href="/timeline">Timeline</Link>
            <Link href="/kb">Rules &amp; KB</Link>
          </nav>
        </header>
        {children}
      </body>
    </html>
  );
}
