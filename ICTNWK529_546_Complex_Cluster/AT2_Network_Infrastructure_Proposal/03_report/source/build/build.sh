#!/bin/bash
# Rebuild the report: docx -> pdf -> heading pages -> TOC injection -> pdf -> verify TOC pages.
set -euo pipefail
B="$(cd "$(dirname "$0")" && pwd)"; W="${W:-$(dirname "$B")}"  # W holds sections/; B needs print/ with print-size figures
export NODE_PATH="/opt/node-tools/node_modules:/usr/local/lib/node_modules_global"
cd "$B"
node build_docx.js "$W/sections" "$B/print" "$B/pass1.docx"
soffice --headless --convert-to pdf --outdir "$B" "$B/pass1.docx" >/dev/null 2>&1
python3 -I toc.py pages pass1.pdf pass1.headings.json pages.json
python3 -I toc.py inject pass1.docx pages.json final.docx
soffice --headless --convert-to pdf --outdir "$B" "$B/final.docx" >/dev/null 2>&1
cp pass1.headings.json final.headings.json
python3 -I toc.py pages final.pdf final.headings.json pages_check.json
python3 -I -c "
import json;a=json.load(open('pages.json'));b=json.load(open('pages_check.json'))
assert [x['page'] for x in a]==[x['page'] for x in b], 'TOC page numbers drifted'
print('TOC verified;', len(a), 'entries')"
pdfinfo final.pdf | grep Pages
