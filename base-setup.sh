#!/bin/bash

set -euo pipefail

set -a
source .env
set +a

sudo apt update && sudo apt upgrade -y

sudo adduser admin

sudo usermod -aG sudo admin

echo "admin:$ADMIN_PASSWORD" | sudo chpasswd

sudo ufw allow OpenSSH

sudo ufw enable

sudo apt install fail2ban