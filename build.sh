#!/usr/bin/env bash
# Exit on error
set -o errexit

# 1. Install project dependencies
pip install -r requirements.txt

# 2. Collect static files for WhiteNoise
python manage.py collectstatic --no-input

# 3. Apply database migrations to PostgreSQL
python manage.py migrate
