"""
ICR System Test Script
=====================

This script tests the ICR system installation and basic functionality.
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test if all required packages can be imported"""
    print("🔍 Testing package imports...")
    
    test_results = {}
    packages = {
        'cv2': 'OpenCV',
        'numpy': 'NumPy', 
        'pandas': 'Pandas',
        'pytesseract': 'Tesseract Python',
        'PIL': 'Pillow (PIL)'
    }
    
    for package, name in packages.items():
        try:
            if package == 'PIL':
                from PIL import Image
            else:
                __import__(package)
            test_results[name] = "✅ OK"
        except ImportError as e:
            test_results[name] = f"❌ FAILED: {str(e)}"
    
    return test_results

def test_tesseract():
    """Test Tesseract OCR installation"""
    print("🔍 Testing Tesseract OCR...")
    
    try:
        import pytesseract
        from PIL import Image
        import numpy as np
        
        # Create a simple test image with text
        img_array = np.ones((100, 300, 3), dtype=np.uint8) * 255
        test_img = Image.fromarray(img_array)
        
        # Try to get Tesseract version
        version = pytesseract.get_tesseract_version()
        return f"✅ OK - Version: {version}"
        
    except Exception as e:
        return f"❌ FAILED: {str(e)}"

def test_opencv():
    """Test OpenCV functionality"""
    print("🔍 Testing OpenCV...")
    
    try:
        import cv2
        import numpy as np
        
        # Create a test image
        test_img = np.ones((100, 100), dtype=np.uint8) * 255
        
        # Test basic OpenCV operations
        blurred = cv2.GaussianBlur(test_img, (5, 5), 0)
        binary = cv2.threshold(test_img, 127, 255, cv2.THRESH_BINARY)[1]
        
        return f"✅ OK - Version: {cv2.__version__}"
        
    except Exception as e:
        return f"❌ FAILED: {str(e)}"

def test_directories():
    """Test if project directories exist"""
    print("🔍 Testing project structure...")
    
    required_dirs = [
        'input_images',
        'processed_images', 
        'output_data',
        'temp_files'
    ]
    
    results = {}
    for directory in required_dirs:
        if os.path.exists(directory):
            results[directory] = "✅ OK"
        else:
            results[directory] = "❌ MISSING"
    
    return results

def create_sample_test_image():
    """Create a simple test image for OCR testing"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import os
        
        # Create white image
        img = Image.new('RGB', (400, 200), color='white')
        draw = ImageDraw.Draw(img)
        
        # Add some test text
        test_text = [
            "Account: 1234567890",
            "Amount: 1500.75", 
            "Date: 24/08/2025",
            "Reference: ABC123XYZ"
        ]
        
        y_pos = 20
        for text in test_text:
            draw.text((20, y_pos), text, fill='black')
            y_pos += 30
        
        # Save to input directory
        os.makedirs('input_images', exist_ok=True)
        sample_path = os.path.join('input_images', 'test_sample.png')
        img.save(sample_path)
        
        return f"✅ Sample image created: {sample_path}"
        
    except Exception as e:
        return f"❌ Failed to create sample: {str(e)}"

def run_basic_icr_test():
    """Run a basic ICR test if everything is working"""
    try:
        # Import the ICR system
        from icr_system import ICRSystem
        
        # Create test instance
        icr = ICRSystem()
        
        # Check if sample image exists
        sample_path = os.path.join('input_images', 'test_sample.png')
        if os.path.exists(sample_path):
            print(f"🧪 Running ICR test on: {sample_path}")
            result = icr.process_single_image(sample_path)
            return f"✅ ICR test completed - Found {len(result)} fields"
        else:
            return "⚠️  No test image available for ICR test"
            
    except Exception as e:
        return f"❌ ICR test failed: {str(e)}"

def main():
    """Main test function"""
    print("🧪 ICR System Test Suite")
    print("=" * 50)
    print(f"Test started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test imports
    import_results = test_imports()
    print("📦 Package Import Tests:")
    for package, result in import_results.items():
        print(f"  {package}: {result}")
    print()
    
    # Test Tesseract
    tesseract_result = test_tesseract()
    print(f"🔤 Tesseract OCR: {tesseract_result}")
    print()
    
    # Test OpenCV
    opencv_result = test_opencv()
    print(f"👁️  OpenCV: {opencv_result}")
    print()
    
    # Test directories
    dir_results = test_directories()
    print("📁 Directory Structure:")
    for directory, result in dir_results.items():
        print(f"  {directory}/: {result}")
    print()
    
    # Create sample image
    sample_result = create_sample_test_image()
    print(f"🖼️  Sample Image: {sample_result}")
    print()
    
    # Run basic ICR test
    icr_result = run_basic_icr_test()
    print(f"🤖 ICR System: {icr_result}")
    print()
    
    # Summary
    print("=" * 50)
    all_passed = all("✅" in str(result) for result in [
        *import_results.values(),
        tesseract_result,
        opencv_result,
        *dir_results.values(),
        sample_result
    ])
    
    if all_passed:
        print("🎉 All tests passed! ICR system is ready to use.")
        print("\n📋 Next steps:")
        print("1. Add your scanned forms to input_images/ folder")
        print("2. Run: python icr_system.py")
        print("3. Check results in output_data/ folder")
    else:
        print("⚠️  Some tests failed. Please check the installation.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure virtual environment is activated")
        print("2. Install Tesseract OCR on your system")
        print("3. Run: pip install -r requirements.txt")
    
    print(f"\nTest completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
