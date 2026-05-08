import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

from Jarvis import JarvisAssistant
import re
import random
import datetime
import requests
import pyjokes
import pyautogui
import pywhatkit
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

obj = JarvisAssistant()

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "hey jarvis", "ok jarvis"]
GREETINGS_RES = ["Yes sir", "I'm ready", "How can I help you?", "I'm listening sir"]

def speak(text):
    print(f"JARVIS: {text}")
    try:
        obj.tts(text)
        print("TTS completed successfully")
    except Exception as e:
        print(f"TTS Error: {e}")

def jarvis_response(text, output_widget=None):
    """Always speak and display JARVIS responses"""
    if output_widget:
        output_widget.append(f"JARVIS: {text}")
    print(f"About to speak: {text}")
    speak(text)

def process_command(command, output_widget=None):
    """Process commands - all responses will be spoken"""
    if not command:
        return
        
    command = command.lower()
    
    if output_widget:
        output_widget.append(f"You: {command}")
    
    if "time" in command:
        time_c = obj.tell_time()
        jarvis_response(f"The time is {time_c}", output_widget)
            
    elif "date" in command:
        date = obj.tell_me_date()
        jarvis_response(date, output_widget)
            
    elif any(greet in command for greet in GREETINGS):
        response = random.choice(GREETINGS_RES)
        jarvis_response(response, output_widget)
            
    elif "open google" in command:
        obj.website_opener('google.com')
        jarvis_response("Opening Google for you sir", output_widget)
        
    elif "weather" in command:
        city = command.split()[-1] if len(command.split()) > 1 else "your location"
        weather_res = obj.weather(city=city)
        if weather_res:
            jarvis_response(weather_res, output_widget)
        else:
            jarvis_response(f"Sorry, I couldn't get weather information for {city}", output_widget)
            
    elif "joke" in command:
        joke = pyjokes.get_joke()
        jarvis_response(joke, output_widget)
            
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        filename = f"screenshot_{datetime.datetime.now().strftime('%H%M%S')}.png"
        img.save(filename)
        jarvis_response(f"Screenshot saved as {filename}", output_widget)
            
    elif "youtube" in command:
        search = command.replace("youtube", "").strip()
        if search:
            jarvis_response(f"Playing {search} on YouTube", output_widget)
            pywhatkit.playonyt(search)
        else:
            jarvis_response("What should I search for on YouTube?", output_widget)
    
    elif "system" in command or "status" in command:
        sys_info = obj.system_info()
        jarvis_response(sys_info, output_widget)
        
    elif "ip" in command:
        try:
            ip = requests.get('https://api.ipify.org', timeout=5).text
            jarvis_response(f"Your IP address is {ip}", output_widget)
        except:
            jarvis_response("Sorry, I couldn't retrieve your IP address", output_widget)
            
    elif "exit" in command or "quit" in command or "goodbye" in command:
        jarvis_response("Goodbye sir! Have a great day!", output_widget)
        QApplication.quit()
        
    else:
        jarvis_response("I didn't understand that command. Try saying: time, date, hello jarvis, joke, open google, weather, youtube, screenshot, or goodbye", output_widget)

class VoiceThread(QThread):
    def __init__(self):
        super().__init__()
        self.running = False
        
    def run(self):
        self.running = True
        while self.running:
            try:
                command = obj.mic_input()
                if command and self.running:
                    process_command(command)
            except:
                pass

class JarvisGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.voice_thread = VoiceThread()
        self.voice_active = False
        
    def initUI(self):
        self.setWindowTitle('JARVIS - Voice Assistant')
        self.setGeometry(100, 100, 800, 600)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout()
        
        # Title
        title = QLabel('JARVIS - Voice Assistant')
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; color: #0099ff; margin: 20px;")
        layout.addWidget(title)
        
        # Time display
        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size: 18px; color: #333; margin: 10px;")
        layout.addWidget(self.time_label)
        
        # Output area
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background-color: #f0f0f0; border: 2px solid #0099ff; border-radius: 10px; padding: 10px; font-size: 14px;")
        layout.addWidget(self.output)
        
        # Input area
        input_layout = QHBoxLayout()
        
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your command here...")
        self.input_field.setStyleSheet("padding: 10px; font-size: 14px; border: 2px solid #0099ff; border-radius: 5px;")
        self.input_field.returnPressed.connect(self.send_command)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("background-color: #0099ff; color: white; padding: 10px 20px; font-size: 14px; border: none; border-radius: 5px;")
        self.send_btn.clicked.connect(self.send_command)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        
        # Control buttons
        button_layout = QHBoxLayout()
        
        self.voice_btn = QPushButton("Start Voice Mode")
        self.voice_btn.setStyleSheet("background-color: #28a745; color: white; padding: 15px; font-size: 16px; border: none; border-radius: 5px;")
        self.voice_btn.clicked.connect(self.toggle_voice)
        button_layout.addWidget(self.voice_btn)
        
        exit_btn = QPushButton("Exit")
        exit_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 15px; font-size: 16px; border: none; border-radius: 5px;")
        exit_btn.clicked.connect(self.close)
        button_layout.addWidget(exit_btn)
        
        layout.addLayout(button_layout)
        
        central_widget.setLayout(layout)
        
        # Timer for time display
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        
        # Initial message without speech during startup
        self.output.append("JARVIS: JARVIS online and ready sir. You can type commands or use voice mode.")
        self.output.append("JARVIS: Available commands: time, date, hello jarvis, joke, open google, weather, youtube, screenshot, or goodbye")
        
        # Delayed welcome speech
        QTimer.singleShot(1000, self.welcome_speech)
        
    def update_time(self):
        current_time = QTime.currentTime().toString('hh:mm:ss')
        current_date = QDate.currentDate().toString('yyyy-MM-dd')
        self.time_label.setText(f"{current_date} | {current_time}")
        
    def send_command(self):
        command = self.input_field.text().strip()
        if command:
            self.input_field.clear()
            process_command(command, self.output)
            
    def welcome_speech(self):
        """Welcome speech after GUI is loaded"""
        speak("JARVIS online and ready sir. How may I help you?")
    
    def toggle_voice(self):
        if not self.voice_active:
            self.voice_active = True
            self.voice_btn.setText("Stop Voice Mode")
            self.voice_btn.setStyleSheet("background-color: #dc3545; color: white; padding: 15px; font-size: 16px; border: none; border-radius: 5px;")
            jarvis_response("Voice mode activated. I'm listening for your commands.", self.output)
            self.voice_thread.start()
        else:
            self.voice_active = False
            self.voice_thread.running = False
            self.voice_btn.setText("Start Voice Mode")
            self.voice_btn.setStyleSheet("background-color: #28a745; color: white; padding: 15px; font-size: 16px; border: none; border-radius: 5px;")
            jarvis_response("Voice mode deactivated. You can continue typing commands.", self.output)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = JarvisGUI()
    window.show()
    sys.exit(app.exec_())