// Builds the HelpYou AT2 report (.docx) from the section markdown files.
// Usage: node build_docx.js <sectionsDir> <printFiguresDir> <out.docx>
// Markdown subset: # / ## / ### headings, paragraphs (lines in one block joined by line breaks),
// pipe tables, ![alt](figures/x.png) images, *Figure/Table captions*, **bold**, *italic*,
// [text](url) links, backslash escapes.
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, ExternalHyperlink, HeadingLevel, AlignmentType,
  Table, TableRow, TableCell, WidthType, ShadingType, BorderStyle, ImageRun, Header, Footer,
  PageNumber, PageOrientation, SectionType, TabStopType, TabStopPosition, VerticalAlign, LineRuleType,
} = require('docx');

const [,, SECTIONS_DIR, FIG_DIR, OUT] = process.argv;
const ORDER = ['S0_cover_summary', 'S1_gap_analysis', 'S2_logical_topology', 'S3_S4_physical_racks',
  'S5_ip_scheme', 'S6a_investment_1_5', 'S6b_investment_6_10', 'S7_bandwidth', 'S8_bibliography'];
const FIG_MAP = {
  'fig1_packet_tracer_physical_view.png': ['fig1_packet_tracer_physical_view.png', 'png'],
  'fig1b_physical_layout_render.png': ['fig1b_physical_layout_render.jpg', 'jpg'],
  'fig2_logical_topology.png': ['fig2_logical_topology.png', 'png'],
  'fig3_rack_diagram.png': ['fig3_rack_diagram.png', 'png'],
};

const FONT = 'Calibri';
const A4W = 11906, A4H = 16838, MARGIN = 1440;
const PORTRAIT_TW = A4W - 2 * MARGIN;   // 9026 twips
const LANDSCAPE_TW = A4H - 2 * MARGIN;  // 13958 twips
const BLUE = '1F3864', GREY = '595959', HEAD_FILL = 'D9E2F3', ZEBRA = 'F5F7FB';

// ---------- image size helpers ----------
function pngSize(buf) { return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) }; }
function jpgSize(buf) {
  let i = 2;
  while (i < buf.length) {
    if (buf[i] !== 0xFF) { i++; continue; }
    const marker = buf[i + 1];
    const len = buf.readUInt16BE(i + 2);
    if (marker >= 0xC0 && marker <= 0xCF && ![0xC4, 0xC8, 0xCC].includes(marker)) {
      return { h: buf.readUInt16BE(i + 5), w: buf.readUInt16BE(i + 7) };
    }
    i += 2 + len;
  }
  throw new Error('jpeg size not found');
}
const twipToPx = t => t / 1440 * 96;
const cmToPx = cm => cm / 2.54 * 96;

// ---------- inline markdown ----------
function inline(text, base = {}) {
  text = text.replace(/ <-> /g, ' ↔ ').replace(/ -> /g, ' → ');
  const runs = [];
  let buf = '', bold = false, ital = false, i = 0;
  const flush = () => { if (buf) { runs.push(new TextRun({ text: buf, bold: bold || base.bold, italics: ital || base.italics, size: base.size, color: base.color, font: FONT })); buf = ''; } };
  while (i < text.length) {
    const c = text[i];
    if (c === '\\' && i + 1 < text.length && '\\`*_{}[]()#+-.!|$'.includes(text[i + 1])) { buf += text[i + 1]; i += 2; continue; }
    if (text.startsWith('**', i)) { flush(); bold = !bold; i += 2; continue; }
    if (c === '*') { flush(); ital = !ital; i += 1; continue; }
    if (c === '[') {
      const m = /^\[([^\]]+)\]\((https?:\/\/[^)\s]+)\)/.exec(text.slice(i));
      if (m) {
        flush();
        runs.push(new ExternalHyperlink({ link: m[2], children: [new TextRun({ text: m[1], style: 'Hyperlink', size: base.size, font: FONT, bold: bold || base.bold })] }));
        i += m[0].length; continue;
      }
    }
    buf += c; i++;
  }
  flush();
  return runs;
}

// ---------- parse sections into blocks ----------
function parse(md) {
  const lines = md.replace(/\r/g, '').split('\n');
  const blocks = [];
  let i = 0;
  while (i < lines.length) {
    const l = lines[i];
    if (!l.trim()) { i++; continue; }
    let m;
    if ((m = /^(#{1,3}) (.*)$/.exec(l))) { blocks.push({ t: 'h', level: m[1].length, text: m[2].trim() }); i++; continue; }
    if ((m = /^!\[([^\]]*)\]\(([^)]+)\)\s*$/.exec(l))) { blocks.push({ t: 'img', alt: m[1], src: m[2] }); i++; continue; }
    if (/^\*(Figure|Table) [0-9]+b?\./.test(l) && l.trim().endsWith('*')) { blocks.push({ t: 'cap', text: l.trim().slice(1, -1) }); i++; continue; }
    if (l.startsWith('|')) {
      const rows = [];
      while (i < lines.length && lines[i].startsWith('|')) { rows.push(lines[i]); i++; }
      const cells = rows.filter(r => !/^\|\s*:?-{3,}/.test(r)).map(r => splitRow(r));
      blocks.push({ t: 'table', header: cells[0], rows: cells.slice(1) });
      continue;
    }
    const para = [];
    while (i < lines.length && lines[i].trim() && !/^(#{1,3} |\||!\[)/.test(lines[i])) { para.push(lines[i]); i++; }
    blocks.push({ t: 'p', lines: para });
  }
  return blocks;
}
function splitRow(r) {
  const s = r.trim().replace(/^\|/, '').replace(/\|$/, '');
  const out = []; let cur = '';
  for (let i = 0; i < s.length; i++) {
    if (s[i] === '\\' && s[i + 1] === '|') { cur += '\\|'; i++; continue; }
    if (s[i] === '|') { out.push(cur.trim()); cur = ''; continue; }
    cur += s[i];
  }
  out.push(cur.trim());
  return out;
}

// ---------- block renderers ----------
const HEADINGS = { 1: HeadingLevel.HEADING_1, 2: HeadingLevel.HEADING_2, 3: HeadingLevel.HEADING_3 };
function heading(b) { return new Paragraph({ heading: HEADINGS[b.level], keepNext: true, keepLines: true, children: inline(b.text) }); }
function para(b) {
  const children = [];
  b.lines.forEach((ln, k) => {
    const runs = inline(ln);
    if (k > 0) children.push(new TextRun({ break: 1, text: '' }));
    children.push(...runs);
  });
  const isBib = /^\[(P|R)\d+\]/.test(b.lines[0]);
  return new Paragraph({ children, spacing: isBib ? { after: 100 } : undefined, keepLines: isBib });
}
function caption(b) {
  return new Paragraph({ style: 'Caption', children: inline(b.text) });
}
function image(b, availTw, maxHeightCm) {
  const name = path.basename(b.src);
  const [file, type] = FIG_MAP[name] || [name, name.endsWith('.jpg') ? 'jpg' : 'png'];
  const data = fs.readFileSync(path.join(FIG_DIR, file));
  const sz = type === 'png' ? pngSize(data) : jpgSize(data);
  let w = twipToPx(availTw);
  if (name.startsWith('fig1_')) w = Math.min(w, cmToPx(11.5));
  let h = w * sz.h / sz.w;
  const maxH = cmToPx(maxHeightCm);
  if (h > maxH) { h = maxH; w = h * sz.w / sz.h; }
  return new Paragraph({ alignment: AlignmentType.CENTER, keepNext: true, spacing: { before: 60, after: 60, line: 240, lineRule: LineRuleType.AUTO },
    children: [new ImageRun({ type, data, transformation: { width: Math.round(w), height: Math.round(h) }, altText: { title: b.alt, description: b.alt, name: b.alt } })] });
}
function table(b, availTw, opts = {}) {
  const ncol = b.header.length;
  const all = [b.header, ...b.rows];
  const plainLen = s => s.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1').replace(/\*\*/g, '').length;
  const weights = [];
  for (let c = 0; c < ncol; c++) {
    const lens = all.map(r => plainLen(r[c] || ''));
    const avg = lens.reduce((a, x) => a + x, 0) / lens.length;
    const mx = Math.max(...lens);
    weights.push(Math.max(7, Math.min(70, 0.6 * avg + 0.15 * mx)));
  }
  if (opts.colWeights) opts.colWeights.forEach((w, k) => { weights[k] = w; });
  const tot = weights.reduce((a, x) => a + x, 0);
  let widths = weights.map(w => Math.max(900, Math.round(availTw * w / tot)));
  const diff = availTw - widths.reduce((a, x) => a + x, 0);
  widths[widths.indexOf(Math.max(...widths))] += diff;
  const size = opts.size || 18;
  const border = { style: BorderStyle.SINGLE, size: 4, color: 'A6A6A6' };
  const borders = { top: border, bottom: border, left: border, right: border };
  const mkCell = (txt, c, isHead, zebra) => new TableCell({
    width: { size: widths[c], type: WidthType.DXA }, borders,
    shading: isHead ? { fill: HEAD_FILL, type: ShadingType.CLEAR, color: 'auto' } : (zebra ? { fill: ZEBRA, type: ShadingType.CLEAR, color: 'auto' } : undefined),
    margins: { top: 50, bottom: 50, left: 90, right: 90 }, verticalAlign: VerticalAlign.TOP,
    children: [new Paragraph({ spacing: { before: 0, after: 0, line: 252, lineRule: LineRuleType.AUTO }, children: inline(txt || '', { size, bold: isHead }) })],
  });
  const rows = [new TableRow({ tableHeader: true, cantSplit: true, children: b.header.map((h, c) => mkCell(h, c, true)) })];
  b.rows.forEach((r, k) => {
    const long = r.join(' ').length > 700;
    const isTotal = /^(Hardware subtotal|Software and licences subtotal|Services and labour subtotal|Initial procurement|Contingency|Year-one operating total|First-year funding requirement)/.test(r[0] || '');
    rows.push(new TableRow({ cantSplit: !long, children: r.map((x, c) => mkCell(isTotal ? `**${x}**` : x, c, false, k % 2 === 1)) }));
  });
  return new Table({ width: { size: availTw, type: WidthType.DXA }, columnWidths: widths, rows });
}

// ---------- assemble ----------
const sections = ORDER.map(n => ({ name: n, blocks: parse(fs.readFileSync(path.join(SECTIONS_DIR, n + '.md'), 'utf8')) }));

// cover = S0 blocks before first heading
const s0 = sections[0].blocks;
const firstH = s0.findIndex(b => b.t === 'h');
const coverLines = s0.slice(0, firstH).map(b => b.lines.join(' '));
sections[0].blocks = s0.slice(firstH);

// flatten and mark landscape runs
let flat = [];
sections.forEach(s => s.blocks.forEach(b => flat.push({ ...b, sec: s.name })));
const isWideImg = b => b.t === 'img' && /fig2_|fig3_/.test(b.src);
const isGapTable = b => b.t === 'table' && /^Current/.test(b.header[0]) && b.header.length === 3;
flat.forEach(b => { b.land = false; });
for (let k = 0; k < flat.length; k++) {
  const b = flat[k];
  if (!(isWideImg(b) || isGapTable(b))) continue;
  b.land = true;
  // pull the lead-in paragraph (and a heading right before it) onto the landscape page
  let j = k - 1;
  if (flat[j] && flat[j].t === 'p') { flat[j].land = true; j--; if (flat[j] && flat[j].t === 'h') { flat[j].land = true; } }
  // caption after it
  if (flat[k + 1] && flat[k + 1].t === 'cap') flat[k + 1].land = true;
  // for the gap table, the closing paragraph too
  if (isGapTable(b) && flat[k + 2] && flat[k + 2].t === 'p') flat[k + 2].land = true;
}

// group into orientation runs
const runs = [];
flat.forEach(b => {
  const last = runs[runs.length - 1];
  if (last && last.land === b.land) last.blocks.push(b); else runs.push({ land: b.land, blocks: [b] });
});

const makeHeaderChildren = land => [
  new Paragraph({ border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: 'A6A6A6', space: 2 } }, spacing: { after: 0 },
    tabStops: [{ type: TabStopType.RIGHT, position: land ? LANDSCAPE_TW : PORTRAIT_TW }],
    children: [
      new TextRun({ text: 'HelpYou Mortgage Network Infrastructure Proposal | ICTNWK529 / ICTNWK546 AT2', size: 16, color: GREY, font: FONT }),
      new TextRun({ text: '\t7 October 2026', size: 16, color: GREY, font: FONT }),
    ] }),
  new Paragraph({ spacing: { after: 0 }, children: [new TextRun({ text: 'Prepared by Roly Lobley | Submitted to the Chief Information Officer, HelpYou Mortgage', size: 16, color: GREY, font: FONT })] }),
];
const makeHeader = land => new Header({ children: makeHeaderChildren(land) });
const makeFooter = () => new Footer({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [new TextRun({ children: ['Page ', PageNumber.CURRENT], size: 18, color: GREY, font: FONT })] })] });

function renderBlocks(blocks, land) {
  const tw = land ? LANDSCAPE_TW : PORTRAIT_TW;
  const out = [];
  blocks.forEach(b => {
    if (b.t === 'h') out.push(heading(b));
    else if (b.t === 'p') out.push(para(b));
    else if (b.t === 'cap') out.push(caption(b));
    else if (b.t === 'img') {
      let maxH = land ? 13.6 : 22.5;
      if (/fig3_/.test(b.src)) maxH = 11.5;      // section 4 heading + intro share the page
      if (/fig1_/.test(b.src)) maxH = 15.5;
      out.push(image(b, tw, maxH));
    } else if (b.t === 'table') {
      const gap = isGapTable(b);
      out.push(table(b, tw, gap ? { size: 17, colWeights: [30, 42, 28] } : {}));
      out.push(new Paragraph({ spacing: { after: 0 }, children: [] }));
    }
  });
  return out;
}

const pagePortrait = { size: { width: A4W, height: A4H }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN, header: 600, footer: 600 } };
const pageLandscape = { size: { width: A4W, height: A4H, orientation: PageOrientation.LANDSCAPE }, margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN, header: 600, footer: 600 } };

// cover
const cover = [];
cover.push(new Paragraph({ spacing: { before: 2400, after: 120 }, children: [new TextRun({ text: coverLines[0], size: 24, color: GREY, font: FONT })] }));
cover.push(new Paragraph({ spacing: { after: 120 }, children: [new TextRun({ text: coverLines[1], size: 24, color: GREY, font: FONT })] }));
cover.push(new Paragraph({ spacing: { after: 1200 }, children: inline(coverLines[2], { size: 24, color: GREY }) }));
cover.push(new Paragraph({ spacing: { after: 240 }, border: { bottom: { style: BorderStyle.SINGLE, size: 12, color: BLUE, space: 8 } },
  children: [new TextRun({ text: coverLines[3].replace(/\*\*/g, ''), bold: true, size: 52, color: BLUE, font: FONT })] }));
cover.push(new Paragraph({ spacing: { after: 1600 }, children: [new TextRun({ text: 'Network design, costing and five-year capacity plan for the Brisbane head office and Cairns branch', size: 26, color: GREY, font: FONT })] }));
coverLines.slice(4).forEach(l => cover.push(new Paragraph({ spacing: { after: 100 }, children: [new TextRun({ text: l, size: 24, font: FONT })] })));

const docSections = [{ properties: { page: pagePortrait }, children: cover }];
runs.forEach((r, k) => {
  const children = [];
  if (k === 0) {
    children.push(new Paragraph({ style: 'ContentsTitle', children: [new TextRun({ text: 'Contents', font: FONT })] }));
    children.push(new Paragraph({ children: [new TextRun({ text: '%%TOC%%', font: FONT })] }));
    children.push(new Paragraph({ pageBreakBefore: true, spacing: { after: 0 }, children: [] }));
  }
  children.push(...renderBlocks(r.blocks, r.land));
  docSections.push({
    properties: { type: SectionType.NEXT_PAGE, page: r.land ? pageLandscape : pagePortrait },
    headers: { default: makeHeader(r.land) }, footers: { default: makeFooter() }, children,
  });
});

const doc = new Document({
  creator: 'Roly Lobley', title: 'HelpYou Mortgage Network Infrastructure Proposal',
  subject: 'ICTNWK529 / ICTNWK546 Assessment Task 2', description: 'Network Infrastructure Proposal',
  styles: {
    default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { after: 120, line: 264, lineRule: LineRuleType.AUTO } } } },
    paragraphStyles: [
      { id: 'Heading1', name: 'Heading 1', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 32, bold: true, color: BLUE }, paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0, keepNext: true } },
      { id: 'Heading2', name: 'Heading 2', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 26, bold: true, color: BLUE }, paragraph: { spacing: { before: 240, after: 100 }, outlineLevel: 1, keepNext: true } },
      { id: 'Heading3', name: 'Heading 3', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 23, bold: true, color: '2F5496' }, paragraph: { spacing: { before: 200, after: 80 }, outlineLevel: 2, keepNext: true } },
      { id: 'Caption', name: 'caption', basedOn: 'Normal', next: 'Normal', quickFormat: true,
        run: { font: FONT, size: 18, italics: true, color: GREY }, paragraph: { spacing: { before: 60, after: 200 } } },
      { id: 'ContentsTitle', name: 'Contents Title', basedOn: 'Normal', next: 'Normal',
        run: { font: FONT, size: 32, bold: true, color: BLUE }, paragraph: { spacing: { after: 240 } } },
      { id: 'TOC1', name: 'toc 1', basedOn: 'Normal', next: 'Normal',
        run: { font: FONT, size: 21, bold: true }, paragraph: { spacing: { before: 100, after: 20 }, tabStops: [{ type: TabStopType.RIGHT, position: PORTRAIT_TW, leader: 'dot' }] } },
      { id: 'TOC2', name: 'toc 2', basedOn: 'Normal', next: 'Normal',
        run: { font: FONT, size: 20 }, paragraph: { spacing: { before: 0, after: 20 }, indent: { left: 360 }, tabStops: [{ type: TabStopType.RIGHT, position: PORTRAIT_TW, leader: 'dot' }] } },
    ],
    characterStyles: [
      { id: 'Hyperlink', name: 'Hyperlink', basedOn: 'DefaultParagraphFont', run: { color: '0563C1', underline: { type: 'single' } } },
    ],
  },
  sections: docSections,
});

Packer.toBuffer(doc).then(buf => {
  fs.writeFileSync(OUT, buf);
  const headingsOut = flat.filter(b => b.t === 'h' && b.level <= 2).map(b => ({ level: b.level, text: b.text.replace(/\\(.)/g, '$1') }));
  fs.writeFileSync(OUT.replace(/\.docx$/, '.headings.json'), JSON.stringify(headingsOut, null, 1));
  console.log('wrote', OUT, buf.length, 'bytes;', runs.length, 'body sections (', runs.filter(r => r.land).length, 'landscape )');
});
