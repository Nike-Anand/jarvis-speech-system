import pyttsx3
import sys

print("Testing TTS engine...")

try:
    # Initialize TTS engine
    engine = pyttsx3.init('sapi5')
    print("TTS engine initialized successfully")
    
    # Set properties
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)
        print(f"Voice set to: {voices[0].id}")
    
    engine.setProperty('rate', 200)
    engine.setProperty('volume', 0.9)
    print("TTS properties set")
    
    # Test speech
    print("Testing speech...")
    engine.say("Hello, this is a test")
    engine.runAndWait()
    print("Speech test completed")
    
except Exception as e:
    print(f"TTS Error: {e}")
    print("TTS engine failed to initialize or speak")

print("Test finished")