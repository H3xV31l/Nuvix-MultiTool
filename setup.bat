@echo off
echo Installing required Python packages...

:: Upgrade pip
python -m pip install --upgrade pip

:: Install required packages
pip install colorama

echo.
echo Setup complete! You can now run the tool with:
echo     python main.py
pause
