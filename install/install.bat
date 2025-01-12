@echo off
REM Install the required Python package
echo Installing NFT_Python_Generator...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.7 or higher.
    exit /b 1
)

REM Install the package in editable mode
pip install --upgrade pip setuptools wheel
pip install -e .

echo NFT_Python_Generator has been installed successfully!
pause