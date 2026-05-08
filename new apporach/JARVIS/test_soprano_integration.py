import sys
import os

# Add JARVIS to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'JARVIS'))

from Jarvis import JarvisAssistant

def test_soprano_tts():
    """Test Soprano TTS integration"""
    print("=" * 60)
    print("Testing JARVIS with Soprano TTS")
    print("=" * 60)
    
    # Initialize JARVIS
    jarvis = JarvisAssistant()
    
    # Test messages
    test_messages = [
        "Hello! I am JARVIS, now powered by Soprano TTS.",
        "This is a test of the new text to speech system.",
        "The quality should be much better than before.",
        "Goodbye!"
    ]
    
    print("\nStarting TTS tests...\n")
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n[Test {i}/{len(test_messages)}]")
        print(f"Message: {message}")
        print("-" * 60)
        
        success = jarvis.tts(message)
        
        if success:
            print(f"✅ Test {i} completed successfully")
        else:
            print(f"❌ Test {i} failed")
        
        # Small pause between messages
        import time
        time.sleep(0.5)
    
    print("\n" + "=" * 60)
    print("TTS Testing Complete!")
    print("=" * 60)
    
    # Check which TTS system was used
    if jarvis._use_soprano:
        print("\n✅ Using Soprano TTS (High Quality)")
    else:
        print("\n⚠️ Using PowerShell TTS (Fallback)")

if __name__ == "__main__":
    try:
        test_soprano_tts()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
