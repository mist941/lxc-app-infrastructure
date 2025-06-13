#!/bin/bash

set -euo pipefail

sudo apt install restic

export RESTIC_PASSWORD=1234567890

restic init
