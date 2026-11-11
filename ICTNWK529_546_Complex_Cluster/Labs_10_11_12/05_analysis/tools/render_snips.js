// Render the raw terminal captures in reference_snips/raw/*.txt as PNG reference snips.
// Nothing is typed in by hand: the terminal text is the capture file, with carriage returns resolved the way a
// terminal would. The amber banner and the numbered notes are added so a reference snip cannot be mistaken
// for lab evidence. Usage: NODE_PATH=/opt/node-tools/node_modules node render_snips.js <raw dir> <out dir>
const fs = require('fs'), path = require('path'), { chromium } = require('playwright');
const [RAW, OUT] = process.argv.slice(2);

const SNIPS = [
  { out: 'lab10_ref1_test_traffic', files: ['lab10_01_test_traffic.txt'], lab: 'Lab 10',
    title: 'Test traffic that an IDS should alert on', env: 'curl against a local web server',
    marks: [[/^uid=0\(root\)/, 'The reply looks like the output of the id command run as root. The test in the Security Onion documentation (curl testmynids.org/uid/index.html) returns the same text.']] },
  { out: 'lab10_ref2_suricata_alert', files: ['lab10_02_suricata_alert.txt'], lab: 'Lab 10',
    title: 'Suricata raising the alert (the IDS engine inside Security Onion, run on its own)', env: 'Suricata 7.0.3 reading the captured packets',
    marks: [[/^alert ip any/, 'The rule. It fires on any packet that contains uid=0(root).'],
            [/\[\*\*\] \[1:2100498/, 'The alert: rule ID, rule name, classification, priority, then source IP:port -> destination IP:port. In Security Onion this is one row on the SOC Alerts page.']] },
  { out: 'lab10_ref3_alert_detail', files: ['lab10_03_alert_detail_eve_json.txt'], lab: 'Lab 10',
    title: 'The same alert in detail (eve.json, the record Security Onion stores and searches)', env: 'Suricata 7.0.3 eve.json',
    marks: [[/"src_ip"/, 'Source and destination address and port: who sent the suspicious packet to whom.'],
            [/"signature":/, 'Rule name, category and severity. These are the fields SOC shows when an alert is drilled into.']] },
  { out: 'lab11_ref1_server_running', files: ['lab11_01_server_running.txt'], lab: 'Lab 11',
    title: 'FTP server installed and running', env: 'vsftpd 3.0.5 on Ubuntu 24.04',
    marks: [[/^vsftpd: version/, 'The FTP server software and its version.'],
            [/^\d+ \/usr\/sbin\/vsftpd/, 'The server process is running.'],
            [/^LISTEN.*:21 /, 'It is listening on TCP port 21 (the FTP control port) on every address.']] },
  { out: 'lab11_ref2_user_and_folder', files: ['lab11_02_user_and_folder.txt'], lab: 'Lab 11',
    title: 'FTP user and shared folder configured', env: 'vsftpd 3.0.5 on Ubuntu 24.04',
    marks: [[/^local_enable=YES/, 'Local user accounts may log in; anonymous logins are off (line above).'],
            [/^write_enable=YES/, 'Uploads are allowed.'],
            [/^pasv_min_port/, 'The passive-mode data port range. This range has to be open on the server firewall.'],
            [/^ftpuser1:x:/, 'The FTP user and its home folder, which is the folder the user sees after login.']] },
  { out: 'lab11_ref3_client_session', files: ['lab11_03_client_session.txt'], lab: 'Lab 11',
    title: 'Client logs in, lists the folder, uploads one file and downloads one file', env: 'ftp client against vsftpd 3.0.5',
    marks: [[/^220 /, 'Control connection to port 21 is open; the server sends its banner.'],
            [/^230 /, 'Login accepted.'],
            [/^229 /, 'Passive mode: the server names a data port (50000 to 50100 here) and the client connects to it.'],
            [/^ftp> put/, 'Upload (the client sends STOR).'],
            [/^ftp> get/, 'Download (the client sends RETR).'],
            [/upload_from_client\.txt$/, 'The second listing shows the uploaded file now on the server.', 'last']] },
  { out: 'lab11_ref4_transfer_proof_and_log', files: ['lab11_04_transfer_proof_and_server_log.txt'], lab: 'Lab 11',
    title: 'Proof of the transfers on both sides, and the server log of the session', env: 'vsftpd 3.0.5 log',
    marks: [[/OK LOGIN/, 'Server log: the login.'], [/OK UPLOAD/, 'Server log: the upload, with file name and size.'],
            [/OK DOWNLOAD/, 'Server log: the download.']] },
  { out: 'lab11_ref5_clear_text_login', files: ['lab11_05_packet_capture_clear_text_login.txt'], lab: 'Lab 11',
    title: 'Packet capture of the login: FTP sends the password in clear text', env: 'tcpdump on the FTP control connection',
    marks: [[/FTP: USER/, 'The user name crosses the network unencrypted.'],
            [/FTP: PASS/, 'So does the password. This is the weakness of plain FTP and the reason for FTPS and SFTP. In Wireshark the display filter is ftp.']] },
  { out: 'lab12_ref1_server_running', files: ['lab12_01_server_running.txt'], lab: 'Lab 12',
    title: 'Mail server running with its domain and two mailboxes', env: 'Postfix 3.8 and Dovecot 2.3 on Ubuntu 24.04',
    marks: [[/^mydomain = /, 'The mail domain the server accepts mail for.'],
            [/^user1:/, 'The two mailboxes (user1@lab.local and user2@lab.local).'],
            [/:110 /, 'POP3 listening on 110 (retrieve mail).'], [/:25 /, 'SMTP listening on 25 (send and receive mail).'],
            [/:143 /, 'IMAP listening on 143 (retrieve mail).']] },
  { out: 'lab12_ref2_smtp_send', files: ['lab12_02_smtp_send_user1_to_user2.txt'], lab: 'Lab 12',
    title: 'user1 sends a message to user2 over SMTP', env: 'swaks SMTP test client against Postfix',
    marks: [[/^<-  220 /, 'The server answers on port 25 with its banner.'],
            [/MAIL FROM:/, 'Sender.'], [/RCPT TO:/, 'Recipient. A 250 reply means the server accepts mail for this mailbox.'],
            [/250 2\.0\.0 Ok: queued/, 'The server has accepted the message for delivery.']] },
  { out: 'lab12_ref3_imap_receive', files: ['lab12_03_imap_user2_receives.txt'], lab: 'Lab 12',
    title: 'user2 logs in over IMAP and reads the message', env: 'telnet to Dovecot IMAP, port 143',
    marks: [[/^a1 OK/, 'user2 is authenticated.'], [/^\* 1 EXISTS/, 'One message in the Inbox.'],
            [/^Subject: Lab 12 test message/, 'The message that user1 sent: From, To, Subject and the body below.']] },
  { out: 'lab12_ref4_reply_pop3_receive', files: ['lab12_04a_reply_sent.txt', 'lab12_04b_pop3_user1_receives_reply.txt'], lab: 'Lab 12',
    title: 'user2 replies, and user1 collects the reply over POP3', env: 'swaks, then telnet to Dovecot POP3, port 110',
    marks: [[/^swaks exit code: 0/, 'The reply was accepted by the server.'], [/^\+OK Logged in/, 'user1 is authenticated.'],
            [/^\+OK 1 messages/, 'One message waiting.'], [/^Subject: RE:/, 'The reply from user2, with the full headers showing the route it took.']] },
  { out: 'lab12_ref5_server_logs', files: ['lab12_05_server_logs.txt'], lab: 'Lab 12',
    title: 'Mail server logs for both deliveries and both mailbox logins', env: 'Postfix and Dovecot logs',
    marks: [[/to=<user2@lab\.local>.*status=sent/, 'First message delivered to user2\'s mailbox.'],
            [/to=<user1@lab\.local>.*status=sent/, 'Reply delivered to user1\'s mailbox.'],
            [/imap-login/, 'user2\'s IMAP login.'], [/pop3-login/, 'user1\'s POP3 login.']] },
];

const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function lines(file) {            // resolve \r the way a terminal does: the last rewrite of a line wins
  return fs.readFileSync(path.join(RAW, file), 'utf8').replace(/\r\n/g, '\n').split('\n')
    .map(l => { const p = l.split('\r').filter(x => x.length); return p.length ? p[p.length - 1] : ''; });
}
function html(s) {
  let ls = []; s.files.forEach(f => { ls = ls.concat(lines(f)); });
  while (ls.length && ls[ls.length - 1] === '') ls.pop();
  const tag = new Array(ls.length).fill(0);
  s.marks.forEach(([re, , which], i) => {
    let idx = -1; ls.forEach((l, n) => { if (re.test(l) && (which === 'last' || idx < 0)) idx = n; });
    if (idx < 0) throw new Error(`${s.out}: no line matches ${re}`);
    if (tag[idx]) throw new Error(`${s.out}: line already marked: ${ls[idx]}`);
    tag[idx] = i + 1;
  });
  const body = ls.map((l, n) => {
    const cmd = /^root@vm:[^#]*# /.test(l);
    const t = cmd ? l.replace(/^(root@vm:[^#]*# )(.*)$/, (m, a, b) => `<span class="ps">${esc(a)}</span><span class="cmd">${esc(b)}</span>`) : esc(l);
    return `<div class="ln${tag[n] ? ' hit' : ''}"><span class="gut">${tag[n] ? `<b>${tag[n]}</b>` : ''}</span><span class="tx">${t || ' '}</span></div>`;
  }).join('');
  const notes = s.marks.map(([, note], i) => `<li><b>${i + 1}</b><span>${esc(note)}</span></li>`).join('');
  return `<!doctype html><meta charset="utf-8"><style>
  body{margin:0;background:#fff;font-family:"DejaVu Sans",Arial,sans-serif}
  #snip{width:1240px;padding:14px;background:#fff}
  .banner{background:#ffe08a;border:2px solid #b97a00;color:#3d2a00;padding:8px 12px;font-size:14px;border-radius:6px 6px 0 0}
  .banner b{letter-spacing:.5px}
  .title{background:#333a45;color:#fff;padding:8px 12px;font-size:15px}
  .title small{color:#b9c2cf;font-size:12px;margin-left:10px}
  .term{background:#16181d;color:#d7dae0;font:13px/1.45 "DejaVu Sans Mono",monospace;padding:10px 0}
  .ln{display:flex}.gut{flex:0 0 34px;text-align:center}
  .gut b{display:inline-block;min-width:18px;height:18px;line-height:18px;border-radius:9px;background:#ffcf40;color:#1a1300;font:bold 11px "DejaVu Sans",sans-serif}
  .tx{flex:1;white-space:pre-wrap;word-break:break-all;padding-right:12px}
  .hit{background:#3b3414}.ps{color:#7fd67f}.cmd{color:#fff;font-weight:bold}
  ol{list-style:none;margin:0;padding:10px 12px;border:1px solid #c9ced6;border-top:0;border-radius:0 0 6px 6px;font-size:13.5px;color:#1f2430;background:#f5f6f8}
  li{display:flex;gap:8px;margin:4px 0}
  li b{flex:0 0 18px;height:18px;line-height:18px;text-align:center;border-radius:9px;background:#ffcf40;font-size:11px}
  </style><div id="snip">
  <div class="banner"><b>REFERENCE EXAMPLE</b> &nbsp;${s.lab}. A real run captured on 11 Nov 2026 on a Linux test machine (${esc(s.env)}). It shows what to look for. It is not my lab evidence: my own snip goes in the results document.</div>
  <div class="title">${esc(s.title)}</div>
  <div class="term">${body}</div><ol>${notes}</ol></div>`;
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  const b = await chromium.launch(); const ctx = await b.newContext({ deviceScaleFactor: 2, viewport: { width: 1300, height: 900 } });
  const p = await ctx.newPage();
  for (const s of SNIPS) {
    await p.setContent(html(s)); await p.locator('#snip').screenshot({ path: path.join(OUT, s.out + '.png') });
    console.log('wrote', s.out + '.png');
  }
  await b.close();
})();
