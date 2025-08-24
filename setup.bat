@echo off
echo.
echo ==========================================
echo   ICR System - Quick Setup for Windows
echo ==========================================
echo.

echo 🚀 Starting ICR System setup...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.7+ first.
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Run the setup script
echo 📦 Running setup...
python setup.py

if errorlevel 1 (
    echo.
    echo ❌ Setup failed. Check the error messages above.
    pause
    exit /b 1
)

echo.
echo ✅ Setup completed successfully!
echo.

REM Activate virtual environment and show instructions
echo 🔌 Activating virtual environment...
call icr_venv\Scripts\activate.bat

echo.
echo 📋 Quick Start Guide:
echo ==================
echo.
echo 1. Add your scanned forms to the 'input_images' folder
echo 2. Run: python icr_system.py
echo 3. Check results in 'output_data' folder
echo.

echo 🧪 Running system test...
python test_icr.py

echo.
echo 🎉 ICR System is ready to use!
echo.
echo Press any key to exit...
pause >nul
