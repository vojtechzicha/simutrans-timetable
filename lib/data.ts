import sheetsJson from '@/data/sheets.json';

export type Mode = 'tram' | 'trolleybus' | 'bus' | 'metro' | 'rail' | 'ferry';
export type Status = 'active' | 'archived' | 'reference' | 'superseded';

export interface Source {
  name: string;
  url?: string | null;
  role?: string;
  note?: string;
}

export interface Sheet {
  slug: string;
  file: string;
  location: 'root' | 'archive';
  title: string | null;
  bytes: number;
  sha256: string;
  sourceModified: string;
  contentChangedAt: string;
  syncedAt: string;
  history: {
    firstSeen: string | null;
    firstPublished: string | null;
    lastPublished: string | null;
    publishCount: number;
    latestVersion: number | null;
    artifactUrls: string[];
    sessions: string[];
  } | null;
  // from data/catalog.json
  name?: string;
  status?: Status;
  modes?: Mode[];
  region?: string;
  kind?: string;
  summary?: string;
  pipeline?: string | null;
  build?: string | null;
  fetch?: string | null;
  sources?: Source[];
  vehicleDay?: string | null;
  networkDate?: string | null;
  created?: string | null;
  createdNote?: string | null;
  artifactUrl?: string | null;
  builtBy?: string | null;
  sync?: string;
  updateRecipe?: string[];
  refreshTriggers?: string[];
  notes?: string;
  counts?: string | null;
  kbNotes?: string[];
  previousFiles?: string[];
  supersededBy?: string | null;
  dependsOn?: string[];
  rawSnapshots?: string[];
  lastUpdated?: string | null;
}

const data = sheetsJson as unknown as { source: string; syncedAt: string; sheets: Sheet[] };

export const sheets: Sheet[] = data.sheets;
export const syncedAt = data.syncedAt;
export const sourceFolder = data.source;

export const getSheet = (slug: string) => sheets.find((s) => s.slug === slug);

export const sheetName = (s: Sheet) => s.name ?? s.title ?? s.file.replace(/\.html$/, '');

/** When the sheet first existed: explicit catalogue date, else the first time a session wrote or published it. */
export const createdAt = (s: Sheet) => s.created ?? s.history?.firstSeen ?? null;
/** Catalogue date if set, else the last artifact publish, else the file's own modification time. */
export const updatedAt = (s: Sheet) => s.lastUpdated ?? s.history?.lastPublished ?? s.sourceModified;

const DAY_RE = /(?:(Mon|Tue|Wed|Thu|Fri|Sat|Sun)\w*\s+)?(\d{1,2})\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\w*(?:\s+(\d{4}))?/;
/** First date in a free-text day description, e.g. "Fri 25 Sep 2026 (fill-ins …)" → "Fri 25 Sep". */
export function shortDay(text: string | null | undefined) {
  if (!text) return null;
  const m = DAY_RE.exec(text);
  return m ? [m[1], m[2], m[3]].filter(Boolean).join(' ') : text.length > 24 ? null : text;
}
export const artifactUrl = (s: Sheet) => s.artifactUrl ?? s.history?.artifactUrls.at(-1) ?? null;

export const REGION_ORDER = [
  'Praha',
  'Brno',
  'Plzeň',
  'Olomouc',
  'Ostrava',
  'Havířov · Karviná · Orlová',
  'ODIS regional',
  'Most · Litvínov',
  'Pardubice',
  'Rail — Prague region',
  'Rail — long distance',
];

export const MODE_LABEL: Record<Mode, string> = {
  tram: 'Tram',
  trolleybus: 'Trolleybus',
  bus: 'Bus',
  metro: 'Metro',
  rail: 'Rail',
  ferry: 'Ferry',
};

export const STATUS_LABEL: Record<Status, string> = {
  active: 'Active',
  archived: 'Archived',
  reference: 'Reference',
  superseded: 'Superseded',
};

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
export function fmtDate(iso: string | null | undefined, withTime = false) {
  if (!iso) return '—';
  const m = /^(\d{4})-(\d{2})-(\d{2})(?:T(\d{2}):(\d{2}))?/.exec(iso);
  if (!m) return iso;
  const d = `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
  return withTime && m[4] ? `${d}, ${m[4]}:${m[5]} UTC` : d;
}

export const REPO_URL = 'https://github.com/vojtechzicha/simutrans-timetable';
export const repoFileUrl = (p: string) => `${REPO_URL}/blob/main/${p.split('/').map(encodeURIComponent).join('/')}`;
