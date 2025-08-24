"""
Enhanced ICR Testing Script
===========================

This script uses improved preprocessing and pattern recognition to get better results
from your bank slip images.
"""

import os
from pathlib import Path
from enhanced_icr import EnhancedICRSystem
import json

def test_enhanced_icr():
    """Test the enhanced ICR system with user images"""
    
    print("🚀 Enhanced ICR System - Testing Your Images")
    print("=" * 60)
    
    # Initialize enhanced system
    icr = EnhancedICRSystem()
    
    # Setup paths
    input_folder = Path("input_images")
    output_folder = Path("output_data")
    
    # Create folders if needed
    input_folder.mkdir(exist_ok=True)
    output_folder.mkdir(exist_ok=True)
    
    # Find images
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = []
    for ext in supported_formats:
        image_files.extend(input_folder.glob(f"*{ext}"))
        image_files.extend(input_folder.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print(f"\n❌ No images found in '{input_folder}' folder!")
        print(f"📁 Please place your bank slip images in the folder.")
        return
    
    print(f"\n📸 Found {len(image_files)} image(s) to process")
    print("-" * 40)
    
    results = []
    
    for i, image_path in enumerate(image_files, 1):
        print(f"\n📋 Processing {i}/{len(image_files)}: {image_path.name}")
        print("=" * 50)
        
        # Process with enhanced system
        result = icr.process_image_enhanced(str(image_path))
        
        if result['success']:
            print(f"✅ SUCCESS! Extracted data from {image_path.name}")
            
            # Show raw text sample
            raw_text = result['raw_text']
            print(f"\n📝 Raw Text Sample (first 200 chars):")
            print(f"   {raw_text[:200]}{'...' if len(raw_text) > 200 else ''}")
            
            # Show structured data
            structured = result['structured_data']
            print(f"\n🏦 EXTRACTED BANK SLIP INFORMATION:")
            
            if structured['account_numbers']:
                print(f"   💳 Account Numbers: {', '.join(structured['account_numbers'])}")
            
            if structured['amounts_numeric']:
                print(f"   💰 Amounts (Numbers): {', '.join(structured['amounts_numeric'])}")
            
            if structured['amounts_words']:
                print(f"   💸 Amounts (Words): {', '.join(structured['amounts_words'])}")
            
            if structured['names']:
                print(f"   👤 Names: {', '.join(structured['names'])}")
            
            if structured['dates']:
                print(f"   📅 Dates: {', '.join(structured['dates'])}")
            
            if structured['reference_numbers']:
                print(f"   🔢 Reference Numbers: {', '.join(structured['reference_numbers'])}")
            
            if structured['bank_names']:
                print(f"   🏦 Banks: {', '.join(structured['bank_names'])}")
            
            if structured['branch_names']:
                print(f"   🏢 Branches: {', '.join(structured['branch_names'])}")
            
            # Check if we found any key information
            key_info_found = any([
                structured['account_numbers'],
                structured['amounts_numeric'],
                structured['amounts_words'],
                structured['names']
            ])
            
            if not key_info_found:
                print(f"   ⚠️  No key bank slip information detected")
                print(f"   💡 This might be due to:")
                print(f"      • Poor image quality or resolution")
                print(f"      • Handwritten text that's hard to read")
                print(f"      • Image not being a bank slip")
                print(f"      • Text in a different format than expected")
            
            # Save detailed results
            output_file = output_folder / f"enhanced_{image_path.stem}_results.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            # Save readable summary
            summary_file = output_folder / f"enhanced_{image_path.stem}_summary.txt"
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(f"Enhanced ICR Results for: {image_path.name}\n")
                f.write("=" * 60 + "\n\n")
                
                f.write(f"EXTRACTED BANK SLIP INFORMATION:\n")
                f.write("-" * 40 + "\n")
                
                if structured['account_numbers']:
                    f.write(f"💳 Account Numbers: {', '.join(structured['account_numbers'])}\n")
                
                if structured['amounts_numeric']:
                    f.write(f"💰 Amounts (Numbers): {', '.join(structured['amounts_numeric'])}\n")
                
                if structured['amounts_words']:
                    f.write(f"💸 Amounts (Words): {', '.join(structured['amounts_words'])}\n")
                
                if structured['names']:
                    f.write(f"👤 Names: {', '.join(structured['names'])}\n")
                
                if structured['dates']:
                    f.write(f"📅 Dates: {', '.join(structured['dates'])}\n")
                
                if structured['reference_numbers']:
                    f.write(f"🔢 Reference Numbers: {', '.join(structured['reference_numbers'])}\n")
                
                if structured['bank_names']:
                    f.write(f"🏦 Banks: {', '.join(structured['bank_names'])}\n")
                
                f.write(f"\nRAW TEXT:\n")
                f.write("-" * 40 + "\n")
                f.write(result['raw_text'])
            
            print(f"💾 Detailed results saved to: {output_file.name}")
            print(f"💾 Summary saved to: {summary_file.name}")
            
            results.append(result)
            
        else:
            print(f"❌ FAILED to process {image_path.name}")
            print(f"   Error: {result['error']}")
            results.append(result)
    
    # Final summary
    print("\n" + "=" * 60)
    print("📊 FINAL PROCESSING SUMMARY")
    print("=" * 60)
    
    successful = sum(1 for r in results if r['success'])
    failed = len(results) - successful
    
    print(f"✅ Successfully processed: {successful}/{len(results)} images")
    if failed > 0:
        print(f"❌ Failed: {failed}/{len(results)} images")
    
    if successful > 0:
        print(f"\n🎯 AGGREGATED FINDINGS:")
        all_accounts = set()
        all_amounts = set()
        all_names = set()
        
        for result in results:
            if result['success']:
                data = result['structured_data']
                all_accounts.update(data.get('account_numbers', []))
                all_amounts.update(data.get('amounts_numeric', []))
                all_names.update(data.get('names', []))
        
        if all_accounts:
            print(f"   💳 All Account Numbers: {', '.join(sorted(all_accounts))}")
        if all_amounts:
            print(f"   💰 All Amounts: {', '.join(sorted(all_amounts))}")
        if all_names:
            print(f"   👤 All Names: {', '.join(sorted(all_names))}")
        
        if not any([all_accounts, all_amounts, all_names]):
            print(f"   ⚠️  No key bank slip information found in any image")
            print(f"\n💡 TROUBLESHOOTING TIPS:")
            print(f"   • Check image quality - should be clear and high resolution")
            print(f"   • Ensure good lighting without shadows")
            print(f"   • Make sure text is readable to human eye")
            print(f"   • Try scanning at higher DPI (300+ recommended)")
            print(f"   • Ensure the document is a bank slip with standard fields")
    
    print(f"\n📁 Check '{output_folder}' folder for all results!")

if __name__ == "__main__":
    try:
        test_enhanced_icr()
    except KeyboardInterrupt:
        print("\n\n⏹️  Testing interrupted.")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n🎯 Press Enter to exit...")
