import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

import speech_recognition as sr
import pyttsx3
import datetime
import random

# Simple TTS setup
engine = pyttsx3.init('sapi5')
engine.setProperty('rate', 180)
engine.setProperty('volume', 0.9)

def speak(text):
    print(f"JARVIS: {text}")
    engine.say(text)
    engine.runAndWait()

def better_listen():
    """Optimized for your audio setup"""
    r = sr.Recognizer()
    
    # Settings optimized for Bluetooth/multiple devices
    r.energy_threshold = 4000  # Higher threshold for noisy Bluetooth
    r.pause_threshold = 1.0    # Longer pause for Bluetooth delay
    r.phrase_threshold = 0.5   # More sensitive phrase detection
    
    try:
        # Use default microphone (usually the best one)
        with sr.Microphone(device_index=None) as source:
            print("Calibrating microphone... (stay quiet for 3 seconds)")
            r.adjust_for_ambient_noise(source, duration=3)
            print(f"Energy threshold: {r.energy_threshold}")
            
            print("Speak clearly now...")
            # Longer timeout for Bluetooth devices
            audio = r.listen(source, timeout=15, phrase_time_limit=6)
            
        print("Processing...")
        
        # Try recognition
        try:
            text = r.recognize_google(audio, language='en-US')
            print(f"✅ You said: '{text}'")
            return text.lower()
        except sr.UnknownValueError:
            print("❌ Couldn't understand - try speaking louder and clearer")
            return None
        except sr.RequestError as e:
            print(f"❌ Google service error: {e}")
            return None
            
    except sr.WaitTimeoutError:
        print("⏰ No speech detected - try again")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def main():
    print("=" * 50)
    print("JARVIS - Fixed for Your Audio Setup")
    print("=" * 50)
    
    # Quick greeting
    hour = datetime.datetime.now().hour
    if 0 <= hour <= 12:
        greeting = "Good morning"
    elif 12 < hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    speak(f"{greeting}! JARVIS is ready.")
    
    print("\nCommands:")
    print("- 'hello' - Greet")
    print("- 'time' - Current time") 
    print("- 'test' - Test recognition")
    print("- 'quit' - Exit")
    print("\nTips:")
    print("- Speak LOUD and CLEAR")
    print("- Wait for 'Speak clearly now...' prompt")
    print("- Use wired headset if possible")
    
    while True:
        try:
            command = better_listen()
            
            if not command:
                continue
                
            if 'hello' in command or 'hi' in command:
                responses = ["Hello sir!", "Yes, I'm here", "How can I help?"]
                speak(random.choice(responses))
                
            elif 'time' in command:
                now = datetime.datetime.now()
                time_str = now.strftime("%I:%M %p")
                speak(f"The time is {time_str}")
                
            elif 'test' in command:
                speak("Speech recognition is working perfectly!")
                
            elif 'quit' in command or 'exit' in command or 'bye' in command:
                speak("Goodbye!")
                break
                
            else:
                speak("I heard you, but didn't understand the command. Try hello, time, test, or quit.")
                
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    main()