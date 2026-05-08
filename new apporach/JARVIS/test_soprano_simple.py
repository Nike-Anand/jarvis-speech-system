"""
Simple test for Soprano TTS integration
Tests only the TTS functionality without loading all JARVIS features
"""

import sys
import os

# Add Soprano TTS path
SOPRANO_PATH = r"c:\D\Projects\jarvis\TTS\soprano"
if os.path.exists(SOPRANO_PATH):
    sys.path.insert(0, SOPRANO_PATH)
    print(f"✅ Soprano TTS path added: {SOPRANO_PATH}")
else:
    print(f"❌ Soprano TTS path not found: {SOPRANO_PATH}")
    sys.exit(1)

def test_soprano_direct():
    """Test Soprano TTS directly"""
    print("\n" + "=" * 60)
    print("Testing Soprano TTS Directly")
    print("=" * 60)
    
    try:
        from soprano.tts import SopranoTTS
        from soprano.utils.streaming import play_stream
        
        print("\n✅ Soprano TTS imported successfully")
        print("Loading model...")
        
        model = SopranoTTS(
            backend='auto',
            device='cpu',
            cache_size_mb=500,
            decoder_batch_size=2
        )
        
        print("✅ Model loaded successfully")
        
        # Test messages
        test_messages = [
            "Hello! I am JARVIS, now powered by Soprano TTS.",
            "This is a test of the new text to speech system.",
            "The quality should be much better than before."
        ]
        
        for i, message in enumerate(test_messages, 1):
            print(f"\n[Test {i}/{len(test_messages)}]")
            print(f"Message: {message}")
            print("-" * 60)
            
            try:
                stream = model.infer_stream(
                    message,
                    chunk_size=1,
                    temperature=0.3,
                    top_p=0.95,
                    repetition_penalty=1.2
                )
                
                play_stream(stream)
                print(f"✅ Test {i} completed successfully")
                
            except Exception as e:
                print(f"❌ Test {i} failed: {e}")
            
            # Small pause
            import time
            time.sleep(0.5)
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except ImportError as e:
        print(f"\n❌ Failed to import Soprano TTS: {e}")
        print("\nMake sure Soprano TTS is installed:")
        print(f"  cd {SOPRANO_PATH}")
        print("  pip install -e .")
        
    except Exception as e:
        print(f"\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    try:
        test_soprano_direct()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
