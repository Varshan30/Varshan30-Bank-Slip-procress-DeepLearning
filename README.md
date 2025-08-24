# ICR System - Intelligent Character Recognition 🤖

A comprehensive Python-based system for processing scanned handwritten forms (like bank slips), extracting text accurately using OCR, and structuring data into readable formats.

## ✅ Features

- **Advanced Image Preprocessing** - Noise reduction, contrast enhancement, and adaptive thresholding
- **Tesseract OCR Integration** - Accurate text extraction with configurable parameters
- **Structured Data Extraction** - Pattern-based field extraction (account numbers, amounts, dates)
- **Batch Processing** - Process multiple documents simultaneously
- **Multiple Output Formats** - CSV and JSON export capabilities
- **Error Handling** - Robust error recovery and logging
- **Extensible Design** - Easy to customize for different document types

## 🔧 Installation & Setup

### Prerequisites

1. **Python 3.7+** - [Download Python](https://www.python.org/downloads/)
2. **Tesseract OCR** - [Download Tesseract](https://github.com/UB-Mannheim/tesseract/wiki)
   - Windows: Download installer from the link above
   - Ubuntu: `sudo apt install tesseract-ocr`
   - macOS: `brew install tesseract`

### Quick Setup

1. **Clone or download** this project to your computer
2. **Run the setup** (choose one method):

   **Method 1: Automatic Setup (Windows)**
   ```bash
   # Double-click setup.bat or run in command prompt
   setup.bat
   ```

   **Method 2: Manual Setup**
   ```bash
   # Create virtual environment
   python -m venv icr_venv
   
   # Activate virtual environment
   # Windows:
   icr_venv\Scripts\activate
   # Linux/Mac:
   source icr_venv/bin/activate
   
   # Install dependencies
   pip install opencv-python pytesseract pillow numpy pandas
   ```

3. **Verify installation**
   ```bash
   python test_icr.py
   ```

## 🚀 Quick Start

### 1. Prepare Your Documents
- Place scanned forms in the `input_images/` folder
- Supported formats: PNG, JPG, JPEG, TIFF, BMP, GIF

### 2. Run Processing
```bash
# Activate virtual environment (if not already active)
icr_venv\Scripts\activate  # Windows
source icr_venv/bin/activate  # Linux/Mac

# Process all images in input_images folder
python icr_system.py

# Process a specific image
python icr_system.py --input path/to/your/image.jpg

# Save only CSV format
python icr_system.py --output-format csv

# Don't display results in console
python icr_system.py --no-display
```

### 3. Check Results
- **CSV/JSON files**: Check the `output_data/` folder
- **Processed images**: View in `processed_images/` folder
- **Logs**: Check `icr_system.log` for detailed processing information

## 📁 Project Structure

```
icr_system/
├── icr_system.py          # Main ICR processing script
├── setup.py               # Setup script for installation
├── test_icr.py           # Test script to verify installation
├── examples.py           # Example usage demonstrations
├── requirements.txt      # Python dependencies
├── setup.bat            # Windows batch setup script
├── setup_windows.ps1    # PowerShell setup script
├── README.md            # This documentation
├── input_images/        # 📁 Place your scanned forms here
├── processed_images/    # 📁 Preprocessed images (auto-generated)
├── output_data/         # 📁 CSV/JSON results (auto-generated)
├── temp_files/          # 📁 Temporary processing files
└── icr_venv/           # 📁 Virtual environment (auto-generated)
```

## 💡 Usage Examples

### Basic Usage
```python
from icr_system import ICRSystem

# Initialize the system
icr = ICRSystem()

# Process a single image
result = icr.process_single_image('input_images/bank_slip.jpg')
print(f"Account Number: {result['account_number']}")
print(f"Amount: {result['amount']}")

# Process multiple images
results = icr.process_batch('input_images/')

# Save results
icr.save_results_csv(results, 'my_results.csv')
icr.save_results_json(results, 'my_results.json')
```

### Custom Configuration
```python
# Initialize with custom Tesseract path
icr = ICRSystem(tesseract_path=r'C:\Program Files\Tesseract-OCR\tesseract.exe')

# Customize OCR settings
icr.ocr_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'

# Add custom field patterns
icr.field_patterns = {
    'invoice_number': r'INV\d{6}',
    'total_amount': r'\$\d+\.\d{2}',
    'customer_id': r'CUST\d{4}'
}
```

## 📊 Output Format

### CSV Output
```csv
source_file,account_number,amount,date,reference,raw_text,processed_timestamp
bank_slip_1.jpg,1234567890,1500.75,24/08/2025,ABC123XYZ,"Account: 1234567890...",2025-08-24T14:08:25
```

### JSON Output
```json
[
  {
    "source_file": "bank_slip_1.jpg",
    "account_number": "1234567890",
    "amount": "1500.75",
    "date": "24/08/2025",
    "reference": "ABC123XYZ",
    "raw_text": "Account: 1234567890...",
    "processed_timestamp": "2025-08-24T14:08:25"
  }
]
```

## 🎯 Supported Document Types

The system is optimized for bank slips and similar forms but can be customized for:
- **Bank deposit/withdrawal slips**
- **Invoice forms**
- **Application forms**
- **Survey forms**
- **Any structured handwritten document**

## ⚙️ Configuration Options

### OCR Configuration
- `--oem 3`: OCR Engine Mode (LSTM only)
- `--psm 6`: Page Segmentation Mode (uniform block of text)
- Character whitelisting for better accuracy

### Field Patterns (Regex)
- `account_number`: `r'\b\d{8,16}\b'`
- `amount`: `r'\b\d{1,6}(?:\.\d{2})?\b'`
- `date`: `r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b'`
- `reference`: `r'\b[A-Z0-9]{6,12}\b'`

## 🔍 Troubleshooting

### Common Issues

1. **"Tesseract not found"**
   - Install Tesseract OCR from the official website
   - Add Tesseract to your system PATH
   - Or specify the path: `ICRSystem(tesseract_path='path/to/tesseract')`

2. **Poor OCR accuracy**
   - Ensure images are high quality (300+ DPI)
   - Use clear, dark text on light background
   - Adjust OCR configuration parameters

3. **Import errors**
   - Activate the virtual environment
   - Reinstall dependencies: `pip install -r requirements.txt`

4. **No results extracted**
   - Check if the image contains readable text
   - Verify field patterns match your document format
   - Review the raw text output in results

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Run with verbose logging
icr = ICRSystem()
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
python test_icr.py
```

Run example demonstrations:
```bash
python examples.py
```

## 📈 Performance Tips

1. **Image Quality**: Use high-resolution scans (300+ DPI)
2. **Preprocessing**: The system automatically optimizes images
3. **Batch Processing**: Process multiple images for efficiency
4. **Custom Patterns**: Tailor regex patterns to your specific forms

## 🤝 Contributing

Feel free to contribute improvements:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify for your needs.

## 🆘 Support

For issues or questions:
1. Check the `icr_system.log` file for detailed error information
2. Run `python test_icr.py` to verify installation
3. Review this README for troubleshooting tips

## 🔄 Version History

- **v1.0**: Initial release with core ICR functionality
- Features: Image preprocessing, OCR extraction, structured data output
- Supported formats: PNG, JPG, JPEG, TIFF, BMP, GIF

---

**Built with ❤️ for document processing automation**

## 📦 Publishing to GitHub

Follow these steps to publish this project to your GitHub account:

### 1. Initialize Git (if not already)
```bash
git init
git add .
git commit -m "Initial commit: ICR System"
```

### 2. Create a New GitHub Repository
1. Go to https://github.com/new
2. Enter Repository name (e.g., `icr-system`)
3. Keep settings (Public or Private)
4. DON'T add a README (you already have one)
5. Click Create repository

### 3. Add Remote and Push
Copy the commands GitHub shows or use this pattern:
```bash
git remote add origin https://github.com/USERNAME/icr-system.git
git branch -M main
git push -u origin main
```
Replace `USERNAME` with your GitHub username.

### 4. Subsequent Updates
```bash
git add .
git commit -m "Describe your change"
git push
```

### 5. Optional: Add a License
```bash
echo "MIT License" > LICENSE
git add LICENSE
git commit -m "Add license"
git push
```

> Note: The `.gitignore` file excludes large and generated folders like `icr_venv/`, `output_data/`, and `processed_images/` to keep the repo clean.
