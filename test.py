import sounddevice as sd
import numpy as np
import queue
from faster_whisper import WhisperModel
import ollama
import os
import asyncio
import edge_tts
import pygame

# ----------------------------
# CONFIG
# ----------------------------
STT_MODEL = "small.en"
TTS_MODEL = "en_US-lessac-medium.onnx"
SAMPLE_RATE = 16000
DURATION = 5
WAKE_WORD = "alex"

# ----------------------------
# RECORD AUDIO FROM MIC
# ----------------------------
def record_audio(filename="input.wav", duration=DURATION, samplerate=SAMPLE_RATE):
    print("🎙️ Listening...")
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="float32")
    sd.wait()
    # Normalize & save
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = np.int16(audio / max_val * 32767)
    else:
        audio = np.int16(audio * 32767)
    import wave
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio.tobytes())

# ----------------------------
# SPEECH TO TEXT (STT)
# ----------------------------
# Initialize model once to avoid reloading
print("🔄 Loading Whisper model...")
whisper_model = WhisperModel(STT_MODEL, device="cpu", compute_type="int8")
print("✅ Model loaded")

def transcribe_audio(filename="input.wav"):
    try:
        segments, _ = whisper_model.transcribe(filename)
        text = " ".join([seg.text for seg in segments]).strip()
        return text.lower()
    except Exception as e:
        print(f"❌ Transcription failed: {e}")
        return ""

# ----------------------------
# OLLAMA CHAT
# ----------------------------
def chat_with_ollama(prompt):
    print("🤖 Processing...")
    system_msg = "You are ALEX, a helpful AI assistant. Be friendly, intelligent, and concise in your responses."
    response = ollama.chat(model="llama3", messages=[
        {"role": "system", "content": system_msg},
        {"role": "user", "content": prompt}
    ])
    reply = response["message"]["content"]
    print(f"🤖 ALEX: {reply}")
    return reply

# ----------------------------
# TEXT TO SPEECH (TTS) with Edge TTS
# ----------------------------
pygame.mixer.init()

async def generate_speech(text):
    communicate = edge_tts.Communicate(text, "en-US-AriaNeural")
    await communicate.save("speech.mp3")

def speak_text(text):
    try:
        asyncio.run(generate_speech(text))
        pygame.mixer.music.load("speech.mp3")
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        print(f"❌ Speech failed: {e}")

# ----------------------------
# MAIN LOOP
# ----------------------------
if __name__ == "__main__":
    print("🤖 ALEX online. Say 'Alex' to activate.")
    
    while True:
        record_audio()
        user_text = transcribe_audio()
        
        if not user_text:
            continue
            
        print(f"👂 Heard: '{user_text}'")
            
        if any(word in user_text for word in ["exit", "quit", "stop", "shutdown"]):
            print("🤖 ALEX: Shutting down. Goodbye.")
            speak_text("Shutting down. Goodbye.")
            break
            
        # Check for wake word or question words
        if (WAKE_WORD in user_text or "alex" in user_text or 
            any(q in user_text for q in ["what", "how", "why", "when", "where", "did", "do", "can", "?"])):
            
            # Remove wake word if present
            command = user_text.replace(WAKE_WORD, "").replace("alex", "").strip()
            
            if command:
                print(f"👤 Command: {command}")
                reply = chat_with_ollama(command)
                speak_text(reply)
            else:
                print("🤖 ALEX: How can I help you?")
                speak_text("How can I help you?")
