import speech_recognition as sr
import google.generativeai as genai
import os

# Configure Gemini API
genai.configure(api_key="AIzaSyBzGvQD1l_t7QyZOwvXKcbaAd_Pgud5bRU")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

class TamilVoiceToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def convert_wav_to_text(self, wav_file_path):
        """Convert WAV file to Tamil text"""
        try:
            print(f"கோப்பு செயலாக்கம்... (Processing file: {wav_file_path})")
            
            # Use speech recognition directly with WAV
            with sr.AudioFile(wav_file_path) as source:
                audio_data = self.recognizer.record(source)
            
            # Convert to Tamil text
            text = self.recognizer.recognize_google(audio_data, language='ta-IN')
            
            return text
            
        except FileNotFoundError:
            return "கோப்பு கிடைக்கவில்லை (File not found)"
        except sr.UnknownValueError:
            return "புரியவில்லை (Could not understand audio)"
        except sr.RequestError as e:
            return f"பிழை (Error): {e}"
        except Exception as e:
            return f"பொது பிழை (General error): {e}"
    
    def enhance_with_gemini(self, text):
        """Optional: Use Gemini to enhance or correct the Tamil text"""
        try:
            prompt = f"Correct and improve this Tamil text if needed: {text}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Gemini error: {e}")
            return text

def main():
    tamil_stt = TamilVoiceToText()
    
    print("தமிழ் WAV உரை மாற்றி (Tamil WAV to Text)")
    
    # Find WAV file in current directory
    wav_files = [f for f in os.listdir('.') if f.endswith('.wav')]
    
    if not wav_files:
        print("WAV கோப்பு கிடைக்கவில்லை (No WAV file found)")
        print("Please convert your MP3 to WAV format first")
        return
    
    wav_file = wav_files[0]  # Use first WAV file found
    print(f"Using file: {wav_file}")
    
    # Convert WAV to text
    tamil_text = tamil_stt.convert_wav_to_text(wav_file)
    
    if tamil_text and "பிழை" not in tamil_text and "கோப்பு" not in tamil_text and "புரியவில்லை" not in tamil_text:
        print(f"\nமூல உரை (Original): {tamil_text}")
        
        # Optional: Enhance with Gemini
        enhanced_text = tamil_stt.enhance_with_gemini(tamil_text)
        if enhanced_text != tamil_text:
            print(f"மேம்படுத்தப்பட்ட உரை (Enhanced): {enhanced_text}")
    else:
        print(f"முடிவு (Result): {tamil_text}")

if __name__ == "__main__":
    main()