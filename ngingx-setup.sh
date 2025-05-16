#!/bin/bash

set -euo pipefail

sudo apt update && sudo apt upgrade -y

sudo apt install -y nginx

cat <<EOF > /etc/nginx/sites-available/app-proxy
  server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass <ip_address>;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
EOF

cat <<EOF > /etc/nginx/sites-available/forgejo-proxy
  server {
    listen 80;
    server_name forgejo.example.com;

    location / {
        proxy_pass <ip_address>;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
EOF

cat <<EOF > /etc/nginx/sites-available/monitoring-proxy
  server {
    listen 80;
    server_name monitoring.example.com;

    location / {
        proxy_pass <ip_address>;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
  }
EOF

sudo ln -s /etc/nginx/sites-available/app-proxy /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/forgejo-proxy /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/monitoring-proxy /etc/nginx/sites-enabled/

sudo systemctl enable nginx

sudo systemctl start nginx

sudo ufw allow 'Nginx Full'

sudo ufw enable