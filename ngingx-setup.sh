#!/bin/bash

set -euo pipefail

sudo apt update && sudo apt upgrade -y

sudo apt install -y nginx

sudo systemctl enable nginx
sudo systemctl start nginx

sudo ufw allow 'Nginx Full'
sudo ufw enable