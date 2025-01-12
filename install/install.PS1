# Install the required Python package
Write-Host "Installing NFT_Python_Generator..."

# Check if Python is installed
if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python 3.7 or higher."
    exit 1
}

# Upgrade pip and setuptools
python -m pip install --upgrade pip setuptools wheel

# Install the package in editable mode
python -m pip install -e .

Write-Host "NFT_Python_Generator has been installed successfully!"
