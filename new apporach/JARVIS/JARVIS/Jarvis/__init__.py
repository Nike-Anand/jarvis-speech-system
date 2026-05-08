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
# from Jarvis.features import google_calendar  # Temporarily disabled - requires Google API setup
from Jarvis.features import note
from Jarvis.features import system_stats
from Jarvis.features import loc

# Add Soprano TTS path
SOPRANO_PATH = r"c:\D\Projects\jarvis\TTS\soprano"
if os.path.exists(SOPRANO_PATH):
    sys.path.insert(0, SOPRANO_PATH)

class JarvisAssistant:
    def __init__(self):
        self._soprano_model = None  # Lazy loading
        self._use_soprano = True

    def mic_input(self):
        """
        Fetch input from mic
        return: user's voice input as text if true, false if fail
        """
        try:
            r = sr.Recognizer()
            # r.pause_threshold = 1
            # r.adjust_for_ambient_noise(source, duration=1)
            with sr.Microphone() as source:
                print("Listening....")
                r.energy_threshold = 4000
                audio = r.listen(source)
            try:
                print("Recognizing...")
                command = r.recognize_google(audio, language='en-in').lower()
                print(f'You said: {command}')
            except:
                print('Please try again')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return  False


    def _init_soprano(self):
        """Initialize Soprano TTS model (lazy loading)"""
        if self._soprano_model is None:
            try:
                from soprano.tts import SopranoTTS
                print("Loading Soprano TTS model...")
                self._soprano_model = SopranoTTS(
                    backend='auto',
                    device='cpu',
                    cache_size_mb=500,
                    decoder_batch_size=2
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
                        from soprano.utils.streaming import play_stream
                        
                        stream = model.infer_stream(
                            text,
                            chunk_size=1,
                            temperature=0.3,
                            top_p=0.95,
                            repetition_penalty=1.2
                        )
                        
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
            
            clean_text = text.replace('"', "'")
            
            cmd = [
                'powershell', '-Command',
                f'Add-Type -AssemblyName System.Speech; '
                f'$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer; '
                f'$synth.Rate = 0; '
                f'$synth.Volume = 100; '
                f'$synth.Speak("{clean_text}")'
            ]
            
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
        """Google Calendar feature temporarily disabled - requires Google API setup"""
        print("[Google Calendar] Feature disabled - requires Google API dependencies")
        print("[Google Calendar] To enable: pip install google-api-python-client google-auth-oauthlib")
        return None
        # service = google_calendar.authenticate_google()
        # date = google_calendar.get_date(text) 
        # 
        # if date:
        #     return google_calendar.get_events(date, service)
        # else:
        #     pass
    
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