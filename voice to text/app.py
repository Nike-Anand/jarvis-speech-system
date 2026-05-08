from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
import google.generativeai as genai
import os
from werkzeug.utils import secure_filename
import subprocess
import sys

# Configure Gemini API
genai.configure(api_key="AIzaSyBzGvQD1l_t7QyZOwvXKcbaAd_Pgud5bRU")
model = genai.GenerativeModel('gemini-1.5-pro-latest')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

class TamilVoiceToText:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        
    def convert_mp3_to_wav_simple(self, mp3_path):
        """Simple MP3 to WAV conversion using Windows built-in tools"""
        try:
            wav_path = mp3_path.replace('.mp3', '_converted.wav')
            # Try using Windows Media Format SDK (if available)
            result = subprocess.run([
                'powershell', '-Command', 
                f'Add-Type -AssemblyName presentationCore; '
                f'$mp = New-Object System.Windows.Media.MediaPlayer; '
                f'$mp.Open("{mp3_path}"); '
                f'Start-Sleep 2; '
                f'$mp.Close()'
            ], capture_output=True, text=True)
            return wav_path if os.path.exists(wav_path) else None
        except:
            return None
    
    def convert_audio_to_text(self, audio_file_path):
        try:
            print(f"Processing file: {audio_file_path}")
            print(f"File exists: {os.path.exists(audio_file_path)}")
            print(f"File size: {os.path.getsize(audio_file_path) if os.path.exists(audio_file_path) else 'N/A'}")
            
            original_path = audio_file_path
            
            # If it's MP3, show message
            if audio_file_path.lower().endswith('.mp3'):
                return "Please convert MP3 to WAV format first using an online converter."
            
            # Check if file has content
            if not os.path.exists(audio_file_path) or os.path.getsize(audio_file_path) < 1000:
                return "Audio file is too small or empty. Please record for at least 2 seconds."
            
            # Use speech recognition
            with sr.AudioFile(audio_file_path) as source:
                print(f"Audio file duration: {source.DURATION}")
                audio_data = self.recognizer.record(source)
            
            print("Sending to Google Speech Recognition...")
            text = self.recognizer.recognize_google(audio_data, language='ta-IN')
            print(f"Recognition result: {text}")
            
            return text
        except sr.UnknownValueError:
            return "Could not understand the audio. Please speak clearly in Tamil."
        except sr.RequestError as e:
            return f"Speech recognition service error: {str(e)}"
        except Exception as e:
            print(f"Full error: {str(e)}")
            return f"Error: {str(e)}"
    
    def enhance_with_gemini(self, text):
        try:
            prompt = f"Correct and improve this Tamil text if needed: {text}"
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return text

tamil_stt = TamilVoiceToText()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simple')
def simple():
    return open('simple_recorder.html').read()

@app.route('/pqc')
def pqc_page():
    return '''<h1>Post-Quantum Cryptography Simulator</h1>
    <p>Run the PQC simulator: <a href="http://127.0.0.1:5001/pqc" target="_blank">Open PQC Simulator</a></p>
    <p>Or run: <code>python pqc_simulator.py</code></p>'''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'audio' in request.files:
        # Handle recorded audio
        file = request.files['audio']
        filename = 'recorded_audio.wav'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    elif 'file' in request.files:
        # Handle uploaded file
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'})
        
        if not file.filename.lower().endswith(('.wav', '.mp3')):
            return jsonify({'error': 'Please upload WAV or MP3 file'})
            
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
    else:
        return jsonify({'error': 'No audio data received'})
    
    # Convert to text
    tamil_text = tamil_stt.convert_audio_to_text(filepath)
    enhanced_text = tamil_stt.enhance_with_gemini(tamil_text)
    
    # Clean up uploaded file
    os.remove(filepath)
    
    return jsonify({
        'original': tamil_text,
        'enhanced': enhanced_text
    })

if __name__ == '__main__':
    app.run(debug=True)