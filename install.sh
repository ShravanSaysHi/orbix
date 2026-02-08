#!/usr/bin/env bash

set -e

echo "== Offline AI Assistant Installer =="

# Check Python version
if ! python3 -c "import sys; exit(0 if (3,10) <= sys.version_info < (3,13) else 1)"; then
  echo "Python 3.10–3.12 required."
  exit 1
fi

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and install deps
pip install --upgrade pip
pip install -r requirements.txt

echo "Installation complete."
echo "Run with: ./run.sh"
