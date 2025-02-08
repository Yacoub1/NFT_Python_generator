#!/bin/bash

# Store the original directory
ORIGINAL_DIR="$(pwd)"

# Get the script's directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $SCRIPT_DIR
cd "$SCRIPT_DIR"

# Install the required Python package
echo "Installing NFT_Python_Generator..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

cd ..
# Install dependencies
pip3 install -r "requirements.txt"

# Build the executable
pyinstaller --onefile --name nft_gen_tool --exclude-module PyQt5 --exclude-module pygame --exclude-module tensorflow --exclude-module torch NFT_Python_generator/nft_gen_tool.py

# Move the executable to a more accessible location
DIST_PATH="./dist"
if [ ! -d "$DIST_PATH" ]; then
    mkdir "$DIST_PATH"
fi
mv dist/NFT_Generator "$DIST_PATH/NFT_Generator"

echo "NFT_Python_Generator has been installed and built successfully!"
echo "You can now run the tool using: $DIST_PATH/NFT_Generator"

# Change back to the original directory
cd "$ORIGINAL_DIR"
