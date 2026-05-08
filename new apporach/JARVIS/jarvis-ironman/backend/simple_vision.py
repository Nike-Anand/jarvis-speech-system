"""
Simple Vision Service using Ollama Vision Models (Qwen2-VL or Llama3.2-Vision)
No dependencies needed - uses Ollama directly!
"""
import ollama
import base64
from typing import Dict, Optional

class SimpleVisionService:
    def __init__(self, model: str = "minicpm-v:latest"):
        """Initialize with vision model"""
        self.model = model
        print(f"[VisionService] Initialized with {model}")
    
    def extract_text_from_image(self, image_data: bytes) -> Dict:
        """Extract text from image using vision model"""
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Ask vision model to extract text
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': 'Extract all text from this image. Only return the extracted text, nothing else.',
                    'images': [image_base64]
                }]
            )
            
            extracted_text = response['message']['content']
            
            return {
                "success": True,
                "full_text": extracted_text,
                "total_words": len(extracted_text.split()),
                "method": "vision_model"
            }
            
        except Exception as e:
            print(f"[VisionService] Error: {e}")
            return {"success": False, "error": str(e)}
    
    def detect_objects(self, image_data: bytes) -> Dict:
        """Detect objects in image using vision model"""
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Ask vision model to detect objects
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': 'List all objects you can see in this image. Format: object1, object2, object3',
                    'images': [image_base64]
                }]
            )
            
            objects_text = response['message']['content']
            objects = [obj.strip() for obj in objects_text.split(',')]
            
            return {
                "success": True,
                "count": len(objects),
                "detections": [{"class": obj} for obj in objects],
                "method": "vision_model"
            }
            
        except Exception as e:
            print(f"[VisionService] Error: {e}")
            return {"success": False, "error": str(e)}
    
    def describe_image(self, image_data: bytes) -> Dict:
        """Get detailed description of image"""
        try:
            # Convert image to base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            # Ask vision model to describe
            response = ollama.chat(
                model=self.model,
                messages=[{
                    'role': 'user',
                    'content': 'Describe this image in detail.',
                    'images': [image_base64]
                }]
            )
            
            description = response['message']['content']
            
            return {
                "success": True,
                "description": description,
                "method": "vision_model"
            }
            
        except Exception as e:
            print(f"[VisionService] Error: {e}")
            return {"success": False, "error": str(e)}
