import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

from Jarvis import JarvisAssistant
import speech_recognition as sr
import re
import random
import datetime
import requests
import pyjokes
import pyautogui
import pywhatkit

# Initialize JARVIS
obj = JarvisAssistant()

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "hey jarvis", "ok jarvis"]
GREETINGS_RES = ["Yes sir", "I'm ready", "How can I help you?", "I'm listening sir"]

def speak(text):
    print(f"JARVIS: {text}")
    obj.tts(text)

def improved_listen():
    """Improved listening with better error handling"""
    r = sr.Recognizer()
    
    # Optimized settings
    r.pause_threshold = 0.8
    r.phrase_threshold = 0.3
    r.energy_threshold = 300
    
    try:
        with sr.Microphone() as source:
            print("Listening... (speak clearly)")
            
            # Quick ambient noise adjustment
            r.adjust_for_ambient_noise(source, duration=0.5)
            
            # Listen with reasonable timeout
            audio = r.listen(source, timeout=8, phrase_time_limit=4)
            
        print("Processing...")
        
        # Try recognition with multiple languages
        for lang in ['en-US', 'en-GB', 'en-IN']:
            try:
                command = r.recognize_google(audio, language=lang).lower()
                print(f"You said: '{command}'")
                return command
            except sr.UnknownValueError:
                continue
        
        print("Sorry, I couldn't understand. Please try again.")
        return None
        
    except sr.WaitTimeoutError:
        print("No speech detected. Try again.")
        return None
    except Exception as e:
        print(f"Listening error: {e}")
        return None

def startup():
    print("=" * 50)
    print("JARVIS - Improved Speech Recognition")
    print("=" * 50)
    
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        greeting = "Good Morning"
    elif 12 < hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    speak(f"{greeting}. JARVIS is online and ready.")
    print("\nAvailable commands:")
    print("- 'hello jarvis' - Activate")
    print("- 'time' - Current time")
    print("- 'date' - Current date")
    print("- 'open google' - Open Google")
    print("- 'weather [city]' - Weather info")
    print("- 'joke' - Tell a joke")
    print("- 'youtube [search]' - Play on YouTube")
    print("- 'screenshot' - Take screenshot")
    print("- 'goodbye' - Exit")
    print("\nTip: Speak clearly and wait for 'Listening...' prompt")

def main():
    startup()
    
    while True:
        try:
            command = improved_listen()
            
            if not command:
                continue
                
            # Process commands
            if any(greeting in command for greeting in GREETINGS):
                response = random.choice(GREETINGS_RES)
                speak(response)
                
            elif 'time' in command:
                current_time = obj.tell_time()
                speak(f"The time is {current_time}")
                
            elif 'date' in command:
                current_date = obj.tell_me_date()
                speak(f"Today is {current_date}")
                
            elif 'open' in command and 'google' in command:
                speak("Opening Google")
                obj.website_opener('google.com')
                
            elif 'weather' in command:
                # Extract city name
                words = command.split()
                if len(words) > 1:
                    city = words[-1]  # Last word as city
                    weather_info = obj.weather(city)
                    if weather_info:
                        speak(weather_info)
                    else:
                        speak(f"Sorry, I couldn't get weather for {city}")
                else:
                    speak("Please specify a city for weather")
                    
            elif 'joke' in command:
                joke = pyjokes.get_joke()
                speak(joke)
                
            elif 'youtube' in command:
                # Extract search term
                words = command.replace('youtube', '').strip()
                if words:
                    speak(f"Playing {words} on YouTube")
                    pywhatkit.playonyt(words)
                else:
                    speak("What should I search on YouTube?")
                    
            elif 'screenshot' in command:
                speak("Taking screenshot")
                img = pyautogui.screenshot()
                filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                img.save(filename)
                speak(f"Screenshot saved as {filename}")
                
            elif 'system' in command or 'status' in command:
                sys_info = obj.system_info()
                speak(sys_info)
                
            elif 'ip' in command:
                try:
                    ip = requests.get('https://api.ipify.org', timeout=5).text
                    speak(f"Your IP address is {ip}")
                except:
                    speak("Sorry, couldn't get IP address")
                    
            elif 'goodbye' in command or 'exit' in command or 'quit' in command:
                speak("Goodbye! Have a great day!")
                break
                
            else:
                speak("I didn't understand that command. Try saying 'hello jarvis' first, then give a command.")
                
        except KeyboardInterrupt:
            print("\nExiting JARVIS...")
            speak("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry, I encountered an error.")

if __name__ == "__main__":
    main()