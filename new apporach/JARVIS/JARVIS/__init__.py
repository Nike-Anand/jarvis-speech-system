import speech_recognition as sr
import sys
import os

from Jarvis.features import date_time
from Jarvis.features import launch_app
from Jarvis.features import website_open
from Jarvis.features import weather
from Jarvis.features import wikipedia
from Jarvis.features import news
from Jarvis.features import send_email
from Jarvis.features import google_search
from Jarvis.features import google_calendar
from Jarvis.features import note
from Jarvis.features import system_stats
from Jarvis.features import loc

# Add Soprano TTS path
SOPRANO_PATH = r"c:\D\Projects\jarvis\TTS\soprano"
if os.path.exists(SOPRANO_PATH):
    sys.path.insert(0, SOPRANO_PATH)

print("TTS system ready - using Soprano TTS")

class JarvisAssistant:
    def __init__(self):
        self._soprano_model = None  # Lazy loading
        self._use_soprano = True
        self._audio_counter = 0  # For unique filenames

    def mic_input(self):
        """
        Improved microphone input with better recognition
        """
        try:
            r = sr.Recognizer()
            
            # Settings optimized for Bluetooth/multiple audio devices
            r.pause_threshold = 1.2  # Longer pause for Bluetooth delay
            r.phrase_threshold = 0.5  # More sensitive phrase detection
            r.non_speaking_duration = 0.8  # Account for Bluetooth latency
            
            with sr.Microphone() as source:
                print("Calibrating microphone... (stay quiet for 3 seconds)")
                r.adjust_for_ambient_noise(source, duration=3)
                print("Speak CLEARLY and LOUDLY now!")
                
                # Higher energy threshold for noisy Bluetooth devices
                r.energy_threshold = max(r.energy_threshold, 4000)
                print(f"Energy threshold: {r.energy_threshold}")
                
                # Longer timeout for Bluetooth devices
                audio = r.listen(source, timeout=15, phrase_time_limit=8)
                
            print("Processing speech...")
            
            # Try multiple recognition methods
            try:
                # Primary: Google (US English)
                command = r.recognize_google(audio, language='en-US').lower()
                print(f'Recognized: {command}')
                return command
            except sr.UnknownValueError:
                try:
                    # Fallback: Google (Indian English)
                    command = r.recognize_google(audio, language='en-IN').lower()
                    print(f'Recognized (IN): {command}')
                    return command
                except sr.UnknownValueError:
                    print('Could not understand audio. Please speak clearly.')
                    return None
            except sr.RequestError as e:
                print(f'Recognition service error: {e}')
                return None
                
        except sr.WaitTimeoutError:
            print('Listening timeout. No speech detected.')
            return None
        except Exception as e:
            print(f'Microphone error: {e}')
            return None

    def _init_soprano(self):
        """Initialize Soprano TTS model (lazy loading)"""
        if self._soprano_model is None:
            try:
                from soprano.tts import SopranoTTS
                print("Loading Soprano TTS model...")
                self._soprano_model = SopranoTTS(
                    backend='auto',
                    device='cpu',
                    cache_size_mb=500,  # Moderate cache for speed
                    decoder_batch_size=2  # Balance speed and memory
                )
                print("Soprano TTS model loaded successfully")
            except Exception as e:
                print(f"Failed to load Soprano TTS: {e}")
                print("Falling back to PowerShell TTS")
                self._use_soprano = False
        return self._soprano_model

    def tts(self, text):
        """
        Convert text to speech using Soprano TTS (with PowerShell fallback)
        """
        try:
            print(f"Speaking: {text}")
            
            # Try Soprano TTS first
            if self._use_soprano:
                try:
                    model = self._init_soprano()
                    if model is not None:
                        # Use streaming for low latency
                        from soprano.utils.streaming import play_stream
                        
                        # Generate and play audio stream
                        stream = model.infer_stream(
                            text,
                            chunk_size=1,  # Low latency
                            temperature=0.3,  # More consistent
                            top_p=0.95,
                            repetition_penalty=1.2
                        )
                        
                        # Play the stream
                        play_stream(stream)
                        print("Speech completed successfully (Soprano TTS)")
                        return True
                        
                except ImportError:
                    print("Soprano TTS not available, falling back to PowerShell")
                    self._use_soprano = False
                except Exception as e:
                    print(f"Soprano TTS error: {e}")
                    print("Falling back to PowerShell TTS")
                    self._use_soprano = False
            
            # Fallback to PowerShell TTS
            import subprocess
            
            # Escape quotes in text
            clean_text = text.replace('"', "'")
            
            # PowerShell command for TTS
            cmd = [
                'powershell', '-Command',
                f'Add-Type -AssemblyName System.Speech; '
                f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                f'$synth.Rate = 0; '
                f'$synth.Volume = 100; '
                f'$synth.Speak("{clean_text}")'
            ]
            
            # Run PowerShell command
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print("Speech completed successfully (PowerShell TTS)")
                return True
            else:
                print(f"PowerShell TTS error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            print("TTS timeout")
            return False
        except Exception as e:
            print(f"TTS Error: {e}")
            return False


    def tell_me_date(self):

        return date_time.date()

    def tell_time(self):

        return date_time.time()

    def launch_any_app(self, path_of_app):
        """
        Launch any windows application 
        :param path_of_app: path of exe 
        :return: True is success and open the application, False if fail
        """
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        """
        This will open website according to domain
        :param domain: any domain, example "youtube.com"
        :return: True if success, False if fail
        """
        return website_open.website_opener(domain)


    def weather(self, city):
        """
        Return weather
        :param city: Any city of this world
        :return: weather info as string if True, or False
        """
        try:
            res = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def tell_me(self, topic):
        """
        Tells about anything from wikipedia
        :param topic: any string is valid options
        :return: First 500 character from wikipedia if True, False if fail
        """
        return wikipedia.tell_me_about(topic)

    def news(self):
        """
        Fetch top news of the day from google news
        :return: news list of string if True, False if fail
        """
        return news.get_news()
    
    def send_mail(self, sender_email, sender_password, receiver_email, msg):

        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, text):
        service = google_calendar.authenticate_google()
        date = google_calendar.get_date(text) 
        
        if date:
            return google_calendar.get_events(date, service)
        else:
            pass
    
    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)
    
    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country