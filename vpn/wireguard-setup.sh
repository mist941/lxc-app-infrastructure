#!/bin/bash

set -euo pipefail

sudo apt update && sudo apt upgrade -y

sudo apt install -y wireguard

umask 077

wg genkey | tee /etc/wireguard/privatekey | wg pubkey > /etc/wireguard/publickey

cat <<EOF > /etc/wireguard/wg0.conf
[Interface]
PrivateKey = $(cat /etc/wireguard/privatekey)
Address = 10.0.0.1/24
ListenPort = 51820
SaveConfig = true

[Peer]
PublicKey = $(cat /etc/wireguard/publickey)
AllowedIPs = 0.0.0.0/0

PostUp = iptables -A FORWARD -i %i -j ACCEPT; iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
PostDown = iptables -D FORWARD -i %i -j ACCEPT; iptables -t nat -D POSTROUTING -o eth0 -j MASQUERADE
EOF

sudo sysctl -p

sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0