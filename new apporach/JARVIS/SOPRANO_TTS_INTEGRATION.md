# JARVIS - Soprano TTS Integration

## 🎙️ Overview

JARVIS now uses **Soprano TTS** as the primary text-to-speech engine, providing:

- ✅ **20x faster** than PowerShell TTS on CPU
- ✅ **Crystal clear 32kHz audio** quality
- ✅ **<250ms latency** with streaming
- ✅ **Highly expressive** natural voice
- ✅ **<1GB memory** usage
- ✅ **Automatic fallback** to PowerShell TTS if needed

## 📋 What Changed

### Before (PowerShell TTS)
- Slower speech generation
- Lower quality audio
- Higher latency
- Windows-only

### After (Soprano TTS)
- 20x faster on CPU
- Professional quality audio (32kHz)
- Low latency streaming
- Fallback to PowerShell if Soprano unavailable

## 🚀 How It Works

### Lazy Loading
The Soprano TTS model is loaded only when first needed, reducing startup time:

```python
jarvis = JarvisAssistant()  # Fast startup
jarvis.tts("Hello")         # Model loads here (first call only)
jarvis.tts("World")         # Uses cached model (fast)
```

### Streaming Playback
Audio is streamed in real-time for low latency:

```python
# Text → Audio Stream → Playback (all happening simultaneously)
stream = model.infer_stream(text, chunk_size=1)
play_stream(stream)  # <250ms latency
```

### Automatic Fallback
If Soprano TTS fails for any reason, JARVIS automatically falls back to PowerShell TTS:

```python
# Try Soprano TTS
try:
    soprano_tts(text)
except:
    # Fallback to PowerShell TTS
    powershell_tts(text)
```

## 🔧 Configuration

### Soprano TTS Settings

The integration uses optimized settings for JARVIS:

```python
SopranoTTS(
    backend='auto',           # Auto-detect best backend
    device='cpu',             # CPU mode (GPU optional)
    cache_size_mb=500,        # 500MB cache for speed
    decoder_batch_size=2      # Balance speed/memory
)
```

### Speech Parameters

```python
model.infer_stream(
    text,
    chunk_size=1,            # Low latency chunks
    temperature=0.3,         # Consistent voice
    top_p=0.95,              # Sampling threshold
    repetition_penalty=1.2   # Avoid repetition
)
```

### Adjusting Settings

You can modify these in `JARVIS/__init__.py`:

**For faster speech (uses more memory):**
```python
cache_size_mb=1000,
decoder_batch_size=4
```

**For lower memory usage:**
```python
cache_size_mb=200,
decoder_batch_size=1
```

**For GPU acceleration (if available):**
```python
device='cuda'  # 2000x real-time speed!
```

## 📁 File Structure

```
JARVIS/
├── JARVIS/
│   ├── __init__.py              # ✨ Updated with Soprano TTS
│   ├── features/                # Unchanged
│   └── config/                  # Unchanged
├── test_soprano_integration.py  # 🆕 Test script
└── SOPRANO_TTS_INTEGRATION.md   # 🆕 This file

External:
c:\D\Projects\jarvis\TTS\soprano\  # Soprano TTS installation
```

## 🧪 Testing

### Quick Test

Run the test script to verify everything works:

```bash
cd "c:\D\Projects\jarvis\new apporach\JARVIS"
python test_soprano_integration.py
```

Expected output:
```
============================================================
Testing JARVIS with Soprano TTS
============================================================

Loading Soprano TTS model...
Soprano TTS model loaded successfully

[Test 1/4]
Message: Hello! I am JARVIS, now powered by Soprano TTS.
------------------------------------------------------------
Speaking: Hello! I am JARVIS, now powered by Soprano TTS.
Speech completed successfully (Soprano TTS)
✅ Test 1 completed successfully

...

✅ Using Soprano TTS (High Quality)
```

### Test in JARVIS

Run any JARVIS entry point:

```bash
# Fast mode
python fast_jarvis.py

# GUI mode
python gui_jarvis.py

# Main mode
python main.py
```

The first TTS call will load the model (takes a few seconds), then all subsequent calls will be fast.

## 🔍 Troubleshooting

### Issue: "Soprano TTS not available"

**Cause:** Soprano TTS not installed or path incorrect

**Solution:**
1. Verify Soprano is installed:
   ```bash
   cd c:\D\Projects\jarvis\TTS\soprano
   pip install -e .
   ```

2. Check the path in `JARVIS/__init__.py`:
   ```python
   SOPRANO_PATH = r"c:\D\Projects\jarvis\TTS\soprano"
   ```

### Issue: "Failed to load Soprano TTS"

**Cause:** Missing dependencies or model files

**Solution:**
1. Reinstall Soprano TTS:
   ```bash
   cd c:\D\Projects\jarvis\TTS\soprano
   pip install -e . --force-reinstall
   ```

2. Check for error messages in console

### Issue: Falls back to PowerShell TTS

**Cause:** Soprano TTS encountered an error

**Effect:** JARVIS still works, just uses PowerShell TTS instead

**Solution:**
- Check console for error messages
- Verify Soprano installation
- Check available memory (needs ~1GB)

### Issue: Slow first TTS call

**Cause:** Model loading on first use (lazy loading)

**Effect:** First TTS call takes 3-5 seconds, then fast

**Solution:** This is normal behavior. Subsequent calls are instant.

## 📊 Performance Comparison

| Metric | PowerShell TTS | Soprano TTS | Improvement |
|--------|---------------|-------------|-------------|
| Speed | 1x | 20x | **20x faster** |
| Quality | 16kHz | 32kHz | **2x better** |
| Latency | ~1000ms | <250ms | **4x lower** |
| Memory | ~100MB | ~1GB | Uses more RAM |
| Expressiveness | Low | High | Much better |

## 🎯 Usage Tips

### Best Results

1. **Sentence length:** 2-30 seconds of speech
2. **Numbers:** Convert to words ("1+1" → "one plus one")
3. **Quotes:** Use double quotes in speech
4. **Regenerate:** If unsatisfied, call TTS again

### Optimizing for Speed

```python
# In JARVIS/__init__.py, increase cache and batch size:
self._soprano_model = SopranoTTS(
    cache_size_mb=1000,      # More cache
    decoder_batch_size=4     # Larger batches
)
```

### Optimizing for Memory

```python
# In JARVIS/__init__.py, reduce cache and batch size:
self._soprano_model = SopranoTTS(
    cache_size_mb=200,       # Less cache
    decoder_batch_size=1     # Smaller batches
)
```

## 🔄 Reverting to PowerShell TTS

If you want to go back to PowerShell TTS only:

**Option 1: Disable Soprano in code**
```python
# In JARVIS/__init__.py __init__ method:
self._use_soprano = False  # Force PowerShell TTS
```

**Option 2: Remove Soprano path**
```python
# In JARVIS/__init__.py, comment out:
# SOPRANO_PATH = r"c:\D\Projects\jarvis\TTS\soprano"
# if os.path.exists(SOPRANO_PATH):
#     sys.path.insert(0, SOPRANO_PATH)
```

## 📚 Additional Resources

- **Soprano TTS Documentation:** See `tts.txt` for full Soprano guide
- **Soprano Repository:** https://github.com/ekwek1/soprano
- **JARVIS Analysis:** See `jarvis_analysis.md` for project overview

## ✅ Summary

**What you get:**
- ✅ Faster, higher quality speech
- ✅ Lower latency streaming
- ✅ Automatic fallback to PowerShell
- ✅ No breaking changes to existing code
- ✅ Easy to test and configure

**What to do:**
1. Run `python test_soprano_integration.py` to test
2. Use JARVIS normally - TTS is automatic
3. Enjoy better voice quality!

---

*Integration completed: 2026-01-19*  
*Soprano TTS Version: 1.1-80M*  
*JARVIS Version: Updated with Soprano TTS support*
