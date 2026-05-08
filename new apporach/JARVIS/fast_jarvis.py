import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

from Jarvis import JarvisAssistant
import re
import random
import datetime
import requests
import pyjokes
import time
import pyautogui
import pywhatkit
from Jarvis.config import config

obj = JarvisAssistant()

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "you there jarvis", "time to work jarvis", "hey jarvis",
             "ok jarvis", "are you there"]
GREETINGS_RES = ["always there for you sir", "i am ready sir",
                 "your wish my command", "how can i help you sir?", "i am online and ready sir"]

def speak(text):
    obj.tts(text)

def fast_startup():
    """Fast startup with minimal TTS"""
    print("JARVIS - Fast Mode Starting...")
    print("Systems initialized")
    print("All modules loaded")
    
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        greeting = "Good Morning"
    elif hour > 12 and hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    c_time = obj.tell_time()
    print(f"{greeting}! Current time: {c_time}")
    print("JARVIS is online and ready!")
    
    # Single TTS call instead of multiple
    speak(f"{greeting}. JARVIS online and ready sir.")

def main_loop():
    """Main command processing loop"""
    print("\nListening for commands... (Say 'hello jarvis' to activate)")
    
    while True:
        try:
            # Get voice input
            command = obj.mic_input()
            if not command:
                continue
                
            print(f"Command: {command}")

            if re.search('date', command):
                date = obj.tell_me_date()
                print(f"Date: {date}")
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                print(f"Time: {time_c}")
                speak(f"Sir the time is {time_c}")

            elif command in GREETINGS:
                response = random.choice(GREETINGS_RES)
                print(f"Response: {response}")
                speak(response)

            elif re.search('open', command):
                domain = command.split(' ')[-1]
                print(f"Opening {domain}")
                obj.website_opener(domain)
                speak(f'Opening {domain}')

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                if weather_res:
                    print(f"Weather: {weather_res}")
                    speak(weather_res)

            elif 'youtube' in command:
                video = command.split(' ')[1]
                print(f"Playing {video} on YouTube")
                speak(f"Playing {video} on youtube")
                pywhatkit.playonyt(video)

            elif "joke" in command:
                joke = pyjokes.get_joke()
                print(f"Joke: {joke}")
                speak(joke)

            elif "system" in command:
                sys_info = obj.system_info()
                print(f"System: {sys_info}")
                speak(sys_info)

            elif "ip address" in command:
                ip = requests.get('https://api.ipify.org').text
                print(f"Your IP: {ip}")
                speak(f"Your ip address is {ip}")

            elif "take screenshot" in command:
                speak("What name for the screenshot?")
                name = obj.mic_input()
                if name:
                    img = pyautogui.screenshot()
                    filename = f"{name}.png"
                    img.save(filename)
                    print(f"Screenshot saved as {filename}")
                    speak("Screenshot captured successfully")

            elif "goodbye" in command or "offline" in command or "bye" in command:
                print("JARVIS going offline...")
                speak("Goodbye sir!")
                break

            else:
                print("Command not recognized. Try: time, date, weather, joke, open google, youtube, screenshot, goodbye")

        except KeyboardInterrupt:
            print("\nExiting JARVIS...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        fast_startup()
        main_loop()
    except Exception as e:
        print(f"Startup Error: {e}")
        print("Please check your microphone and audio settings.")