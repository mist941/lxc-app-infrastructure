#!/bin/bash

set -euo pipefail

POSTGRES_USER="forgejo"
POSTGRES_PASSWORD="forgejo"
POSTGRES_DB="forgejo"

apt update && apt install postgresql -y

sed -i "s/^#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/*/main/postgresql.conf

echo "host    all             all             192.168.88.0/24            md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf > /dev/null

systemctl restart postgresql

sudo -u postgres psql -c "CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';"

sudo -u postgres psql -c "CREATE DATABASE $POSTGRES_DB;"

sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;"