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

# System updates
sudo apt update && sudo apt upgrade -y

# Create admin user
sudo adduser --gecos "" admin
echo "admin:${ADMIN_PASSWORD}" | sudo chpasswd
sudo usermod -aG sudo admin

# SSH setup
sudo mkdir -p /home/admin/.ssh
sudo chmod 700 /home/admin/.ssh
sudo cp ~/.ssh/authorized_keys /home/admin/.ssh/authorized_keys
sudo chmod 600 /home/admin/.ssh/authorized_keys
sudo chown -R admin:admin /home/admin/.ssh

# SSH security
sudo sed -i 's/#PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' /etc/ssh/sshd_config
sudo sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/' /etc/ssh/sshd_config
sudo sed -i 's/#ChallengeResponseAuthentication yes/ChallengeResponseAuthentication no/' /etc/ssh/sshd_config
sudo systemctl restart sshd

# Firewall setup
sudo ufw allow OpenSSH
sudo ufw enable

# Fail2ban setup
sudo apt install -y fail2ban
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# System settings
sudo timedatectl set-timezone Europe/Kiev

# Automatic security updates
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades