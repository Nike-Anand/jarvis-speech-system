import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

import speech_recognition as sr

def test_microphone():
    """Test microphone and speech recognition"""
    print("=== Microphone Test ===")
    
    # List available microphones
    print("Available microphones:")
    for index, name in enumerate(sr.Microphone.list_microphone_names()):
        print(f"  {index}: {name}")
    
    # Test recognition
    r = sr.Recognizer()
    
    # Optimized settings
    r.pause_threshold = 0.8
    r.phrase_threshold = 0.3
    r.non_speaking_duration = 0.5
    
    try:
        with sr.Microphone() as source:
            print("\nAdjusting for ambient noise... (be quiet for 2 seconds)")
            r.adjust_for_ambient_noise(source, duration=2)
            print(f"Energy threshold set to: {r.energy_threshold}")
            
            print("\nSay something (you have 10 seconds):")
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            
        print("Processing...")
        
        # Try recognition
        try:
            text = r.recognize_google(audio, language='en-US')
            print(f"✅ Recognized: '{text}'")
        except sr.UnknownValueError:
            print("❌ Could not understand audio")
        except sr.RequestError as e:
            print(f"❌ Recognition error: {e}")
            
    except sr.WaitTimeoutError:
        print("❌ No speech detected within timeout")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_continuous_listening():
    """Test continuous listening like JARVIS"""
    print("\n=== Continuous Listening Test ===")
    print("Say 'test' to test recognition, 'quit' to exit")
    
    r = sr.Recognizer()
    r.pause_threshold = 0.8
    r.energy_threshold = 300
    
    while True:
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=5, phrase_time_limit=3)
                
            text = r.recognize_google(audio, language='en-US').lower()
            print(f"You said: '{text}'")
            
            if 'quit' in text or 'exit' in text:
                print("Exiting...")
                break
            elif 'test' in text:
                print("✅ Recognition working!")
                
        except sr.WaitTimeoutError:
            print(".", end="", flush=True)  # Show it's still listening
        except sr.UnknownValueError:
            print("?", end="", flush=True)  # Couldn't understand
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    test_microphone()
    
    choice = input("\nTest continuous listening? (y/n): ")
    if choice.lower() == 'y':
        test_continuous_listening()