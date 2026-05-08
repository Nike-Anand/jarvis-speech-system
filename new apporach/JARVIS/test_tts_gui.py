import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

from Jarvis import JarvisAssistant
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class TTSTest(QWidget):
    def __init__(self):
        super().__init__()
        self.obj = JarvisAssistant()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('TTS Test')
        self.setGeometry(300, 300, 400, 200)
        
        layout = QVBoxLayout()
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text to speak...")
        layout.addWidget(self.text_input)
        
        speak_btn = QPushButton("Test TTS")
        speak_btn.clicked.connect(self.test_tts)
        layout.addWidget(speak_btn)
        
        self.output = QTextEdit()
        layout.addWidget(self.output)
        
        self.setLayout(layout)
        
    def test_tts(self):
        text = self.text_input.text().strip()
        if text:
            self.output.append(f"Testing TTS with: {text}")
            try:
                print(f"Calling TTS with: {text}")
                result = self.obj.tts(text)
                print(f"TTS result: {result}")
                self.output.append(f"TTS Result: {result}")
            except Exception as e:
                print(f"TTS Error: {e}")
                self.output.append(f"TTS Error: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TTSTest()
    window.show()
    sys.exit(app.exec_())