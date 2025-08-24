# Testing ICR with Your Own Images 🖼️

## Quick Start Guide

### Step 1: Prepare Your Images 📸
1. Place your bank slip images in the `input_images` folder
2. Supported formats: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.tiff`, `.tif`
3. For best results, ensure images are:
   - Clear and well-lit
   - Text is readable
   - Minimum 300 DPI resolution
   - Not too blurry or skewed

### Step 2: Run the Test 🚀
**Option A: Double-click the batch file**
```
test_my_images.bat
```

**Option B: Run manually**
```bash
# Activate virtual environment
icr_venv\Scripts\activate.bat

# Run the test script
python test_your_images.py
```

### Step 3: View Results 📊
Results will be saved in:
- `output_data/` - Text files with extracted data
- `processed_images/` - Processed versions of your images

## What the System Detects 🔍

The ICR system will automatically detect:

### 🏦 Bank Slip Information
- **💳 Account Numbers**: Various formats (10-16 digits)
- **💰 Amounts (Numbers)**: Currency amounts in digits
- **💸 Amounts (Words)**: Written amount descriptions
- **👤 Names**: Personal and business names
- **📅 Dates**: Various date formats
- **🔢 Reference Numbers**: Transaction references

### 📝 Pattern Examples
The system recognizes patterns like:
```
Account Numbers:
- 1234567890
- 12-3456-789012
- AC123456789

Amounts:
- $1,234.56
- USD 500.00
- Rs. 10,000

Names:
- John Smith
- ABC Corporation
- Mr. Johnson

Dates:
- 12/31/2023
- Dec 31, 2023
- 31-12-2023
```

## Troubleshooting 🛠️

### Common Issues:

**No images found:**
- Check that images are in `input_images` folder
- Verify file extensions are supported
- Make sure files aren't corrupted

**Poor OCR results:**
- Ensure images are clear and high resolution
- Check that text is not too small or blurry
- Try scanning at higher DPI (300+ recommended)

**Missing detected fields:**
- Some handwritten text may not be recognized
- Try different image preprocessing settings
- Consider improving image quality

### Image Quality Tips 📷

**For Best Results:**
1. **Lighting**: Ensure even, bright lighting
2. **Focus**: Make sure text is sharp and clear
3. **Angle**: Keep document flat and straight
4. **Resolution**: Use at least 300 DPI
5. **Format**: PNG or high-quality JPG works best

**Avoid:**
- Shadows on the document
- Blurry or out-of-focus text
- Extreme angles or perspective distortion
- Very low resolution images

## Sample Test Run 🎯

```
🏦 Bank Slip ICR Testing with Your Images
==================================================
📌 Make sure to place your images in the 'input_images' folder first!

🔧 Initializing ICR System...

📸 Found 2 image(s) to process:
   • bank_slip_1.jpg
   • deposit_slip.png

🚀 Starting OCR processing...
==================================================

📋 Processing Image 1/2: bank_slip_1.jpg
----------------------------------------
✅ OCR Success!

📝 Raw Text Extracted:
   DEPOSIT SLIP
   Date: 12/15/2023
   Account: 1234567890
   Amount: $1,500.00
   Name: John Smith...

🏦 Bank Slip Information Detected:
   💳 Account Numbers: 1234567890
   💰 Amount (Numbers): $1,500.00
   👤 Names: John Smith
   📅 Dates: 12/15/2023

💾 Results saved to: bank_slip_1_results.txt
```

## Advanced Usage 🔧

For custom processing or integration, you can use the ICR system directly:

```python
from icr_system import ICRSystem

# Initialize
icr = ICRSystem()

# Process single image
result = icr.process_single_image("path/to/your/image.jpg")

# Access results
if 'error' not in result:
    print("Processing successful!")
    print("Account Number:", result.get('account_number'))
    print("Amount:", result.get('amount_numbers'))
    print("Name:", result.get('name'))
else:
    print("Error:", result['error'])
```

## Next Steps 🎯

After testing:
1. Review results in `output_data` folder
2. Check processed images in `processed_images` folder
3. Fine-tune image quality for better results
4. Integrate the ICR system into your workflow

Happy testing! 🚀
