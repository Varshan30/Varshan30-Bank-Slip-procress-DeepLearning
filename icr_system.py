"""
Intelligent Character Recognition (ICR) System
==============================================

A comprehensive system for processing scanned handwritten forms (like bank slips),
extracting text accurately, and structuring it into a readable format.

Features:
- Image preprocessing for better OCR accuracy
- Text extraction using Tesseract OCR
- Data structuring and CSV export
- Support for various image formats
- Batch processing capabilities

Author: ICR System
Date: August 2025
"""

import cv2
import numpy as np
import pandas as pd
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import os
import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('icr_system.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ICRSystem:
    """
    Intelligent Character Recognition System for processing handwritten forms
    """
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Initialize the ICR System
        
        Args:
            tesseract_path: Path to Tesseract executable (if not in PATH)
        """
        self.setup_directories()
        
        # Set Tesseract path if provided
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
        
        # Enhanced OCR configuration for better bank slip recognition
        self.ocr_config = '--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,/:- '
        
        # Alternative OCR configs for different attempts
        self.ocr_configs = [
            '--oem 3 --psm 6',  # Default
            '--oem 3 --psm 4',  # Single column of text
            '--oem 3 --psm 8',  # Single word
            '--oem 3 --psm 7',  # Single text line
            '--oem 3 --psm 11', # Sparse text
            '--oem 3 --psm 12', # Sparse text with OSD
        ]
        
        # Enhanced field patterns for bank slips
        self.field_patterns = {
            'account_number': r'(?:account|acc|acct|a/c)[\s:.-]*(\d{8,16})',
            'amount_numbers': r'(?:amount|amt|sum|rs|₹|\$)[\s:.-]*(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)',
            'amount_words': r'(?:rupees|dollars|only)[\s]*((?:[a-zA-Z]+[\s]*){1,10})(?:only|rupees|dollars)?',
            'name': r'(?:name|depositor|account\s*holder|beneficiary)[\s:.-]*([A-Za-z\s]{2,30})',
            'date': r'(?:date)[\s:.-]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            'reference': r'(?:ref|reference|txn|transaction)[\s:.-]*([A-Z0-9]{4,12})'
        }
        
        # Enhanced amount detection patterns
        self.amount_patterns = {
            'numerical': [
                r'(?:rs|₹|\$)[\s]*(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)',
                r'(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)[\s]*(?:rs|₹|\$|rupees|dollars)',
                r'amount[\s:.-]+(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)',
                r'(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)[\s]*only'
            ],
            'words': [
                r'(?:rupees|dollars)[\s]+((?:[a-zA-Z]+[\s]*){1,15})(?:only)?',
                r'((?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|lakh|crore|million|billion)[\s]*){1,15}(?:rupees|dollars|only)?'
            ]
        }
        
        logger.info("ICR System initialized successfully")
    
    def setup_directories(self):
        """Create necessary directories for the ICR system"""
        self.directories = {
            'input': 'input_images',
            'processed': 'processed_images', 
            'output': 'output_data',
            'temp': 'temp_files'
        }
        
        for dir_name, dir_path in self.directories.items():
            os.makedirs(dir_path, exist_ok=True)
            logger.info(f"Directory '{dir_path}' ready")
    
    def preprocess_image(self, image_path: str) -> np.ndarray:
        """
        Preprocess image for better OCR accuracy with enhanced techniques
        
        Args:
            image_path: Path to input image
            
        Returns:
            Preprocessed image as numpy array
        """
        logger.info(f"Preprocessing image: {image_path}")
        
        # Read image
        img = cv2.imread(image_path)
        if img is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Multiple preprocessing approaches
        approaches = []
        
        # Approach 1: Standard preprocessing
        denoised = cv2.fastNlMeansDenoising(gray)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        enhanced = clahe.apply(denoised)
        blurred = cv2.GaussianBlur(enhanced, (1, 1), 0)
        binary1 = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        approaches.append(("standard", binary1))
        
        # Approach 2: OTSU thresholding
        blurred2 = cv2.GaussianBlur(gray, (5, 5), 0)
        _, binary2 = cv2.threshold(blurred2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        approaches.append(("otsu", binary2))
        
        # Approach 3: Morphological operations
        kernel = np.ones((2,2), np.uint8)
        morph = cv2.morphologyEx(binary1, cv2.MORPH_CLOSE, kernel)
        morph = cv2.morphologyEx(morph, cv2.MORPH_OPEN, kernel)
        approaches.append(("morphological", morph))
        
        # Choose the best approach (for now, use morphological)
        best_approach = approaches[2][1]  # Use morphological approach
        
        # Save preprocessed image
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        processed_path = os.path.join(self.directories['processed'], f"{base_name}_processed.png")
        cv2.imwrite(processed_path, best_approach)
        
        logger.info(f"Preprocessed image saved: {processed_path}")
        return best_approach
    
    def extract_text(self, image: np.ndarray) -> str:
        """
        Extract text from preprocessed image using Tesseract OCR with multiple attempts
        
        Args:
            image: Preprocessed image as numpy array
            
        Returns:
            Extracted text
        """
        try:
            # Convert numpy array to PIL Image
            pil_image = Image.fromarray(image)
            
            # Additional PIL enhancements
            enhancer = ImageEnhance.Contrast(pil_image)
            pil_image = enhancer.enhance(1.5)
            
            enhancer = ImageEnhance.Sharpness(pil_image)
            pil_image = enhancer.enhance(2.0)
            
            # Try multiple OCR configurations
            best_text = ""
            max_length = 0
            
            for config in self.ocr_configs:
                try:
                    text = pytesseract.image_to_string(pil_image, config=config)
                    text = text.strip()
                    
                    # Choose the result with most meaningful content
                    if len(text) > max_length and len(text) > 10:
                        best_text = text
                        max_length = len(text)
                        
                except Exception as e:
                    logger.warning(f"OCR config {config} failed: {str(e)}")
                    continue
            
            # If no good result, try with original config
            if not best_text:
                best_text = pytesseract.image_to_string(pil_image, config=self.ocr_config)
            
            logger.info(f"Text extraction completed. Length: {len(best_text)} characters")
            return best_text.strip()
            
        except Exception as e:
            logger.error(f"Error during text extraction: {str(e)}")
            return ""
    
    def extract_structured_data(self, text: str) -> Dict[str, str]:
        """
        Extract structured data from raw text using enhanced pattern matching
        
        Args:
            text: Raw extracted text
            
        Returns:
            Dictionary with structured field data
        """
        structured_data = {}
        
        # Clean text for better matching
        cleaned_text = text.lower().replace('\n', ' ').replace('\t', ' ')
        
        # Extract account number with enhanced patterns
        account_patterns = [
            r'(?:account|acc|acct|a/?c)[\s:.-]*(\d{8,16})',
            r'(\d{8,16})(?:\s*account|\s*acc|\s*a/?c)',
            r'account\s*number[\s:.-]*(\d{8,16})',
            r'a/?c\s*no[\s:.-]*(\d{8,16})',
            r'account[\s:.-]*(\d{8,16})',
            r'(\d{10,16})',  # Standalone long numbers likely to be account numbers
        ]
        
        account_number = ""
        for pattern in account_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            if matches:
                # Validate account number (should be 8-16 digits)
                candidate = matches[0]
                if len(candidate) >= 8 and candidate.isdigit():
                    account_number = candidate
                    break
        
        structured_data['account_number'] = account_number
        
        # Enhanced amount extraction (numbers)
        amount_patterns_enhanced = [
            r'(?:rs|₹|\$|amount)[\s:.-]*(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)',
            r'(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)[\s]*(?:rs|₹|\$|rupees|dollars|only)',
            r'amount[\s:.-]+(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)',
            r'(?:inr|usd)[\s]*(\d{1,8}(?:[,.]?\d{1,3})*(?:\.\d{2})?)',
            r'(\d{1,6}\.\d{2})(?=\s|$)',  # Decimal amounts
            r'(\d{4,8})(?=\s|$)',  # Large whole numbers
        ]
        
        amount_numbers = ""
        for pattern in amount_patterns_enhanced:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            if matches:
                amount_numbers = matches[0].replace(',', '')  # Remove commas
                break
        structured_data['amount_numbers'] = amount_numbers
        
        # Enhanced amount in words extraction
        amount_word_patterns = [
            r'(?:rupees|dollars)[\s]+((?:(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|lakh|crore|million|billion|and|only)[\s]*){1,20})',
            r'(?:in\s*words?)[\s:.-]*((?:(?:[a-zA-Z]+[\s]*){1,15}))(?:only|rupees|dollars)?',
            r'((?:(?:one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|thousand|lakh|crore|million|billion)[\s]*){2,15})',
        ]
        
        amount_words = ""
        for pattern in amount_word_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            if matches:
                candidate = matches[0].strip()
                # Filter out common non-amount words
                if len(candidate) > 10 and not any(word in candidate.lower() for word in ['branch', 'bank', 'slip', 'deposit', 'account', 'signature']):
                    amount_words = candidate
                    break
        structured_data['amount_words'] = amount_words
        
        # Enhanced name extraction
        # Enhanced name extraction
        name_patterns_enhanced = [
            r'(?:name|depositor|account\s*holder|beneficiary|holder)[\s:.-]*([A-Za-z\s]{3,30})(?=\s*(?:amount|account|date|branch|$))',
            r'(?:mr|mrs|ms|dr)[\s.]*([A-Za-z\s]{3,30})(?=\s*(?:amount|account|date|branch|$))',
            r'depositor[\s:.-]*([A-Za-z\s]{3,30})',
            r'holder[\s:.-]*([A-Za-z\s]{3,30})',
            r'name[\s:.-]*([A-Za-z\s]{3,30})(?=\s*(?:amount|account|date|branch|mobile|$))',
        ]
        
        name = ""
        for pattern in name_patterns_enhanced:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            if matches:
                # Clean and validate the name
                candidate_name = matches[0].strip()
                # Remove common non-name words and validate
                words_to_exclude = ['branch', 'bank', 'slip', 'deposit', 'amount', 'account', 'number', 'date', 'reference', 'mobile', 'signature']
                if not any(word in candidate_name.lower() for word in words_to_exclude) and len(candidate_name) >= 3:
                    name = candidate_name
                    break
        structured_data['name'] = name
        
        # Extract other fields using original patterns
        for field_name, pattern in self.field_patterns.items():
            if field_name not in ['amount_numbers', 'amount_words', 'account_number', 'name']:
                matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
                if matches:
                    structured_data[field_name] = matches[0]
                else:
                    structured_data[field_name] = ""
        
        # Add raw text
        structured_data['raw_text'] = text
        structured_data['processed_timestamp'] = datetime.now().isoformat()
        
        logger.info(f"Enhanced extraction: Account={account_number}, Amount(num)={amount_numbers}, Amount(words)={amount_words}, Name={name}")
        return structured_data
    
    def process_single_image(self, image_path: str) -> Dict[str, str]:
        """
        Process a single image through the complete ICR pipeline
        
        Args:
            image_path: Path to image file
            
        Returns:
            Dictionary with extracted and structured data
        """
        logger.info(f"Processing image: {image_path}")
        
        try:
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            
            # Extract text
            raw_text = self.extract_text(processed_image)
            
            # Structure data
            structured_data = self.extract_structured_data(raw_text)
            structured_data['source_file'] = os.path.basename(image_path)
            
            return structured_data
            
        except Exception as e:
            logger.error(f"Error processing {image_path}: {str(e)}")
            return {
                'source_file': os.path.basename(image_path),
                'error': str(e),
                'processed_timestamp': datetime.now().isoformat()
            }
    
    def process_batch(self, input_directory: str = None) -> List[Dict[str, str]]:
        """
        Process multiple images in batch
        
        Args:
            input_directory: Directory containing images (default: input_images)
            
        Returns:
            List of dictionaries with processed data
        """
        if input_directory is None:
            input_directory = self.directories['input']
        
        # Supported image formats
        supported_formats = ('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')
        
        # Find all image files
        image_files = []
        for file in os.listdir(input_directory):
            if file.lower().endswith(supported_formats):
                image_files.append(os.path.join(input_directory, file))
        
        if not image_files:
            logger.warning(f"No image files found in {input_directory}")
            return []
        
        logger.info(f"Found {len(image_files)} images to process")
        
        # Process all images
        results = []
        for image_path in image_files:
            result = self.process_single_image(image_path)
            results.append(result)
        
        logger.info(f"Batch processing completed. Processed {len(results)} images")
        return results
    
    def save_results_csv(self, results: List[Dict[str, str]], filename: str = None) -> str:
        """
        Save processing results to CSV file
        
        Args:
            results: List of result dictionaries
            filename: Output filename (default: auto-generated)
            
        Returns:
            Path to saved CSV file
        """
        if not results:
            logger.warning("No results to save")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"icr_results_{timestamp}.csv"
        
        output_path = os.path.join(self.directories['output'], filename)
        
        # Create DataFrame and save
        df = pd.DataFrame(results)
        df.to_csv(output_path, index=False, encoding='utf-8')
        
        logger.info(f"Results saved to: {output_path}")
        return output_path
    
    def save_results_json(self, results: List[Dict[str, str]], filename: str = None) -> str:
        """
        Save processing results to JSON file
        
        Args:
            results: List of result dictionaries
            filename: Output filename (default: auto-generated)
            
        Returns:
            Path to saved JSON file
        """
        if not results:
            logger.warning("No results to save")
            return ""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"icr_results_{timestamp}.json"
        
        output_path = os.path.join(self.directories['output'], filename)
        
        # Save JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to: {output_path}")
        return output_path
    
    def display_results(self, results: List[Dict[str, str]]):
        """
        Display processing results in a formatted way
        
        Args:
            results: List of result dictionaries
        """
        print("\n" + "="*60)
        print("ICR PROCESSING RESULTS - ENHANCED BANK SLIP DETECTION")
        print("="*60)
        
        for i, result in enumerate(results, 1):
            print(f"\n--- Document {i}: {result.get('source_file', 'Unknown')} ---")
            
            if 'error' in result:
                print(f"❌ Error: {result['error']}")
                continue
            
            print(f"🏦 Account Number: {result.get('account_number', 'Not found')}")
            print(f"💰 Amount (Numbers): {result.get('amount_numbers', 'Not found')}")
            print(f"💬 Amount (Words): {result.get('amount_words', 'Not found')}")
            print(f"👤 Name/Depositor: {result.get('name', 'Not found')}")
            print(f"📅 Date: {result.get('date', 'Not found')}")
            print(f"🔗 Reference: {result.get('reference', 'Not found')}")
            
            if result.get('raw_text'):
                print(f"📝 Raw Text Preview: {result['raw_text'][:100]}...")
        
        print(f"\n✅ Total documents processed: {len(results)}")
        print("="*60)


def main():
    """Main function to run the ICR system"""
    parser = argparse.ArgumentParser(description='Intelligent Character Recognition System')
    parser.add_argument('--input', '-i', help='Input directory or single image file')
    parser.add_argument('--tesseract-path', help='Path to Tesseract executable')
    parser.add_argument('--output-format', choices=['csv', 'json', 'both'], 
                       default='both', help='Output format for results')
    parser.add_argument('--no-display', action='store_true', 
                       help='Skip displaying results in console')
    
    args = parser.parse_args()
    
    try:
        # Initialize ICR system
        icr = ICRSystem(tesseract_path=args.tesseract_path)
        
        # Process images
        if args.input and os.path.isfile(args.input):
            # Single file
            results = [icr.process_single_image(args.input)]
        else:
            # Batch processing
            results = icr.process_batch(args.input)
        
        if not results:
            print("No images processed. Please check input directory.")
            return
        
        # Display results
        if not args.no_display:
            icr.display_results(results)
        
        # Save results
        if args.output_format in ['csv', 'both']:
            csv_path = icr.save_results_csv(results)
            print(f"\n📊 CSV results saved: {csv_path}")
        
        if args.output_format in ['json', 'both']:
            json_path = icr.save_results_json(results)
            print(f"📄 JSON results saved: {json_path}")
        
        print("\n🎉 ICR processing completed successfully!")
        
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
