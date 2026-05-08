"""
Intent Detection and Feature Execution
Add this to jarvis_ai.py to detect and execute features
"""
import re
from typing import Dict, Optional, Tuple

class FeatureDetector:
    """Detect user intent and execute appropriate features"""
    
    def __init__(self, jarvis_ai):
        self.jarvis = jarvis_ai
    
    def detect_and_execute(self, message: str, image_data: Optional[bytes] = None) -> Tuple[bool, Optional[Dict]]:
        """
        Detect intent and execute feature if applicable
        Returns: (feature_executed, result_data)
        """
        message_lower = message.lower()
        
        # OCR Detection
        if any(keyword in message_lower for keyword in ['extract text', 'read text', 'ocr', 'read image']):
            print(f"[FeatureDetector] OCR detected. image_data: {len(image_data) if image_data else 'None'} bytes")
            print(f"[FeatureDetector] Has vision service: {hasattr(self.jarvis, 'vision') and self.jarvis.vision is not None}")
            if image_data and hasattr(self.jarvis, 'vision') and self.jarvis.vision:
                print(f"[FeatureDetector] Calling vision service for OCR...")
                result = self.jarvis.vision.extract_text_from_image(image_data)
                print(f"[FeatureDetector] OCR result: {result}")
                return True, result
            return True, {"success": False, "error": "Please upload an image"}
        
        # Image Generation Detection
        if any(keyword in message_lower for keyword in ['generate image', 'create image', 'draw', 'create picture']):
            if hasattr(self.jarvis, 'image_gen'):
                # Extract prompt (everything after the command)
                prompt = re.sub(r'(generate|create|draw)\s+(image|picture)\s+(of|showing)?\s*', '', message_lower, flags=re.IGNORECASE)
                result = self.jarvis.image_gen.generate_image(prompt.strip())
                return True, result
            return True, {"success": False, "error": "Image generation not available"}
        
        # PowerPoint Detection
        if any(keyword in message_lower for keyword in ['create presentation', 'make powerpoint', 'generate slides', 'create ppt']):
            if hasattr(self.jarvis, 'ppt'):
                # Extract topic
                topic = re.sub(r'(create|make|generate)\s+(presentation|powerpoint|slides|ppt)\s+(about|on)?\s*', '', message_lower, flags=re.IGNORECASE)
                result = self.jarvis.ppt.create_from_text(message, title=topic.strip().title())
                return True, result
            return True, {"success": False, "error": "PowerPoint generation not available"}
        
        # Web Scraping Detection
        if any(keyword in message_lower for keyword in ['scrape', 'extract data from', 'get data from']):
            if hasattr(self.jarvis, 'scraper'):
                # Extract URL
                url_match = re.search(r'https?://[^\s]+|www\.[^\s]+|[a-zA-Z0-9-]+\.[a-z]{2,}', message)
                if url_match:
                    url = url_match.group(0)
                    if not url.startswith('http'):
                        url = 'https://' + url
                    result = self.jarvis.scraper.scrape_url(url)
                    return True, result
                return True, {"success": False, "error": "Please provide a URL"}
            return True, {"success": False, "error": "Web scraping not available"}
        
        # Object Detection
        if any(keyword in message_lower for keyword in ['detect objects', 'what objects', 'identify objects', "what's in"]):
            if image_data and hasattr(self.jarvis, 'vision') and self.jarvis.vision:
                result = self.jarvis.vision.detect_objects(image_data)
                return True, result
            return True, {"success": False, "error": "Please upload an image"}
        
        # Screenshot
        if 'screenshot' in message_lower or 'take screenshot' in message_lower:
            if hasattr(self.jarvis, 'automation'):
                result = self.jarvis.automation.screenshot()
                return True, result
            return True, {"success": False, "error": "Automation not available"}
        
        # File Operations
        if 'organize files' in message_lower:
            if hasattr(self.jarvis, 'automation'):
                # Extract directory
                dir_match = re.search(r'in\s+([^\s]+)', message_lower)
                directory = dir_match.group(1) if dir_match else "."
                result = self.jarvis.automation.organize_files(directory)
                return True, result
            return True, {"success": False, "error": "Automation not available"}
        
        # Data Analysis
        if 'analyze' in message_lower and 'numbers' in message_lower:
            if hasattr(self.jarvis, 'ml'):
                # Extract numbers
                numbers = re.findall(r'-?\d+\.?\d*', message)
                if numbers:
                    data = [float(n) for n in numbers]
                    result = self.jarvis.ml.analyze_data(data)
                    return True, result
                return True, {"success": False, "error": "No numbers found"}
            return True, {"success": False, "error": "ML not available"}
        
        # No feature detected
        return False, None
