#!/bin/bash

set -e

export RESTIC_REPOSITORY=/mnt/backups/db
export RESTIC_PASSWORD=yourpassword
BACKUP_DIR=/tmp/db_backup
TIMESTAMP=$(date +%F_%H-%M-%S)
DB_NAME=yourdb
DB_USER=youruser

mkdir -p $BACKUP_DIR

pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_dump_$TIMESTAMP.sql

restic backup $BACKUP_DIR

restic forget --prune --keep-daily 7 --keep-weekly 4 --keep-monthly 6

rm -rf $BACKUP_DIR
