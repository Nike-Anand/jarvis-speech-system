"""
Simple Soprano TTS Example
Quick start guide for generating speech
"""
from soprano.tts import SopranoTTS

# Initialize model
print("Loading Soprano TTS...")
model = SopranoTTS(backend='auto', device='cpu')

# Generate speech
text = "Hello! This is a simple example of Soprano text to speech."
print(f"Generating: {text}")
model.infer(text, "hello.wav")
print("✓ Audio saved to hello.wav")
