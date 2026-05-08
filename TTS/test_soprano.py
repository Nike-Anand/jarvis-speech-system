"""
Test script for Soprano TTS
Generates sample audio using different methods
"""
from soprano.tts import SopranoTTS
import os

def main():
    print("Initializing Soprano TTS...")
    # Initialize the model with CPU backend
    model = SopranoTTS(
        backend='auto', 
        device='cpu',  # Using CPU for compatibility
        cache_size_mb=100, 
        decoder_batch_size=1
    )
    
    print("Model loaded successfully!")
    
    # Test 1: Basic inference
    print("\n=== Test 1: Basic Inference ===")
    text1 = "Soprano is an extremely lightweight text to speech model."
    output_file1 = "output_basic.wav"
    print(f"Generating: '{text1}'")
    model.infer(text1, output_file1)
    print(f"✓ Audio saved to: {output_file1}")
    
    # Test 2: Custom sampling parameters
    print("\n=== Test 2: Custom Sampling Parameters ===")
    text2 = "This is a test with custom temperature and top p settings for more varied speech generation."
    output_file2 = "output_custom.wav"
    print(f"Generating: '{text2}'")
    model.infer(
        text2,
        output_file2,
        temperature=0.3,
        top_p=0.95,
        repetition_penalty=1.2,
    )
    print(f"✓ Audio saved to: {output_file2}")
    
    # Test 3: Longer text
    print("\n=== Test 3: Longer Text ===")
    text3 = """Soprano is an ultra-lightweight, on-device text-to-speech model designed for 
    expressive, high-fidelity speech synthesis at unprecedented speed. It can generate up to 
    twenty times real-time on CPU and two thousand times real-time on GPU."""
    output_file3 = "output_long.wav"
    print(f"Generating longer text...")
    model.infer(text3, output_file3)
    print(f"✓ Audio saved to: {output_file3}")
    
    print("\n" + "="*50)
    print("All tests completed successfully!")
    print("Generated files:")
    for f in [output_file1, output_file2, output_file3]:
        if os.path.exists(f):
            size = os.path.getsize(f) / 1024  # KB
            print(f"  - {f} ({size:.2f} KB)")

if __name__ == "__main__":
    main()
