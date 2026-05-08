import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

from Jarvis import JarvisAssistant
import datetime

def simple_startup():
    print("=== JARVIS Simple Mode ===")
    print("Initializing...")
    
    obj = JarvisAssistant()
    
    # Quick greeting without excessive TTS
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        greeting = "Good Morning"
    elif hour > 12 and hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    print(f"Speaking: {greeting}. JARVIS is online and ready.")
    obj.tts(f"{greeting}. JARVIS is online and ready.")
    
    print("\nAvailable commands:")
    print("- 'time' - Get current time")
    print("- 'date' - Get current date") 
    print("- 'open google' - Open Google")
    print("- 'joke' - Tell a joke")
    print("- 'exit' - Quit JARVIS")
    print("\nListening for commands...")
    
    return obj

def main():
    try:
        jarvis = simple_startup()
        
        while True:
            try:
                command = input("\nEnter command (or 'voice' for voice input): ").lower()
                
                if command == 'voice':
                    print("Listening...")
                    command = jarvis.mic_input()
                    if not command:
                        continue
                
                if 'exit' in command or 'quit' in command:
                    jarvis.tts("Goodbye!")
                    break
                elif 'time' in command:
                    time_now = jarvis.tell_time()
                    print(f"Time: {time_now}")
                    jarvis.tts(f"The time is {time_now}")
                elif 'date' in command:
                    date_now = jarvis.tell_me_date()
                    print(f"Date: {date_now}")
                    jarvis.tts(f"Today is {date_now}")
                elif 'open google' in command:
                    jarvis.website_opener('google.com')
                    jarvis.tts("Opening Google")
                elif 'joke' in command:
                    import pyjokes
                    joke = pyjokes.get_joke()
                    print(f"Joke: {joke}")
                    jarvis.tts(joke)
                else:
                    print("Command not recognized. Try 'time', 'date', 'open google', 'joke', or 'exit'")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")
                
    except Exception as e:
        print(f"Startup error: {e}")

if __name__ == "__main__":
    main()