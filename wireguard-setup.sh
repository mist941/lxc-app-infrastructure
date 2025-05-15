#!/bin/bash

set -euo pipefail

sudo apt update && sudo apt upgrade -y

sudo apt install -y wireguard

sudo systemctl enable wg-quick@wg0
sudo systemctl start wg-quick@wg0

sudo ufw allow 51820/udp
sudo ufw enable

