#!/bin/bash
# HumaninFinder: Automated Environment Setup
set -e

echo "[*] Initializing HumaninFinder setup..."

# 1. Check for HMMER3
if ! command -v hmmsearch &> /dev/null; then
    echo "[!] HMMER3 not found. This is a required system dependency."
    echo "    Install it via: 'conda install -c bioconda hmmer' or 'sudo apt install hmmer'"
    exit 1
fi

# 2. Install Python dependencies
echo "[*] Installing Python dependencies..."
pip install --upgrade pip
pip install .

echo "[+] Setup complete! You can now run the tool using:"
echo "    humanin-finder --help"
