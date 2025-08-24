"""
Enhanced ICR Test - Bank Slip Recognition
========================================

This script tests the enhanced ICR system with realistic bank slip data
focusing on account numbers, amounts (numbers and words), and names.
"""

import os
from datetime import datetime
from icr_system import ICRSystem

def create_realistic_bank_slip():
    """Create a realistic bank slip for testing"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a realistic bank slip
        img = Image.new('RGB', (800, 600), color='white')
        draw = ImageDraw.Draw(img)
        
        # Bank header
        draw.rectangle([(50, 20), (750, 80)], outline='black', width=2)
        draw.text((60, 30), "STATE BANK OF INDIA", fill='black')
        draw.text((60, 50), "DEPOSIT SLIP", fill='black')
        
        # Form fields with realistic data
        fields = [
            (80, 120, "Account Number: 123456789012"),
            (80, 160, "Account Holder: John Michael Smith"),
            (80, 200, "Amount in Numbers: Rs. 15,750.50"),
            (80, 240, "Amount in Words: Fifteen Thousand Seven Hundred Fifty Rupees and Fifty Paise Only"),
            (80, 280, "Date: 24/08/2025"),
            (80, 320, "Reference: TXN2025ABC789"),
            (80, 360, "Depositor Name: Sarah Wilson"),
            (80, 400, "Branch: Main Street Branch"),
            (80, 440, "Signature: ________________")
        ]
        
        for x, y, text in fields:
            draw.text((x, y), text, fill='black')
        
        # Add some decorative elements
        draw.line([(50, 100), (750, 100)], fill='black', width=1)
        draw.line([(50, 480), (750, 480)], fill='black', width=1)
        
        # Save sample
        os.makedirs('input_images', exist_ok=True)
        sample_path = os.path.join('input_images', 'realistic_bank_slip.png')
        img.save(sample_path)
        
        return sample_path
        
    except ImportError:
        print("⚠️  PIL not available - cannot create sample image")
        return None
    except Exception as e:
        print(f"❌ Error creating sample: {str(e)}")
        return None

def create_handwritten_style_slip():
    """Create a more handwritten-style bank slip"""
    try:
        from PIL import Image, ImageDraw
        
        img = Image.new('RGB', (700, 500), color='white')
        draw = ImageDraw.Draw(img)
        
        # Title
        draw.text((50, 20), "CASH DEPOSIT SLIP", fill='black')
        draw.line([(50, 45), (650, 45)], fill='black', width=2)
        
        # Handwritten-style fields
        fields = [
            (60, 80, "A/C No: 987654321098"),
            (60, 120, "Name: Mrs. Elizabeth Johnson"),
            (60, 160, "Amount: 25000.00"),
            (60, 200, "In Words: Twenty Five Thousand Rupees Only"),
            (60, 240, "Date: 24-08-2025"),
            (60, 280, "Ref No: REF987654"),
            (60, 320, "Mobile: 9876543210"),
            (60, 360, "Deposited By: Robert Johnson")
        ]
        
        for x, y, text in fields:
            draw.text((x, y), text, fill='black')
        
        sample_path = os.path.join('input_images', 'handwritten_slip.png')
        img.save(sample_path)
        
        return sample_path
        
    except Exception as e:
        print(f"❌ Error creating handwritten sample: {str(e)}")
        return None

def test_enhanced_extraction():
    """Test the enhanced extraction capabilities"""
    print("🧪 Enhanced ICR Bank Slip Test")
    print("=" * 50)
    
    # Create test samples
    sample1 = create_realistic_bank_slip()
    sample2 = create_handwritten_style_slip()
    
    if not sample1 and not sample2:
        print("❌ Could not create test samples")
        return
    
    # Initialize enhanced ICR system
    icr = ICRSystem()
    
    # Test samples
    samples = []
    if sample1:
        samples.append(sample1)
    if sample2:
        samples.append(sample2)
    
    print(f"\n📁 Created {len(samples)} test samples")
    
    # Process each sample
    for sample_path in samples:
        print(f"\n🤖 Processing: {os.path.basename(sample_path)}")
        print("-" * 40)
        
        result = icr.process_single_image(sample_path)
        
        # Display enhanced results
        print(f"🏦 Account Number: '{result.get('account_number', 'Not detected')}'")
        print(f"💰 Amount (Numbers): '{result.get('amount_numbers', 'Not detected')}'")
        print(f"💬 Amount (Words): '{result.get('amount_words', 'Not detected')}'")
        print(f"👤 Name: '{result.get('name', 'Not detected')}'")
        print(f"📅 Date: '{result.get('date', 'Not detected')}'")
        print(f"🔗 Reference: '{result.get('reference', 'Not detected')}'")
        
        print(f"\n📝 Raw OCR Text:")
        print(f"'{result.get('raw_text', '')[:200]}...'")
    
    print(f"\n✅ Enhanced extraction test completed!")
    print("\n📊 Results saved to output_data/ folder")

def main():
    """Main test function"""
    print("🎯 Enhanced ICR System - Bank Slip Recognition Test")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        test_enhanced_extraction()
        
        print("\n" + "=" * 60)
        print("🎉 Enhanced bank slip recognition test completed!")
        print("\n📚 Enhanced Features Tested:")
        print("• Account number detection with multiple patterns")
        print("• Amount extraction (both numbers and words)")
        print("• Name/depositor identification")
        print("• Improved pattern matching for bank slips")
        print("• Enhanced text preprocessing")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")

if __name__ == "__main__":
    main()
