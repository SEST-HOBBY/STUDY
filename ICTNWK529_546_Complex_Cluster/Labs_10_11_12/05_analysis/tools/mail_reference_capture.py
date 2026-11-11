#!/usr/bin/env python3
"""Lab 12 reference run: send real mail between two mailboxes on the Postfix/Dovecot server started by
mail_reference_setup.sh and read it back over IMAP and POP3 in interactive telnet sessions.
Saves exactly what the terminal showed. Usage: mail_reference_capture.py <outdir>"""
import os, subprocess, sys, time, pexpect

out = sys.argv[1]; os.makedirs(out, exist_ok=True)
PS = "root@vm:~# "; PW = "Lab12-Pass!"

def shell(cmds, name):
    lines = []
    for c in cmds:
        r = subprocess.run(c, shell=True, capture_output=True, text=True)
        lines.append(PS + c); lines.append((r.stdout + r.stderr).rstrip("\n"))
    open(os.path.join(out, name), "w").write("\n".join(lines) + "\n")

def telnet(port, steps, name):
    log = open(os.path.join(out, name), "w")
    log.write(f"{PS}telnet mail.lab.local {port}\n")
    c = pexpect.spawn("telnet", ["mail.lab.local", str(port)], encoding="utf-8", timeout=15, dimensions=(60, 110))
    c.logfile_read = log
    c.expect(r"(\* OK|\+OK).*\r\n")
    for send, expect in steps:
        c.sendline(send); c.expect(expect)
    c.expect(pexpect.EOF); log.close()

shell(["postconf -n | grep -E '^(myhostname|mydomain|mydestination|home_mailbox|inet_interfaces)'",
       "cat /etc/dovecot/local.conf", "getent passwd user1 user2 | cut -d: -f1,6",
       "getent hosts mail.lab.local", "ss -tlnp | grep -E ':(25|110|143) '"], "lab12_01_server_running.txt")

shell(["swaks --server mail.lab.local --helo client.lab.local --from user1@lab.local --to user2@lab.local "
       "--header 'Subject: Lab 12 test message' --body 'Hello user2, this is the Lab 12 test message from user1.'"],
      "lab12_02_smtp_send_user1_to_user2.txt")
time.sleep(2)
telnet(143, [(f"a1 LOGIN user2 {PW}", r"a1 OK.*\r\n"), ("a2 SELECT INBOX", r"a2 OK.*\r\n"),
             ("a3 FETCH 1 (BODY[HEADER.FIELDS (FROM TO SUBJECT DATE)] BODY[TEXT])", r"a3 OK.*\r\n"),
             ("a4 LOGOUT", r"a4 OK.*\r\n")], "lab12_03_imap_user2_receives.txt")

shell(["swaks --server mail.lab.local --helo client.lab.local --from user2@lab.local --to user1@lab.local "
       "--header 'Subject: RE: Lab 12 test message' --body 'Hello user1, received. This is the reply.' --hide-all; "
       "echo swaks exit code: $?"], "lab12_04a_reply_sent.txt")
time.sleep(2)
telnet(110, [("USER user1", r"\+OK.*\r\n"), (f"PASS {PW}", r"\+OK.*\r\n"), ("LIST", r"\r\n\.\r\n"),
             ("RETR 1", r"\r\n\.\r\n"), ("QUIT", r"\+OK.*\r\n")], "lab12_04b_pop3_user1_receives_reply.txt")

shell(["grep -E 'from=<|to=<' /var/log/postfix.log", "grep -E 'Login' /var/log/dovecot.log"],
      "lab12_05_server_logs.txt")
