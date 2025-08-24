@echo off
title ICR System - Intelligent Character Recognition

echo.
echo ==========================================
echo   ICR System - Document Processing
echo ==========================================
echo.

REM Check if virtual environment exists
if not exist "icr_venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo Please run setup.bat first to install the system.
    echo.
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔌 Activating virtual environment...
call icr_venv\Scripts\activate.bat

echo ✅ ICR System ready!
echo.

:menu
echo 📋 Choose an option:
echo.
echo 1. Process all images in input_images folder
echo 2. Process a specific image file
echo 3. Run system test
echo 4. View examples
echo 5. Open project folder
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto process_all
if "%choice%"=="2" goto process_single
if "%choice%"=="3" goto run_test
if "%choice%"=="4" goto run_examples
if "%choice%"=="5" goto open_folder
if "%choice%"=="6" goto exit

echo Invalid choice. Please try again.
goto menu

:process_all
echo.
echo 🤖 Processing all images in input_images folder...
python icr_system.py
echo.
echo ✅ Processing completed! Check output_data folder for results.
echo.
pause
goto menu

:process_single
echo.
set /p filepath="Enter the path to your image file: "
echo.
echo 🤖 Processing: %filepath%
python icr_system.py --input "%filepath%"
echo.
echo ✅ Processing completed! Check output_data folder for results.
echo.
pause
goto menu

:run_test
echo.
echo 🧪 Running system test...
python test_icr.py
echo.
pause
goto menu

:run_examples
echo.
echo 🎯 Running examples...
python examples.py
echo.
pause
goto menu

:open_folder
echo.
echo 📁 Opening project folder...
start .
goto menu

:exit
echo.
echo 👋 Thank you for using ICR System!
echo.
pause
