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
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt, QThread
from PyQt5.QtGui import QMovie
from PyQt5.QtWidgets import *
from Jarvis.features.gui import Ui_MainWindow
from Jarvis.config import config

obj = JarvisAssistant()

GREETINGS = ["hello jarvis", "jarvis", "wake up jarvis", "hey jarvis", "ok jarvis"]
GREETINGS_RES = ["Yes sir", "I'm ready", "How can I help you?", "I'm listening sir"]

def speak(text):
    print(f"JARVIS: {text}")
    obj.tts(text)

class CommandProcessor:
    @staticmethod
    def process(command, ui_output=None):
        """Process commands and optionally update UI"""
        if not command:
            return
            
        command = command.lower()
        print(f"Processing: {command}")
        
        if ui_output:
            ui_output.append(f"JARVIS: Processing '{command}'")
        
        if re.search('date', command):
            date = obj.tell_me_date()
            speak(date)
            if ui_output:
                ui_output.append(f"JARVIS: {date}")
                
        elif "time" in command:
            time_c = obj.tell_time()
            speak(f"The time is {time_c}")
            if ui_output:
                ui_output.append(f"JARVIS: The time is {time_c}")
                
        elif command in GREETINGS:
            response = random.choice(GREETINGS_RES)
            speak(response)
            if ui_output:
                ui_output.append(f"JARVIS: {response}")
                
        elif re.search('open', command):
            domain = command.split(' ')[-1]
            obj.website_opener(domain)
            speak(f'Opening {domain}')
            if ui_output:
                ui_output.append(f"JARVIS: Opening {domain}")
                
        elif re.search('weather', command):
            city = command.split(' ')[-1]
            weather_res = obj.weather(city=city)
            if weather_res:
                speak(weather_res)
                if ui_output:
                    ui_output.append(f"JARVIS: {weather_res}")
            else:
                speak(f"Sorry, couldn't get weather for {city}")
                
        elif 'youtube' in command:
            video = command.replace('youtube', '').strip()
            if video:
                speak(f"Playing {video} on YouTube")
                pywhatkit.playonyt(video)
                if ui_output:
                    ui_output.append(f"JARVIS: Playing {video} on YouTube")
            else:
                speak("What should I search on YouTube?")
                
        elif "joke" in command:
            joke = pyjokes.get_joke()
            speak(joke)
            if ui_output:
                ui_output.append(f"JARVIS: {joke}")
                
        elif "system" in command:
            sys_info = obj.system_info()
            speak(sys_info)
            if ui_output:
                ui_output.append(f"JARVIS: {sys_info}")
                
        elif "ip address" in command:
            try:
                ip = requests.get('https://api.ipify.org', timeout=5).text
                speak(f"Your IP address is {ip}")
                if ui_output:
                    ui_output.append(f"JARVIS: Your IP is {ip}")
            except:
                speak("Sorry, couldn't get IP address")
                
        elif "screenshot" in command:
            speak("Taking screenshot")
            img = pyautogui.screenshot()
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            img.save(filename)
            speak(f"Screenshot saved as {filename}")
            if ui_output:
                ui_output.append(f"JARVIS: Screenshot saved as {filename}")
                
        elif "goodbye" in command or "exit" in command or "quit" in command:
            speak("Goodbye!")
            if ui_output:
                ui_output.append("JARVIS: Goodbye!")
            sys.exit()
            
        else:
            speak("I didn't understand that command.")
            if ui_output:
                ui_output.append("JARVIS: Command not recognized. Try: time, date, weather, joke, open google, youtube, screenshot")

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
                    CommandProcessor.process(command)
            except Exception as e:
                print(f"Voice error: {e}")
                time.sleep(1)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Connect buttons
        self.ui.pushButton.clicked.connect(self.toggleVoiceMode)
        self.ui.pushButton_2.clicked.connect(self.close)
        self.ui.sendButton.clicked.connect(self.sendTextCommand)
        self.ui.lineEdit.returnPressed.connect(self.sendTextCommand)
        
        # Initialize
        self.voice_thread = VoiceThread()
        self.voice_mode = False
        
        # Start timer for time display
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        
        # Initial message
        self.ui.textBrowser_3.append("JARVIS Ready! Type commands below or use Voice Mode.")
        self.ui.textBrowser_3.append("Commands: time, date, weather [city], joke, open google, youtube [search], screenshot")
        
    def toggleVoiceMode(self):
        """Toggle voice mode on/off"""
        if not self.voice_mode:
            self.voice_mode = True
            self.ui.pushButton.setText("Stop Voice")
            self.ui.textBrowser_3.append("Voice mode activated. Listening...")
            self.voice_thread.start()
        else:
            self.voice_mode = False
            self.voice_thread.running = False
            self.ui.pushButton.setText("Voice Mode")
            self.ui.textBrowser_3.append("Voice mode deactivated.")
            
    def sendTextCommand(self):
        """Process text command"""
        command = self.ui.lineEdit.text().strip()
        if command:
            self.ui.textBrowser_3.append(f"You: {command}")
            self.ui.lineEdit.clear()
            CommandProcessor.process(command, self.ui.textBrowser_3)
            
    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        self.ui.textBrowser.setText(current_date.toString(Qt.ISODate))
        self.ui.textBrowser_2.setText(current_time.toString('hh:mm:ss'))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    jarvis = Main()
    jarvis.show()
    sys.exit(app.exec_())