"""
ICR Image Diagnostic Tool
=========================

This tool helps diagnose issues with your images and provides recommendations
for improving OCR results.
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path
import pytesseract

def analyze_image_quality(image_path):
    """Analyze image quality and provide recommendations"""
    
    print(f"\n🔍 Analyzing: {Path(image_path).name}")
    print("-" * 50)
    
    try:
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            print("❌ Could not load image. Check file format.")
            return
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Basic image properties
        height, width = gray.shape
        print(f"📏 Dimensions: {width} x {height} pixels")
        
        # Check resolution
        if width < 800 or height < 600:
            print("⚠️  Low resolution detected - recommend higher resolution (1200x900+)")
        else:
            print("✅ Good resolution")
        
        # Check brightness
        mean_brightness = np.mean(gray)
        print(f"💡 Average brightness: {mean_brightness:.1f}/255")
        
        if mean_brightness < 50:
            print("⚠️  Image too dark - increase brightness")
        elif mean_brightness > 200:
            print("⚠️  Image too bright - might lose text detail")
        else:
            print("✅ Good brightness level")
        
        # Check contrast
        contrast = np.std(gray)
        print(f"🎨 Contrast level: {contrast:.1f}")
        
        if contrast < 30:
            print("⚠️  Low contrast - text might not be clear")
        else:
            print("✅ Good contrast")
        
        # Check for blur
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        print(f"🔍 Sharpness score: {laplacian_var:.1f}")
        
        if laplacian_var < 100:
            print("⚠️  Image appears blurry - try better focus")
        else:
            print("✅ Image appears sharp")
        
        # Try quick OCR test
        print(f"\n🤖 Quick OCR Test:")
        try:
            # Basic preprocessing
            _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # Extract text
            text = pytesseract.image_to_string(thresh).strip()
            
            if text:
                print(f"✅ OCR detected text ({len(text)} characters)")
                if len(text) > 50:
                    print(f"   Sample: {text[:50]}...")
                else:
                    print(f"   Text: {text}")
            else:
                print("❌ No text detected by OCR")
                
            # Check OCR confidence
            data = pytesseract.image_to_data(thresh, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            
            if confidences:
                avg_conf = sum(confidences) / len(confidences)
                print(f"📊 OCR confidence: {avg_conf:.1f}%")
                
                if avg_conf < 50:
                    print("⚠️  Low OCR confidence - image quality issues")
                else:
                    print("✅ Good OCR confidence")
            
        except Exception as e:
            print(f"❌ OCR test failed: {str(e)}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if width < 800 or height < 600:
            print("   • Scan/photo at higher resolution (minimum 300 DPI)")
        
        if mean_brightness < 50:
            print("   • Increase lighting or image brightness")
        elif mean_brightness > 200:
            print("   • Reduce overexposure or brightness")
        
        if contrast < 30:
            print("   • Improve contrast between text and background")
        
        if laplacian_var < 100:
            print("   • Ensure camera is in focus")
            print("   • Hold camera steady or use tripod")
        
        if not text or len(text) < 20:
            print("   • Check if image contains readable text")
            print("   • Ensure text is not too small")
            print("   • Try different angles or lighting")
        
        print("   • For best results: clear, high-contrast, well-lit images")
        
    except Exception as e:
        print(f"❌ Error analyzing image: {str(e)}")

def diagnose_all_images():
    """Diagnose all images in input folder"""
    
    print("🔧 ICR Image Quality Diagnostic Tool")
    print("=" * 60)
    
    input_folder = Path("input_images")
    
    if not input_folder.exists():
        print("❌ input_images folder not found!")
        return
    
    # Find images
    supported_formats = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif'}
    image_files = []
    for ext in supported_formats:
        image_files.extend(input_folder.glob(f"*{ext}"))
        image_files.extend(input_folder.glob(f"*{ext.upper()}"))
    
    if not image_files:
        print("❌ No images found in input_images folder!")
        return
    
    print(f"📸 Found {len(image_files)} image(s) to analyze")
    
    for image_path in image_files:
        analyze_image_quality(str(image_path))
    
    print(f"\n" + "=" * 60)
    print("🎯 GENERAL TIPS FOR BETTER OCR RESULTS:")
    print("=" * 60)
    print("• Use high resolution (300+ DPI)")
    print("• Ensure good, even lighting")
    print("• Keep document flat and straight") 
    print("• Make sure camera is in focus")
    print("• Use good contrast between text and background")
    print("• Avoid shadows and glare")
    print("• Text should be clearly readable to human eye")

if __name__ == "__main__":
    try:
        diagnose_all_images()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    
    input("\n🎯 Press Enter to exit...")
