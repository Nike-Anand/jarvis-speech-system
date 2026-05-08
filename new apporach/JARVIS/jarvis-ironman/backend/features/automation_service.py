"""
Task Automation Service - Automate tasks using pyautogui and schedule
"""
import pyautogui
import schedule
import time
from typing import Dict, List
import os
import shutil
from pathlib import Path

class AutomationService:
    def __init__(self):
        """Initialize automation service"""
        self.scheduled_tasks = []
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        print("[AutomationService] Initialized")
    
    def click_at(self, x: int, y: int) -> Dict:
        """Click at specific coordinates"""
        try:
            pyautogui.click(x, y)
            return {"success": True, "action": "click", "x": x, "y": y}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def type_text(self, text: str, interval: float = 0.1) -> Dict:
        """Type text with specified interval between keys"""
        try:
            pyautogui.write(text, interval=interval)
            return {"success": True, "action": "type", "text": text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def press_key(self, key: str) -> Dict:
        """Press a specific key"""
        try:
            pyautogui.press(key)
            return {"success": True, "action": "press", "key": key}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def hotkey(self, *keys) -> Dict:
        """Press multiple keys simultaneously"""
        try:
            pyautogui.hotkey(*keys)
            return {"success": True, "action": "hotkey", "keys": list(keys)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def screenshot(self, filepath: str = "screenshot.png") -> Dict:
        """Take a screenshot"""
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(filepath)
            return {"success": True, "filepath": filepath}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> Dict:
        """Move mouse to coordinates"""
        try:
            pyautogui.moveTo(x, y, duration=duration)
            return {"success": True, "x": x, "y": y}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # File Operations
    def create_folder(self, path: str) -> Dict:
        """Create a folder"""
        try:
            os.makedirs(path, exist_ok=True)
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def copy_file(self, src: str, dst: str) -> Dict:
        """Copy file from src to dst"""
        try:
            shutil.copy2(src, dst)
            return {"success": True, "src": src, "dst": dst}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def move_file(self, src: str, dst: str) -> Dict:
        """Move file from src to dst"""
        try:
            shutil.move(src, dst)
            return {"success": True, "src": src, "dst": dst}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def delete_file(self, path: str) -> Dict:
        """Delete a file"""
        try:
            os.remove(path)
            return {"success": True, "path": path}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_files(self, directory: str, pattern: str = "*") -> Dict:
        """List files in directory matching pattern"""
        try:
            path = Path(directory)
            files = [str(f) for f in path.glob(pattern)]
            return {"success": True, "files": files, "count": len(files)}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def organize_files(self, directory: str) -> Dict:
        """Organize files in directory by extension"""
        try:
            path = Path(directory)
            organized = {}
            
            for file in path.iterdir():
                if file.is_file():
                    ext = file.suffix[1:] if file.suffix else "no_extension"
                    ext_dir = path / ext
                    ext_dir.mkdir(exist_ok=True)
                    
                    new_path = ext_dir / file.name
                    file.rename(new_path)
                    
                    organized[ext] = organized.get(ext, 0) + 1
            
            return {"success": True, "organized": organized}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # Scheduling
    def schedule_task(self, task_name: str, interval: str, action: str) -> Dict:
        """
        Schedule a recurring task
        interval: 'daily', 'hourly', 'every_10_minutes', etc.
        """
        try:
            # This is a simplified version - full implementation would need a background worker
            self.scheduled_tasks.append({
                "name": task_name,
                "interval": interval,
                "action": action
            })
            
            return {
                "success": True,
                "task_name": task_name,
                "interval": interval,
                "message": "Task scheduled (background worker needed for execution)"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_scheduled_tasks(self) -> Dict:
        """Get list of scheduled tasks"""
        return {
            "success": True,
            "tasks": self.scheduled_tasks,
            "count": len(self.scheduled_tasks)
        }
