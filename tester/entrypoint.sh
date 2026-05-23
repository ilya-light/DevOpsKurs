#!/usr/bin/env bash
set -euo pipefail

mkdir -p /run/sshd /workspace/logs
chmod 700 /home/tester/.ssh
chmod 600 /home/tester/.ssh/authorized_keys
chown -R tester:tester /home/tester/.ssh /workspace
ssh-keygen -A >/dev/null 2>&1
/usr/sbin/sshd

cd /workspace
exec "$@"
