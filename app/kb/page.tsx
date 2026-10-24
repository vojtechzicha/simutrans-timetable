import type { Metadata } from 'next';
import { repoFileUrl } from '@/lib/data';
import { renderDoc } from '@/lib/docs';
import DocShell from '../docs/doc-shell';

export const metadata: Metadata = { title: 'Rules & knowledge base' };

export default function KbHome() {
  const r = renderDoc('kb/README')!;
  return <DocShell current="kb/README" html={r.html} description={null} sourceUrl={repoFileUrl(r.doc.file)} file={r.doc.file} />;
}
