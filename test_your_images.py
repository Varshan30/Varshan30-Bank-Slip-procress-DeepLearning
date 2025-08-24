"""
Test ICR System with Your Own Images
===================================

This script allows you to easily test the ICR system with your own bank slip images.
Simply place your images in the 'input_images' folder and run this script.
"""

import os
import sys
from pathlib import Path
from icr_system import ICRSystem

def test_user_images():
    """Test ICR system with user's own images"""
    
    # Initialize the ICR system
    print("🔧 Initializing ICR System...")
    icr = ICRSystem()
    
    # Define paths
    input_folder = Path("input_images")
    output_folder = Path("output_data")
    processed_folder = Path("processed_images")
    
    # Create folders if they don't exist
    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)
    processed_folder.mkdir(exist_ok=True)
    
    # Supported image formats
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    
    # Find all images in input folder
    image_files = []
    for ext in supported_formats:
        image_files.extend(input_folder.glob(f"*{ext}"))
        image_files.extend(input_folder.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"\n❌ No images found in '{input_folder}' folder!")
        print(f"📁 Please place your bank slip images in the '{input_folder}' folder.")
        print(f"🖼️  Supported formats: {', '.join(supported_formats)}")
        print(f"\n💡 Example: Place 'bank_slip.jpg' in '{input_folder}' folder")
        return
    
    print(f"\n📸 Found {len(image_files)} image(s) to process:")
    for img in image_files:
        print(f"   • {img.name}")
    
    print(f"\n🚀 Starting OCR processing...")
    print("=" * 50)
    
    # Process each image
    results = []
    for i, image_path in enumerate(image_files, 1):
        print(f"\n📋 Processing Image {i}/{len(image_files)}: {image_path.name}")
        print("-" * 40)
        
        try:
            # Process the image
            result = icr.process_single_image(str(image_path))
            
            # Check if processing was successful (no error key means success)
            if result and 'error' not in result:
                # Display results
                print(f"✅ OCR Success!")
                
                # Get raw text by processing again to extract it
                try:
                    processed_img = icr.preprocess_image(str(image_path))
                    raw_text = icr.extract_text(processed_img)
                    
                    # Show extracted text
                    if raw_text:
                        print(f"\n📝 Raw Text Extracted:")
                        print(f"   {raw_text[:200]}{'...' if len(raw_text) > 200 else ''}")
                except:
                    raw_text = "Unable to extract raw text"
                
                # Show structured data
                print(f"\n🏦 Bank Slip Information Detected:")
                
                if result.get('account_number'):
                    print(f"   💳 Account Number: {result['account_number']}")
                
                if result.get('amount_numbers'):
                    print(f"   💰 Amount (Numbers): {result['amount_numbers']}")
                
                if result.get('amount_words'):
                    print(f"   💸 Amount (Words): {result['amount_words']}")
                
                if result.get('name'):
                    print(f"   👤 Name: {result['name']}")
                
                if result.get('date'):
                    print(f"   📅 Date: {result['date']}")
                
                if result.get('reference_number'):
                    print(f"   🔢 Reference Number: {result['reference_number']}")
                
                # Save results
                output_file = output_folder / f"{image_path.stem}_results.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(f"ICR Results for: {image_path.name}\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Raw Text:\n{raw_text}\n\n")
                    f.write("Structured Data:\n")
                    for key, value in result.items():
                        if key != 'source_file' and value:  # Skip empty values and source_file
                            f.write(f"{key}: {value}\n")
                
                print(f"💾 Results saved to: {output_file.name}")
                
                results.append({
                    'image': image_path.name,
                    'success': True,
                    'structured_data': result
                })
                
            else:
                print(f"❌ OCR Failed for {image_path.name}")
                error_msg = result.get('error', 'Unknown error') if result else 'No result returned'
                print(f"   Error: {error_msg}")
                
                results.append({
                    'image': image_path.name,
                    'success': False,
                    'error': error_msg
                })
        
        except Exception as e:
            print(f"❌ Error processing {image_path.name}: {str(e)}")
            results.append({
                'image': image_path.name,
                'success': False,
                'error': str(e)
            })
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 PROCESSING SUMMARY")
    print("=" * 50)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"✅ Successfully processed: {successful}/{len(results)} images")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(results)} images")
    
    # Show aggregated results
    if successful > 0:
        print(f"\n🎯 AGGREGATED RESULTS:")
        all_accounts = set()
        all_amounts_num = set()
        all_amounts_words = set()
        all_names = set()
        
        for result in results:
            if result['success'] and 'structured_data' in result:
                data = result['structured_data']
                if data.get('account_number'):
                    all_accounts.add(data['account_number'])
                if data.get('amount_numbers'):
                    all_amounts_num.add(data['amount_numbers'])
                if data.get('amount_words'):
                    all_amounts_words.add(data['amount_words'])
                if data.get('name'):
                    all_names.add(data['name'])
        
        if all_accounts:
            print(f"   💳 All Account Numbers Found: {', '.join(sorted(all_accounts))}")
        if all_amounts_num:
            print(f"   💰 All Numeric Amounts Found: {', '.join(sorted(all_amounts_num))}")
        if all_amounts_words:
            print(f"   💸 All Word Amounts Found: {', '.join(sorted(all_amounts_words))}")
        if all_names:
            print(f"   👤 All Names Found: {', '.join(sorted(all_names))}")
    
    print(f"\n📁 Check the '{output_folder}' folder for detailed results!")
    print(f"🖼️  Processed images are saved in '{processed_folder}' folder.")

if __name__ == "__main__":
    print("🏦 Bank Slip ICR Testing with Your Images")
    print("=" * 50)
    print("📌 Make sure to place your images in the 'input_images' folder first!")
    print()
    
    try:
        test_user_images()
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n🎯 Press Enter to exit...")
