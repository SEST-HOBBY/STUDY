#!/bin/bash
# Lab 11 reference run: a real vsftpd server on Ubuntu 24.04, one local user, one shared folder.
# Run as root on a throwaway Linux machine. The captures in ../reference_snips/raw/lab11_*.txt came from this.
set -euo pipefail
id ftpuser1 >/dev/null 2>&1 || useradd -m -d /srv/ftp/ftpuser1 -s /bin/bash ftpuser1
echo 'ftpuser1:Lab11-Pass!' | chpasswd
rm -f /srv/ftp/ftpuser1/upload_from_client.txt
echo "Lab 11 test file on the FTP server" > /srv/ftp/ftpuser1/readme_server.txt
chown -R ftpuser1:ftpuser1 /srv/ftp/ftpuser1
mkdir -p /var/run/vsftpd/empty
cat > /etc/vsftpd.conf <<'CONF'
listen=YES
listen_ipv6=NO
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
chroot_local_user=YES
allow_writeable_chroot=YES
pasv_enable=YES
pasv_min_port=50000
pasv_max_port=50100
xferlog_enable=YES
log_ftp_protocol=YES
vsftpd_log_file=/var/log/vsftpd.log
secure_chroot_dir=/var/run/vsftpd/empty
pam_service_name=vsftpd
CONF
pkill -x vsftpd 2>/dev/null || true
: > /var/log/vsftpd.log
nohup /usr/sbin/vsftpd /etc/vsftpd.conf >/dev/null 2>&1 &
sleep 1
ss -tlnp | grep ':21 '
