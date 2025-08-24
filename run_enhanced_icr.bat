@echo off
echo.
echo ===============================================
echo     Enhanced ICR System - Better Results
echo ===============================================
echo.

REM Check if virtual environment exists
if not exist "icr_venv\Scripts\activate.bat" (
    echo Virtual environment not found! Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call icr_venv\Scripts\activate.bat

echo Starting Enhanced ICR Processing...
echo.

REM Run the enhanced testing script
python test_enhanced_system.py

REM Deactivate virtual environment
deactivate

echo.
echo Enhanced processing completed!
echo Check the output_data folder for detailed results.
pause
