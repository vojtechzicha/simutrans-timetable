import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { repoFileUrl } from '@/lib/data';
import { listDocs, renderDoc } from '@/lib/docs';
import DocShell from '../doc-shell';

export function generateStaticParams() {
  return listDocs().map((d) => ({ path: d.id.split('/') }));
}

const idOf = (path: string[]) => path.map(decodeURIComponent).join('/');

export async function generateMetadata({ params }: PageProps<'/docs/[...path]'>): Promise<Metadata> {
  const id = idOf((await params).path);
  const d = listDocs().find((x) => x.id === id);
  return d ? { title: d.title, description: d.description ?? undefined } : {};
}

export default async function DocPage({ params }: PageProps<'/docs/[...path]'>) {
  const id = idOf((await params).path);
  const r = renderDoc(id);
  if (!r) notFound();
  return <DocShell current={id} html={r.html} description={r.doc.description} sourceUrl={repoFileUrl(r.doc.file)} file={r.doc.file} />;
}
