import os
import threading

class SimpleTTS:
    def __init__(self):
        self.is_speaking = False
        
    def speak(self, text):
        if self.is_speaking:
            return
            
        def speak_thread():
            self.is_speaking = True
            try:
                # Clean text for Windows TTS
                clean_text = text.replace('"', '').replace("'", "").replace('`', '')
                
                # Use Windows built-in TTS via PowerShell
                ps_command = f'powershell -Command "Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Rate = 0; $speak.Volume = 100; $speak.Speak(\'{clean_text}\')"'
                
                os.system(ps_command)
                
            except Exception as e:
                print(f"TTS Error: {e}")
            finally:
                self.is_speaking = False
                
        threading.Thread(target=speak_thread, daemon=False).start()