@echo off

SET ORIGINAL_DIR=%CD%

REM Find the script's directory and move there
SET SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

REM Install the required Python package
echo Installing NFT_Python_Generator...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.7 or higher.
    exit /b 1
)

REM Install dependencies
pip install --upgrade pip setuptools wheel pyinstaller
pip install -r "..\requirements.txt"

echo Building the executable...
pyinstaller --onefile --windowed --name "NFT_Generator" "..\gui.py"

REM Move the executable to a dedicated folder
if not exist "%SCRIPT_DIR%\dist" mkdir "%SCRIPT_DIR%\dist"
move "%SCRIPT_DIR%\dist\NFT_Generator.exe" "%SCRIPT_DIR%\dist\NFT_Generator.exe" 
echo NFT_Python_Generator has been built successfully!

REM Optional: Run the executable after installation
echo Starting the NFT Generator GUI...
start "" "%SCRIPT_DIR%\dist\NFT_Generator.exe"

REM Change back to the original directory
cd /d %ORIGINAL_DIR%

pause
