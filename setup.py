"""
ICR System Setup Script
======================

This script sets up the virtual environment and installs all dependencies
for the Intelligent Character Recognition system.

Usage:
    python setup.py
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(command, check=True):
    """Run a shell command and handle errors"""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def setup_virtual_environment():
    """Create and activate virtual environment"""
    print("🔧 Setting up virtual environment...")
    
    # Create virtual environment
    venv_path = "icr_venv"
    if not os.path.exists(venv_path):
        run_command(f"python -m venv {venv_path}")
        print(f"✅ Virtual environment created: {venv_path}")
    else:
        print(f"📁 Virtual environment already exists: {venv_path}")
    
    # Determine activation script path based on OS
    if os.name == 'nt':  # Windows
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
        pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
    else:  # Unix/Linux/Mac
        activate_script = os.path.join(venv_path, "bin", "activate")
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    return activate_script, pip_path

def install_dependencies(pip_path):
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    # Upgrade pip first
    run_command(f'"{pip_path}" install --upgrade pip')
    
    # Install requirements
    if os.path.exists("requirements.txt"):
        run_command(f'"{pip_path}" install -r requirements.txt')
        print("✅ Dependencies installed from requirements.txt")
    else:
        # Install individual packages
        packages = [
            "opencv-python==4.9.0.80",
            "pytesseract==0.3.10", 
            "pillow==10.3.0",
            "numpy==1.26.4",
            "pandas==2.2.1"
        ]
        
        for package in packages:
            run_command(f'"{pip_path}" install {package}')
        
        print("✅ Core dependencies installed")

def create_project_structure():
    """Create necessary project directories"""
    print("📁 Creating project structure...")
    
    directories = [
        "input_images",
        "processed_images", 
        "output_data",
        "temp_files",
        "sample_images"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"  📂 {directory}/")
    
    print("✅ Project structure created")

def create_sample_files():
    """Create sample configuration and test files"""
    print("📝 Creating sample files...")
    
    # Create a sample configuration file
    config_content = """{
    "tesseract_path": "",
    "ocr_config": "--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,/- ",
    "field_patterns": {
        "account_number": "\\\\b\\\\d{8,16}\\\\b",
        "amount": "\\\\b\\\\d{1,6}(?:\\\\.\\\\d{2})?\\\\b",
        "date": "\\\\b\\\\d{1,2}[/-]\\\\d{1,2}[/-]\\\\d{2,4}\\\\b",
        "reference": "\\\\b[A-Z0-9]{6,12}\\\\b"
    }
}"""
    
    with open("config.json", "w") as f:
        f.write(config_content)
    
    # Create a README file
    readme_content = """# ICR System - Intelligent Character Recognition

## Setup Complete! 🎉

Your ICR system is now ready to process handwritten forms and documents.

## Quick Start

1. **Activate Virtual Environment:**
   ```bash
   # Windows
   icr_venv\\Scripts\\activate
   
   # Linux/Mac
   source icr_venv/bin/activate
   ```

2. **Add Images:**
   - Place your scanned forms in the `input_images/` folder
   - Supported formats: PNG, JPG, JPEG, TIFF, BMP, GIF

3. **Run Processing:**
   ```bash
   python icr_system.py
   ```

4. **Check Results:**
   - CSV/JSON files will be saved in `output_data/`
   - Processed images will be in `processed_images/`

## Usage Examples

```bash
# Process all images in input_images folder
python icr_system.py

# Process a specific image
python icr_system.py --input path/to/image.jpg

# Save only CSV format
python icr_system.py --output-format csv

# Don't display results in console
python icr_system.py --no-display
```

## Tesseract Installation

Make sure Tesseract OCR is installed:

- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Ubuntu**: `sudo apt install tesseract-ocr`
- **macOS**: `brew install tesseract`

## Project Structure

```
icr_system/
├── icr_system.py          # Main ICR processing script
├── setup.py               # Setup script (this file)
├── requirements.txt       # Python dependencies
├── config.json           # Configuration settings
├── input_images/         # Place your scanned forms here
├── processed_images/     # Preprocessed images
├── output_data/          # CSV/JSON results
├── temp_files/           # Temporary processing files
└── icr_venv/            # Virtual environment
```

## Features

✅ Image preprocessing for better OCR accuracy
✅ Text extraction using Tesseract OCR  
✅ Structured data extraction (account numbers, amounts, dates)
✅ Batch processing support
✅ CSV and JSON export
✅ Comprehensive logging
✅ Error handling and recovery

## Support

For issues or questions, check the log file: `icr_system.log`
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    
    print("✅ Sample files created (config.json, README.md)")

def main():
    """Main setup function"""
    print("🚀 ICR System Setup")
    print("=" * 50)
    
    try:
        # Setup virtual environment
        activate_script, pip_path = setup_virtual_environment()
        
        # Install dependencies
        install_dependencies(pip_path)
        
        # Create project structure
        create_project_structure()
        
        # Create sample files
        create_sample_files()
        
        print("\n" + "=" * 50)
        print("🎉 ICR System setup completed successfully!")
        print("\n📋 Next Steps:")
        print(f"1. Activate virtual environment:")
        if os.name == 'nt':
            print(f"   icr_venv\\Scripts\\activate")
        else:
            print(f"   source icr_venv/bin/activate")
        print("2. Place images in input_images/ folder")
        print("3. Run: python icr_system.py")
        print("\n📖 Check README.md for detailed instructions")
        
    except Exception as e:
        print(f"❌ Setup failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
