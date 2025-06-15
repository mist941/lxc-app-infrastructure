#!/bin/bash

set -euo pipefail

export RESTIC_REPOSITORY=/mnt/backups/db
export RESTIC_PASSWORD=password
BACKUP_DIR=/tmp/db_backup
REMOTE_DB_HOST=192.168.88.87
TIMESTAMP=$(date +%F_%H-%M-%S)

echo "Backing up Forgejo database..."
PGPASSWORD=password pg_dump -h $REMOTE_DB_HOST -U forgejo_admin forgejo > $BACKUP_DIR/db_forgejo_dump_$TIMESTAMP.sql
restic backup $BACKUP_DIR
rm -f $BACKUP_DIR/db_forgejo_dump_$TIMESTAMP.sql

echo "Backing up Drone database..."
PGPASSWORD=password pg_dump -h $REMOTE_DB_HOST -U drone_admin drone > $BACKUP_DIR/db_drone_dump_$TIMESTAMP.sql
restic backup $BACKUP_DIR
rm -f $BACKUP_DIR/db_drone_dump_$TIMESTAMP.sql

# Cleanup old backups
echo "Cleaning up old backups..."
restic forget --prune --keep-daily 7 --keep-weekly 4 --keep-monthly 6

rm -rf $BACKUP_DIR

echo "Backup completed successfully"