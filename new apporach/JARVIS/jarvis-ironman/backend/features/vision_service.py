"""
Object Detection Service - Detect objects using YOLOv8
"""
from ultralytics import YOLO
import cv2
import numpy as np
import base64
from typing import Dict, List
import os

class VisionService:
    def __init__(self):
        """Initialize vision service"""
        self.model = None
        self.model_name = "yolov8n.pt"  # Nano model (fastest, free)
        print("[VisionService] Initialized")
    
    def _load_model(self):
        """Lazy load YOLO model"""
        if self.model is None:
            print(f"[VisionService] Loading {self.model_name}...")
            self.model = YOLO(self.model_name)
            print("[VisionService] Model loaded")
    
    def detect_objects(self, image_data: bytes, confidence: float = 0.5) -> Dict:
        """Detect objects in image"""
        try:
            self._load_model()
            
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            # Perform detection
            results = self.model(image, conf=confidence)
            
            # Extract detections
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    detection = {
                        "class": result.names[int(box.cls[0])],
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist()  # [x1, y1, x2, y2]
                    }
                    detections.append(detection)
            
            return {
                "success": True,
                "detections": detections,
                "count": len(detections)
            }
            
        except Exception as e:
            print(f"[VisionService] Error: {e}")
            return {"success": False, "error": str(e)}
    
    def detect_from_base64(self, base64_image: str, confidence: float = 0.5) -> Dict:
        """Detect objects from base64 encoded image"""
        try:
            # Remove data URL prefix if present
            if "base64," in base64_image:
                base64_image = base64_image.split("base64,")[1]
            
            # Decode base64
            image_data = base64.b64decode(base64_image)
            
            return self.detect_objects(image_data, confidence)
            
        except Exception as e:
            return {"success": False, "error": f"Base64 decode error: {str(e)}"}
    
    def detect_from_camera(self, camera_index: int = 0, confidence: float = 0.5) -> Dict:
        """Detect objects from camera feed (single frame)"""
        try:
            self._load_model()
            
            # Capture frame from camera
            cap = cv2.VideoCapture(camera_index)
            ret, frame = cap.read()
            cap.release()
            
            if not ret:
                return {"success": False, "error": "Failed to capture frame"}
            
            # Perform detection
            results = self.model(frame, conf=confidence)
            
            # Extract detections
            detections = []
            for result in results:
                boxes = result.boxes
                for box in boxes:
                    detection = {
                        "class": result.names[int(box.cls[0])],
                        "confidence": float(box.conf[0]),
                        "bbox": box.xyxy[0].tolist()
                    }
                    detections.append(detection)
            
            return {
                "success": True,
                "detections": detections,
                "count": len(detections)
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_available_classes(self) -> Dict:
        """Get list of classes the model can detect"""
        try:
            self._load_model()
            
            return {
                "success": True,
                "classes": list(self.model.names.values())
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
