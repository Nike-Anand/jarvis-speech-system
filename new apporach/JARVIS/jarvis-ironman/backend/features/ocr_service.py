"""
OCR Service - Extract text from images using Tesseract (and optionally EasyOCR)
"""
import pytesseract
from PIL import Image
import io
import base64
from typing import Dict, List, Optional

# Try to import EasyOCR (optional)
try:
    import easyocr
    EASYOCR_AVAILABLE = True
except ImportError:
    EASYOCR_AVAILABLE = False
    print("[OCRService] EasyOCR not available, using Tesseract only")

class OCRService:
    def __init__(self):
        """Initialize OCR readers"""
        self.easyocr_reader = None
        self.supported_languages = ['en']  # Can add more: 'es', 'fr', 'de, etc.
        self.easyocr_available = EASYOCR_AVAILABLE
        if self.easyocr_available:
            print("[OCRService] Initialized with EasyOCR + Tesseract")
        else:
            print("[OCRService] Initialized with Tesseract only")
    
    def _init_easyocr(self):
        """Lazy load EasyOCR (heavy model)"""
        if not self.easyocr_available:
            return # Cannot initialize if EasyOCR is not available

        if self.easyocr_reader is None:
            print("[OCRService] Loading EasyOCR model...")
            self.easyocr_reader = easyocr.Reader(self.supported_languages, gpu=False)
            print("[OCRService] EasyOCR model loaded")
    
    def extract_text_easyocr(self, image_data: bytes) -> Dict:
        """Extract text using EasyOCR (better for handwriting)"""
        try:
            self._init_easyocr()
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Perform OCR
            results = self.easyocr_reader.readtext(image_data)
            
            # Format results
            extracted_text = []
            full_text = ""
            
            for (bbox, text, confidence) in results:
                extracted_text.append({
                    "text": text,
                    "confidence": float(confidence),
                    "bbox": bbox
                })
                full_text += text + " "
            
            return {
                "success": True,
                "method": "easyocr",
                "full_text": full_text.strip(),
                "detailed_results": extracted_text,
                "total_words": len(full_text.split())
            }
            
        except Exception as e:
            print(f"[OCRService] EasyOCR error: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_text_tesseract(self, image_data: bytes) -> Dict:
        """Extract text using Tesseract (better for printed text)"""
        try:
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Perform OCR
            text = pytesseract.image_to_string(image)
            
            # Get detailed data
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            return {
                "success": True,
                "method": "tesseract",
                "full_text": text.strip(),
                "total_words": len(text.split()),
                "confidence": sum(data['conf']) / len(data['conf']) if data['conf'] else 0
            }
            
        except Exception as e:
            print(f"[OCRService] Tesseract error: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_text(self, image_data: bytes, method: str = "auto") -> Dict:
        """
        Extract text from image
        method: 'auto', 'easyocr', 'tesseract'
        """
        if method == "tesseract":
            return self.extract_text_tesseract(image_data)
        elif method == "easyocr":
            return self.extract_text_easyocr(image_data)
        else:
            # Auto: try EasyOCR first, fallback to Tesseract
            result = self.extract_text_easyocr(image_data)
            if not result.get("success"):
                result = self.extract_text_tesseract(image_data)
            return result
    
    def extract_from_base64(self, base64_image: str, method: str = "auto") -> Dict:
        """Extract text from base64 encoded image"""
        try:
            # Remove data URL prefix if present
            if "base64," in base64_image:
                base64_image = base64_image.split("base64,")[1]
            
            # Decode base64
            image_data = base64.b64decode(base64_image)
            
            return self.extract_text(image_data, method)
            
        except Exception as e:
            return {"success": False, "error": f"Base64 decode error: {str(e)}"}
