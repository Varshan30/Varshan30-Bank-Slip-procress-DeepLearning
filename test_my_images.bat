@echo off
echo.
echo ===============================================
echo     Bank Slip ICR - Test Your Own Images
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

REM Check if input_images folder exists and has images
if not exist "input_images" (
    mkdir input_images
    echo Created input_images folder.
)

REM Count images in folder
set image_count=0
for %%i in (input_images\*.jpg input_images\*.jpeg input_images\*.png input_images\*.bmp input_images\*.tiff input_images\*.tif) do set /a image_count+=1

if %image_count%==0 (
    echo.
    echo [WARNING] No images found in input_images folder!
    echo.
    echo Please place your bank slip images in the 'input_images' folder:
    echo   - Supported formats: JPG, PNG, BMP, TIFF
    echo   - Example: input_images\bank_slip.jpg
    echo.
    echo Opening input_images folder for you...
    start "" "input_images"
    echo.
    pause
    exit /b 1
)

echo Found %image_count% image(s) to process.
echo.

REM Run the testing script
python test_your_images.py

REM Deactivate virtual environment
deactivate

echo.
echo Testing completed! Check the output_data folder for results.
pause
