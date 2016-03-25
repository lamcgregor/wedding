#!/bin/sh
set -e
rm -rf dist/static/*; cp -r static dist/
gunicorn -b 0.0.0.0:8000 wedding_api.wsgi --pythonpath ./wedding_api --log-file - --log-level debug --access-logfile -
