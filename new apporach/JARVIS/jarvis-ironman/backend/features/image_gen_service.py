"""
Image Generation Service - Generate images using Stable Diffusion (simplified)
Note: For full Stable Diffusion, use Hugging Face Inference API (free tier)
"""
import requests
import base64
from typing import Dict
import os
from datetime import datetime

class ImageGenService:
    def __init__(self):
        """Initialize image generation service"""
        self.output_dir = "generated_images"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Using Hugging Face Inference API (free)
        self.api_url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
        self.api_key = os.getenv("HUGGINGFACE_API_KEY", "")  # Optional, works without key but slower
        
        print("[ImageGenService] Initialized")
    
    def generate_image(self, prompt: str, negative_prompt: str = "") -> Dict:
        """
        Generate image from text prompt using Hugging Face API (free)
        """
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            payload = {
                "inputs": prompt,
            }
            
            if negative_prompt:
                payload["negative_prompt"] = negative_prompt
            
            # Call API
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=60)
            
            if response.status_code == 200:
                # Save image
                filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                filepath = os.path.join(self.output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                # Convert to base64 for frontend
                image_base64 = base64.b64encode(response.content).decode('utf-8')
                
                return {
                    "success": True,
                    "filepath": filepath,
                    "filename": filename,
                    "image_base64": f"data:image/png;base64,{image_base64}"
                }
            elif response.status_code == 503:
                return {
                    "success": False,
                    "error": "Model is loading, please try again in a few seconds"
                }
            else:
                return {
                    "success": False,
                    "error": f"API error: {response.status_code}"
                }
            
        except requests.Timeout:
            return {"success": False, "error": "Request timeout - model may be loading"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_simple_placeholder(self, text: str, width: int = 512, height: int = 512) -> Dict:
        """
        Generate a simple placeholder image (fallback when API is unavailable)
        """
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create image
            img = Image.new('RGB', (width, height), color=(30, 30, 30))
            draw = ImageDraw.Draw(img)
            
            # Add text
            try:
                font = ImageFont.truetype("arial.ttf", 24)
            except:
                font = ImageFont.load_default()
            
            # Center text
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            position = ((width - text_width) // 2, (height - text_height) // 2)
            
            draw.text(position, text, fill=(255, 184, 0), font=font)
            
            # Save
            filename = f"placeholder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join(self.output_dir, filename)
            img.save(filepath)
            
            # Convert to base64
            import io
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "image_base64": f"data:image/png;base64,{image_base64}",
                "note": "Placeholder image (AI model unavailable)"
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
