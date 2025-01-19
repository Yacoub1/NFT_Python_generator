#!/bin/bash

# Install the required Python package
echo "Installing NFT_Python_Generator..."

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install the package in editable mode
pip install -e .

echo "NFT_Python_Generator has been installed successfully!"