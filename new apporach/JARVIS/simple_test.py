import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

from Jarvis import JarvisAssistant
import datetime

def simple_test():
    """Simple test without GUI"""
    print("=" * 60)
    print("JARVIS - Simple Test Mode")
    print("=" * 60)
    
    # Initialize JARVIS
    jarvis = JarvisAssistant()
    
    # Greeting
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour <= 12:
        greeting = "Good Morning"
    elif 12 < hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"
    
    print(f"\n{greeting}! JARVIS is online and ready.")
    print("\nTesting Soprano TTS integration...")
    
    # Test TTS
    jarvis.tts(f"{greeting}. JARVIS is online and ready sir.")
    
    print("\n✅ TTS test complete!")
    print("\nAvailable commands:")
    print("- time")
    print("- date")
    print("- joke")
    print("- open google")
    print("- system (system stats)")
    print("- exit")
    
    # Command loop
    while True:
        try:
            command = input("\nEnter command: ").lower().strip()
            
            if not command:
                continue
                
            if 'exit' in command or 'quit' in command:
                jarvis.tts("Goodbye sir!")
                break
                
            elif 'time' in command:
                time_now = jarvis.tell_time()
                print(f"Time: {time_now}")
                jarvis.tts(f"The time is {time_now}")
                
            elif 'date' in command:
                date_now = jarvis.tell_me_date()
                print(f"Date: {date_now}")
                jarvis.tts(f"Today is {date_now}")
                
            elif 'joke' in command:
                import pyjokes
                joke = pyjokes.get_joke()
                print(f"Joke: {joke}")
                jarvis.tts(joke)
                
            elif 'open google' in command:
                jarvis.website_opener('google.com')
                jarvis.tts("Opening Google")
                
            elif 'system' in command:
                sys_info = jarvis.system_info()
                print(f"System: {sys_info}")
                jarvis.tts(sys_info)
                
            else:
                print("Command not recognized. Try: time, date, joke, open google, system, exit")
                
        except KeyboardInterrupt:
            print("\n\nExiting...")
            jarvis.tts("Goodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    try:
        simple_test()
    except Exception as e:
        print(f"Startup error: {e}")
        import traceback
        traceback.print_exc()
