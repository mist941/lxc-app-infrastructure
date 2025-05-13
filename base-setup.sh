#!/bin/bash

set -euo pipefail

if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

set -a
source .env
set +a

if [ -z "${ADMIN_PASSWORD:-}" ]; then
    echo "Error: ADMIN_PASSWORD is not set in .env file"
    exit 1
fi

sudo apt update && sudo apt upgrade -y

sudo adduser admin

sudo usermod -aG sudo admin

sudo mkdir -p /home/admin/.ssh

sudo chmod 700 /home/admin/.ssh

sudo cp ~/.ssh/authorized_keys /home/admin/.ssh/authorized_keys

sudo chmod 600 /home/admin/.ssh/authorized_keys

sudo chown -R admin:admin /home/admin/.ssh

sudo ufw allow OpenSSH

sudo ufw enable

sudo apt install fail2ban