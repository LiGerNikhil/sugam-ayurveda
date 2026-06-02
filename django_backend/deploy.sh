#!/bin/bash

# Deployment Script for Sugam Ayurveda
# Target: /var/www/sugam-ayurveda/django_backend/

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

PROJECT_DIR="/var/www/sugam-ayurveda/django_backend"
VENV_DIR="$PROJECT_DIR/.venv"

cd "$PROJECT_DIR"

# ── Git pull ──────────────────────────────────────────────────────────────────
info "Pulling latest code from git..."
git stash -- staticfiles/ 2>/dev/null || true
git pull --ff-only origin main
git stash drop 2>/dev/null || true

# ── Virtual environment ───────────────────────────────────────────────────────
info "Activating virtual environment..."
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi
source "$VENV_DIR/bin/activate"
pip install -r requirements.txt --quiet

# ── Collect static files ──────────────────────────────────────────────────────
info "Collecting static files (clearing old cache)..."
export DJANGO_PRODUCTION=true
python manage.py collectstatic --noinput --clear

# ── Permissions ───────────────────────────────────────────────────────────────
info "Setting permissions on staticfiles..."
sudo chown -R www-data:www-data "$PROJECT_DIR/staticfiles"
sudo chmod -R 755 "$PROJECT_DIR/staticfiles"

# ── Nginx reload ──────────────────────────────────────────────────────────────
info "Reloading Nginx..."
sudo nginx -t && sudo systemctl reload nginx

info "Deployment complete."
