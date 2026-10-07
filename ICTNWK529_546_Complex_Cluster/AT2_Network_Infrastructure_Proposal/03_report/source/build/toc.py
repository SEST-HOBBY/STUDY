"""Two helpers for the report build.

  python3 -I toc.py pages  report.pdf  headings.json  pages.json
      finds the PDF page on which each heading starts (searching forward page by page)
  python3 -I toc.py inject report.docx pages.json     out.docx
      replaces the %%TOC%% placeholder paragraph with a real Word TOC field whose cached
      entries carry those page numbers (Word can refresh it with Update Field).
"""
import json, re, subprocess, sys, zipfile, shutil, os
from xml.sax.saxutils import escape


def norm(s):
    return re.sub(r'\s+', ' ', s).strip().lower()


def pages(pdf, headings_json, out_json):
    heads = json.load(open(headings_json))
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    texts = []
    for p in range(1, n + 1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-layout', pdf, '-'], capture_output=True, text=True).stdout
        texts.append([norm(l) for l in t.split('\n') if l.strip()])
    cur = 2  # skip cover (1) and contents (2)
    out = []
    for h in heads:
        key = norm(h['text'])[:45]
        found = None
        for p in range(cur, n):
            if any(l.startswith(key) for l in texts[p]):
                found = p + 1
                break
        if found is None:
            raise SystemExit(f'heading not found in PDF: {h["text"]}')
        cur = found - 1
        out.append({**h, 'page': found})
    json.dump(out, open(out_json, 'w'), indent=1)
    print(f'{len(out)} headings located over {n} pages')


def inject(docx, pages_json, out_docx):
    entries = json.load(open(pages_json))
    tmp = out_docx + '.dir'
    shutil.rmtree(tmp, ignore_errors=True)
    with zipfile.ZipFile(docx) as z:
        z.extractall(tmp)
        names = z.namelist()
    p = os.path.join(tmp, 'word', 'document.xml')
    xml = open(p, encoding='utf-8').read()
    m = re.search(r'<w:p\b(?:(?!<w:p\b).)*?%%TOC%%.*?</w:p>', xml, re.S)
    if not m:
        raise SystemExit('placeholder not found')
    paras = []
    for k, e in enumerate(entries):
        style = 'TOC1' if e['level'] == 1 else 'TOC2'
        runs = ''
        if k == 0:
            runs += ('<w:r><w:fldChar w:fldCharType="begin"/></w:r>'
                     '<w:r><w:instrText xml:space="preserve"> TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r>'
                     '<w:r><w:fldChar w:fldCharType="separate"/></w:r>')
        runs += f'<w:r><w:t xml:space="preserve">{escape(e["text"])}</w:t></w:r><w:r><w:tab/></w:r><w:r><w:t>{e["page"]}</w:t></w:r>'
        if k == len(entries) - 1:
            runs += '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
        paras.append(f'<w:p><w:pPr><w:pStyle w:val="{style}"/></w:pPr>{runs}</w:p>')
    xml = xml[:m.start()] + ''.join(paras) + xml[m.end():]
    open(p, 'w', encoding='utf-8').write(xml)
    if os.path.exists(out_docx):
        os.remove(out_docx)
    with zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED) as z:
        for n in names:  # keep the original member order ([Content_Types].xml first)
            z.write(os.path.join(tmp, n), n)
    shutil.rmtree(tmp)
    print(f'injected {len(entries)} TOC entries into {out_docx}')


if __name__ == '__main__':
    {'pages': pages, 'inject': inject}[sys.argv[1]](*sys.argv[2:])
