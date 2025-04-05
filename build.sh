#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Create default media directories
mkdir -p media/default_profiles
mkdir -p media/profile_pics
mkdir -p media/cover_pics
mkdir -p media/tweet_images

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput
