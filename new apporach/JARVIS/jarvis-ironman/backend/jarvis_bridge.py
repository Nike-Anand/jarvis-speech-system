"""
JARVIS Bridge - Integration with existing JARVIS codebase
"""
import sys
import os

# Add existing JARVIS to path
EXISTING_JARVIS_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "JARVIS")
sys.path.insert(0, EXISTING_JARVIS_PATH)

from Jarvis import JarvisAssistant


class JarvisBridge:
    """Bridge to existing JARVIS functionality"""
    
    def __init__(self):
        """Initialize connection to existing JARVIS"""
        try:
            self.jarvis = JarvisAssistant()
            self.available = True
            print("[JarvisBridge] Successfully connected to existing JARVIS")
        except Exception as e:
            print(f"[JarvisBridge] Error initializing JARVIS: {e}")
            self.jarvis = None
            self.available = False
    
    def speak(self, text):
        """Use JARVIS TTS (Soprano)"""
        if self.available and self.jarvis:
            return self.jarvis.tts(text)
        return False
    
    def get_time(self):
        """Get current time"""
        if self.available and self.jarvis:
            return self.jarvis.tell_time()
        return None
    
    def get_date(self):
        """Get current date"""
        if self.available and self.jarvis:
            return self.jarvis.tell_me_date()
        return None
    
    def get_weather(self, city):
        """Get weather for a city"""
        if self.available and self.jarvis:
            return self.jarvis.weather(city)
        return None
    
    def get_news(self):
        """Get top news headlines"""
        if self.available and self.jarvis:
            return self.jarvis.news()
        return None
    
    def search_wikipedia(self, topic):
        """Search Wikipedia"""
        if self.available and self.jarvis:
            return self.jarvis.tell_me(topic)
        return None
    
    def get_system_stats(self):
        """Get system statistics"""
        if self.available and self.jarvis:
            return self.jarvis.system_info()
        return None
    
    def open_website(self, domain):
        """Open a website"""
        if self.available and self.jarvis:
            return self.jarvis.website_opener(domain)
        return False
    
    def launch_app(self, app_path):
        """Launch an application"""
        if self.available and self.jarvis:
            return self.jarvis.launch_any_app(app_path)
        return False
    
    def google_search(self, query):
        """Perform Google search"""
        if self.available and self.jarvis:
            return self.jarvis.search_anything_google(query)
        return False
    
    def take_note(self, text):
        """Take a note"""
        if self.available and self.jarvis:
            return self.jarvis.take_note(text)
        return False
    
    def get_location(self, location):
        """Get location information"""
        if self.available and self.jarvis:
            return self.jarvis.location(location)
        return None
    
    def get_my_location(self):
        """Get current location"""
        if self.available and self.jarvis:
            return self.jarvis.my_location()
        return None
    
    def listen(self):
        """Listen for voice input"""
        if self.available and self.jarvis:
            return self.jarvis.mic_input()
        return None
