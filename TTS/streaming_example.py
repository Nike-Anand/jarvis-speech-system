"""
Streaming Example for Soprano TTS
Demonstrates low-latency streaming audio playback
"""
from soprano.tts import SopranoTTS
from soprano.utils.streaming import play_stream

# Initialize model
print("Loading Soprano TTS...")
model = SopranoTTS(backend='auto', device='cpu', cache_size_mb=100, decoder_batch_size=1)

# Stream audio with low latency
text = "This is a streaming example. The audio will play as it's being generated, providing ultra-low latency speech synthesis."
print(f"Streaming: {text}")
print("Playing audio...")

stream = model.infer_stream(text, chunk_size=1)
play_stream(stream)

print("✓ Streaming complete!")
