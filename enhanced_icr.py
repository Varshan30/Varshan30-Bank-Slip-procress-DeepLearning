"""
Enhanced ICR System with Better Preprocessing and Pattern Recognition
====================================================================

This improved version includes:
1. Multiple image preprocessing techniques
2. Enhanced pattern recognition for bank slips
3. OCR confidence checking
4. Manual field extraction assistance
"""

import cv2
import numpy as np
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
import re
from pathlib import Path
import json
from datetime import datetime

class EnhancedICRSystem:
    """Enhanced ICR System with improved preprocessing and pattern recognition"""
    
    def __init__(self):
        """Initialize the enhanced ICR system"""
        self.preprocessing_methods = [
            self._preprocess_standard,
            self._preprocess_high_contrast,
            self._preprocess_denoised,
            self._preprocess_sharpened,
            self._preprocess_dilated
        ]
    
    def _preprocess_standard(self, image_path):
        """Standard preprocessing"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    
    def _preprocess_high_contrast(self, image_path):
        """High contrast preprocessing"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Enhance contrast
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        enhanced = clahe.apply(gray)
        
        # Apply threshold
        _, thresh = cv2.threshold(enhanced, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    
    def _preprocess_denoised(self, image_path):
        """Denoised preprocessing"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Remove noise
        denoised = cv2.medianBlur(gray, 3)
        
        # Apply threshold
        _, thresh = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    
    def _preprocess_sharpened(self, image_path):
        """Sharpened preprocessing"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Sharpen image
        kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
        sharpened = cv2.filter2D(gray, -1, kernel)
        
        # Apply threshold
        _, thresh = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh
    
    def _preprocess_dilated(self, image_path):
        """Dilated preprocessing for better text connectivity"""
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Apply threshold first
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        # Dilate to connect text components
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(thresh, kernel, iterations=1)
        
        return dilated
    
    def extract_text_multiple_methods(self, image_path):
        """Extract text using multiple preprocessing methods"""
        best_text = ""
        best_confidence = 0
        all_results = []
        
        print(f"   🔍 Trying multiple OCR preprocessing methods...")
        
        for i, method in enumerate(self.preprocessing_methods):
            try:
                processed_img = method(image_path)
                
                # Try different OCR configurations
                configs = [
                    '--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz .,/-:',
                    '--psm 4',
                    '--psm 6',
                    '--psm 3',
                    '--psm 1'
                ]
                
                for config in configs:
                    try:
                        # Extract text with confidence
                        data = pytesseract.image_to_data(processed_img, config=config, output_type=pytesseract.Output.DICT)
                        
                        # Calculate average confidence
                        confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
                        avg_confidence = sum(confidences) / len(confidences) if confidences else 0
                        
                        # Extract text
                        text = pytesseract.image_to_string(processed_img, config=config).strip()
                        
                        if text and len(text) > 10:  # Only consider substantial text
                            all_results.append({
                                'method': f"Method {i+1}",
                                'config': config,
                                'text': text,
                                'confidence': avg_confidence,
                                'length': len(text)
                            })
                            
                            if avg_confidence > best_confidence:
                                best_confidence = avg_confidence
                                best_text = text
                                
                    except Exception as e:
                        continue
                        
            except Exception as e:
                print(f"     ⚠️  Method {i+1} failed: {str(e)}")
                continue
        
        print(f"   📊 Best OCR confidence: {best_confidence:.1f}%")
        return best_text, all_results
    
    def enhanced_pattern_extraction(self, text):
        """Enhanced pattern extraction for bank slip information"""
        results = {
            'account_numbers': [],
            'amounts_numeric': [],
            'amounts_words': [],
            'names': [],
            'dates': [],
            'reference_numbers': [],
            'bank_names': [],
            'branch_names': []
        }
        
        if not text:
            return results
        
        # Clean text
        cleaned_text = text.replace('\n', ' ').replace('\t', ' ')
        
        # Enhanced Account Number Patterns
        account_patterns = [
            r'(?:account|acc|acct|a/?c)[\s:.-]*(\d{8,18})',
            r'(\d{8,18})(?=\s|$|[^\d])',  # Standalone long numbers
            r'(?:sb|ca|od|cc|rd|tl|dl)[\s/]*no[\s.:]*(\d{6,16})',
            r'account[\s]*number[\s:.-]*(\d{6,16})',
            r'a/?c[\s]*no[\s:.-]*(\d{6,16})',
        ]
        
        for pattern in account_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 6 and match.isdigit():
                    results['account_numbers'].append(match)
        
        # Enhanced Amount Patterns (Numbers)
        amount_num_patterns = [
            r'(?:rs|₹|\$|amount|deposit)[\s:.-]*(\d{1,10}(?:[,.]?\d{1,3})*(?:\.\d{2})?)',
            r'(\d{1,10}(?:[,.]?\d{1,3})*(?:\.\d{2})?)[\s]*(?:rs|₹|\$|rupees|dollars|only)',
            r'(\d{1,6}\.\d{2})(?=\s|$)',
            r'(\d{4,10})(?=\s*/-|\s*only|\s*rs|\s*₹)',
            r'deposit[\s]*of[\s]*[₹$]?[\s]*(\d{1,10}(?:[,.]?\d{1,3})*)',
            r'amount[\s:.-]+(\d{1,10}(?:[,.]?\d{1,3})*)',
        ]
        
        for pattern in amount_num_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            for match in matches:
                clean_amount = match.replace(',', '')
                if clean_amount.replace('.', '').isdigit():
                    results['amounts_numeric'].append(match)
        
        # Enhanced Amount Patterns (Words)
        amount_word_patterns = [
            r'(?:rupees|dollars|rs\.?|usd)\s+([a-z\s]+?)(?:only|\.|\s*$)',
            r'([a-z\s]*(?:thousand|lakh|crore|hundred|million)[a-z\s]*?)(?:only|rupees|dollars)',
            r'amount\s*in\s*words[\s:.-]*([a-z\s]+?)(?:only|\.|\s*$)',
        ]
        
        for pattern in amount_word_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            for match in matches:
                if len(match.strip()) > 3:
                    results['amounts_words'].append(match.strip())
        
        # Enhanced Name Patterns
        name_patterns = [
            r'(?:name|pay\s*to|beneficiary)[\s:.-]*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'(?:mr|mrs|ms|dr)\.?\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\s*(?:account|acc)',
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, text)  # Use original text for names (case sensitive)
            for match in matches:
                if len(match.split()) >= 2:  # At least first and last name
                    results['names'].append(match)
        
        # Date Patterns
        date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
            r'(\d{1,2}\s+(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\s+\d{2,4})',
            r'date[\s:.-]*(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',
        ]
        
        for pattern in date_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            results['dates'].extend(matches)
        
        # Bank and Branch Names
        bank_patterns = [
            r'([\w\s]+bank)',
            r'(state\s+bank\s+of\s+\w+)',
            r'(hdfc|icici|sbi|axis|pnb|canara|union)[\s]*bank',
        ]
        
        for pattern in bank_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            results['bank_names'].extend(matches)
        
        # Reference Numbers
        ref_patterns = [
            r'(?:ref|reference|txn|transaction)[\s:.-]*([A-Z0-9]{6,20})',
            r'([A-Z]{3}\d{6,12})',
            r'(?:utr|rrn)[\s:.-]*([A-Z0-9]{8,16})',
        ]
        
        for pattern in ref_patterns:
            matches = re.findall(pattern, cleaned_text, re.IGNORECASE)
            results['reference_numbers'].extend(matches)
        
        # Remove duplicates and clean up
        for key in results:
            results[key] = list(set(results[key]))  # Remove duplicates
            results[key] = [item for item in results[key] if item.strip()]  # Remove empty
        
        return results
    
    def process_image_enhanced(self, image_path):
        """Process image with enhanced methods"""
        print(f"\n🔍 Enhanced processing: {Path(image_path).name}")
        
        try:
            # Extract text using multiple methods
            best_text, all_results = self.extract_text_multiple_methods(image_path)
            
            if not best_text:
                return {
                    'success': False,
                    'error': 'No text could be extracted from image',
                    'image': Path(image_path).name
                }
            
            print(f"   📝 Extracted text length: {len(best_text)} characters")
            
            # Enhanced pattern extraction
            structured_data = self.enhanced_pattern_extraction(best_text)
            
            # Count found items
            total_items = sum(len(v) for v in structured_data.values())
            print(f"   🎯 Found {total_items} structured data items")
            
            return {
                'success': True,
                'raw_text': best_text,
                'structured_data': structured_data,
                'all_ocr_results': all_results,
                'image': Path(image_path).name,
                'processing_timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'image': Path(image_path).name
            }
