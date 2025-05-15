#!/bin/bash

set -euo pipefail

sudo apt update && sudo apt upgrade -y

sudo apt install -y certbot python3-certbot-nginx
