#!/usr/bin/env python3
"""Lab 11 reference run: drive a real interactive ftp client session against the vsftpd server started by
ftp_reference_setup.sh and save exactly what the terminal showed. Usage: ftp_reference_capture.py <server-ip> <outdir>"""
import os, subprocess, sys, pexpect

ip, out = sys.argv[1], sys.argv[2]
os.makedirs(out, exist_ok=True)
PS = "root@vm:~# "

def shell(cmds, name):
    lines = []
    for c in cmds:
        r = subprocess.run(c, shell=True, capture_output=True, text=True)
        lines.append(PS + c)
        lines.append((r.stdout + r.stderr).rstrip("\n"))
    open(os.path.join(out, name), "w").write("\n".join(lines) + "\n")

shell(["vsftpd -v 2>&1 0>&1", "pgrep -a vsftpd | grep -v defunct", "ss -tlnp | grep ':21 '"],
      "lab11_01_server_running.txt")
shell(["grep -v '^#' /etc/vsftpd.conf", "getent passwd ftpuser1", "ls -l /srv/ftp/ftpuser1"],
      "lab11_02_user_and_folder.txt")

work = "/tmp/ftpclient"; os.makedirs(work, exist_ok=True)
open(os.path.join(work, "upload_from_client.txt"), "w").write("Lab 11 test file uploaded from the FTP client\n")
for f in ("readme_server.txt",):
    p = os.path.join(work, f)
    if os.path.exists(p): os.remove(p)

cap = subprocess.Popen(["tcpdump", "-i", "lo", "-U", "-w", "/tmp/ftpclient/ftp.pcap", "tcp port 21"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
import time; time.sleep(2)
log = open(os.path.join(out, "lab11_03_client_session.txt"), "w")
log.write(f"root@vm:/tmp/ftpclient# ftp {ip}\n")
c = pexpect.spawn("ftp", [ip], cwd=work, encoding="utf-8", timeout=20, dimensions=(50, 110))
c.logfile_read = log
c.expect("Name .*: "); c.sendline("ftpuser1")
c.expect("Password:"); c.sendline("Lab11-Pass!")
for cmd in ("pwd", "ls", "put upload_from_client.txt", "get readme_server.txt", "ls", "bye"):
    c.expect("ftp> "); c.sendline(cmd)
c.expect(pexpect.EOF); log.close()
time.sleep(1); cap.terminate(); cap.wait()

shell(["ls -l /tmp/ftpclient", "cat /tmp/ftpclient/readme_server.txt", "ls -l /srv/ftp/ftpuser1",
       "grep -E 'CONNECT|LOGIN|UPLOAD|DOWNLOAD|command: .*(USER|PASS|LIST|STOR|RETR|QUIT)' /var/log/vsftpd.log"],
      "lab11_04_transfer_proof_and_server_log.txt")
shell(["tcpdump -nn -r /tmp/ftpclient/ftp.pcap 2>/dev/null | grep -E 'FTP: (220|USER|331|PASS|230)'"],
      "lab11_05_packet_capture_clear_text_login.txt")
