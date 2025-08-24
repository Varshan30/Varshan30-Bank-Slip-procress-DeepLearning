"""
ICR System - Usage Guide and Real-World Examples
===============================================

This guide shows how to use the ICR system with real bank slips and forms.
The system is designed to extract:
- Account numbers
- Amounts (both in numbers and words)
- Names/depositors
- Dates and references
"""

import os
from icr_system import ICRSystem

def create_usage_guide():
    """Create a comprehensive usage guide"""
    
    guide = """
# ICR System - Bank Slip Recognition Guide

## 🎯 What the Enhanced System Can Detect:

### 1. Account Numbers
- Patterns like: "Account Number: 1234567890"
- "A/C No: 1234567890"
- "Account: 1234567890"
- Standalone long numbers (8-16 digits)

### 2. Amounts in Numbers
- "Amount: 15,750.50"
- "Rs. 25000.00"
- "$1,500.75"
- "15750.50 Only"

### 3. Amounts in Words
- "Fifteen Thousand Seven Hundred Fifty Rupees Only"
- "Twenty Five Thousand Rupees Only"
- "One Lakh Fifty Thousand Rupees Only"

### 4. Names/Depositors
- "Name: John Smith"
- "Depositor: Sarah Wilson"
- "Account Holder: Michael Johnson"
- "Mr./Mrs./Ms./Dr. followed by name"

### 5. Other Fields
- Dates: "24/08/2025", "24-08-2025"
- References: "TXN123456", "REF789ABC"

## 📋 How to Use with Real Bank Slips:

1. **Scan/Photo Quality**:
   - Use high resolution (300+ DPI)
   - Ensure good lighting
   - Avoid shadows and glare
   - Keep text horizontal and clear

2. **File Formats**: PNG, JPG, JPEG, TIFF, BMP, GIF

3. **Place Files**: Put your scanned slips in the `input_images/` folder

4. **Run Processing**:
   ```bash
   # Activate virtual environment
   icr_venv\\Scripts\\activate
   
   # Process all images
   python icr_system.py
   
   # Or use the GUI launcher
   run_icr.bat
   ```

5. **Check Results**:
   - CSV file in `output_data/` folder
   - Visual overlays in `processed_images/` folder

## 🔧 Customization for Your Forms:

If you have specific form types, you can customize the patterns:

```python
from icr_system import ICRSystem

# Initialize system
icr = ICRSystem()

# Customize for your specific forms
icr.field_patterns.update({
    'customer_id': r'customer[\s:.-]*([A-Z0-9]{4,8})',
    'invoice_number': r'invoice[\s:.-]*([A-Z0-9]{6,10})',
    # Add your patterns here
})

# Process your documents
results = icr.process_batch()
```

## 📊 Expected Output Format:

### CSV Output:
```csv
source_file,account_number,amount_numbers,amount_words,name,date,reference
bank_slip_1.jpg,1234567890,15750.50,fifteen thousand rupees,john smith,24/08/2025,TXN123
```

### JSON Output:
```json
{
  "account_number": "1234567890",
  "amount_numbers": "15750.50",
  "amount_words": "fifteen thousand rupees",
  "name": "john smith",
  "date": "24/08/2025",
  "reference": "TXN123"
}
```

## ⚠️ Important Notes:

1. **OCR Accuracy**: Results depend on image quality and handwriting clarity
2. **False Positives**: Always verify extracted data manually for critical applications
3. **Privacy**: Ensure sensitive financial data is handled securely
4. **Backup**: Keep original images as backup

## 🧪 Testing Your Setup:

1. Run the test script: `python test_icr.py`
2. Check log file: `icr_system.log`
3. Verify Tesseract installation
4. Test with a sample clear image first

## 🔍 Troubleshooting:

### Poor Recognition:
- Check image quality and resolution
- Ensure text is clear and horizontal
- Try different lighting conditions
- Clean the document before scanning

### Missing Fields:
- Check if field labels match expected patterns
- Customize regex patterns for your forms
- Review raw OCR text in results

### Installation Issues:
- Ensure Tesseract OCR is installed
- Check virtual environment activation
- Verify all dependencies are installed

## 🎉 Success Tips:

1. **Quality First**: High-quality scans = better results
2. **Consistent Format**: Use similar document layouts
3. **Clear Labels**: Ensure field labels are clearly visible
4. **Batch Processing**: Process multiple similar documents together
5. **Manual Review**: Always verify critical extracted data

---
Happy Processing! 🤖
"""
    
    with open("USAGE_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(guide)
    
    print("📖 Usage guide created: USAGE_GUIDE.md")

def demonstrate_real_world_patterns():
    """Demonstrate how the enhanced patterns work"""
    
    print("\n🔍 ICR System - Enhanced Pattern Recognition Demo")
    print("=" * 60)
    
    # Sample text that might come from OCR
    sample_texts = [
        "Account Number: 1234567890123\nAmount: Rs. 15,750.50\nName: John Michael Smith\nDate: 24/08/2025",
        "A/C No: 987654321098\nDepositor: Mrs. Sarah Wilson\nAmount in Words: Twenty Five Thousand Rupees Only\nAmount: 25000.00",
        "Account Holder: Dr. Robert Johnson\nTransaction Amount: $1,500.75\nReference: TXN789ABC\nDate: 24-08-2025",
        "Beneficiary Name: Ms. Emily Davis\nAccount: 456789012345\nAmount: Fifty Thousand Rupees Only\nAmount: 50,000.00"
    ]
    
    icr = ICRSystem()
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n--- Sample Text {i} ---")
        print(f"Raw: {text}")
        print()
        
        # Extract structured data
        result = icr.extract_structured_data(text)
        
        print("Extracted:")
        print(f"  🏦 Account: '{result.get('account_number', 'Not found')}'")
        print(f"  💰 Amount (Num): '{result.get('amount_numbers', 'Not found')}'")
        print(f"  💬 Amount (Words): '{result.get('amount_words', 'Not found')}'")
        print(f"  👤 Name: '{result.get('name', 'Not found')}'")
        print(f"  📅 Date: '{result.get('date', 'Not found')}'")
        print(f"  🔗 Reference: '{result.get('reference', 'Not found')}'")

def main():
    """Main demonstration function"""
    print("📚 ICR System - Enhanced Bank Slip Recognition")
    print("=" * 60)
    
    try:
        # Create usage guide
        create_usage_guide()
        
        # Demonstrate pattern matching
        demonstrate_real_world_patterns()
        
        print("\n" + "=" * 60)
        print("✅ Enhanced ICR system demonstration completed!")
        print("\n📋 Key Improvements:")
        print("• Multiple account number detection patterns")
        print("• Separate extraction for amount numbers and words")
        print("• Enhanced name/depositor recognition")
        print("• Improved text preprocessing")
        print("• Better error handling and validation")
        print("\n📖 Check USAGE_GUIDE.md for detailed instructions")
        print("🔧 Ready to process real bank slips and forms!")
        
    except Exception as e:
        print(f"❌ Demo failed: {str(e)}")

if __name__ == "__main__":
    main()
