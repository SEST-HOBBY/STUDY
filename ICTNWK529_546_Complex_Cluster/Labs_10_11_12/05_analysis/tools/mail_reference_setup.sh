#!/bin/bash
# Lab 12 reference run: a real Postfix (SMTP) + Dovecot (IMAP, POP3) mail server on Ubuntu 24.04 for the
# domain lab.local with two mailboxes. Run as root on a throwaway Linux machine: plain-text logins are
# switched on so the protocol can be read, which is only acceptable in a lab.
# The captures in ../reference_snips/raw/lab12_*.txt came from this.
set -euo pipefail
IP="${1:?server IP}"
grep -q 'mail.lab.local' /etc/hosts || echo "$IP mail.lab.local mail" >> /etc/hosts
for u in user1 user2; do
  id $u >/dev/null 2>&1 || useradd -m -s /bin/bash $u
  echo "$u:Lab12-Pass!" | chpasswd
  rm -rf /home/$u/Maildir
done
postconf -e 'myhostname = mail.lab.local' 'mydomain = lab.local' 'myorigin = $mydomain' \
  'mydestination = $myhostname, $mydomain, localhost' 'inet_interfaces = all' 'inet_protocols = ipv4' \
  "mynetworks = 127.0.0.0/8 $IP/32" 'home_mailbox = Maildir/' 'maillog_file = /var/log/postfix.log' \
  'smtpd_banner = $myhostname ESMTP' 'compatibility_level = 3.6'
cat > /etc/dovecot/local.conf <<'CONF'
protocols = imap pop3
listen = *
mail_location = maildir:~/Maildir
disable_plaintext_auth = no
ssl = no
log_path = /var/log/dovecot.log
CONF
postfix stop >/dev/null 2>&1 || true; pkill -x dovecot 2>/dev/null || true; sleep 1
: > /var/log/postfix.log; : > /var/log/dovecot.log
[ -x /usr/lib/postfix/configure-instance.sh ] && /usr/lib/postfix/configure-instance.sh - || true
postfix start
dovecot
sleep 2
ss -tlnp | grep -E ':(25|110|143) '
