# Soprano TTS Setup Guide

## Installation

Successfully installed Soprano TTS in `c:\D\Projects\jarvis\TTS\soprano`

### Installation Steps Completed:
1. ✅ Cloned repository with `git clone --depth 1 https://github.com/ekwek1/soprano.git`
2. ✅ Installed dependencies with `pip install -e .` (CPU version)
3. ✅ All dependencies installed successfully

## Project Structure

```
TTS/
├── soprano/              # Main Soprano repository
│   ├── soprano/         # Python package
│   │   ├── __init__.py
│   │   ├── tts.py       # Main TTS class
│   │   ├── cli.py       # CLI interface
│   │   ├── webui.py     # Web UI
│   │   ├── server.py    # API server
│   │   ├── backends/    # Inference backends
│   │   ├── utils/       # Utilities
│   │   └── vocos/       # Decoder
│   └── examples/        # Example scripts
├── test_soprano.py      # Comprehensive test script
├── simple_example.py    # Quick start example
└── streaming_example.py # Streaming demo
```

## Usage Examples

### 1. Simple Usage (Python Script)

```python
from soprano.tts import SopranoTTS

# Initialize
model = SopranoTTS(backend='auto', device='cpu')

# Generate speech
model.infer("Hello world!", "output.wav")
```

### 2. CLI Usage

```bash
# Basic generation
soprano "Your text here"

# With custom output file
soprano "Your text here" --output my_audio.wav

# Enable streaming playback
soprano "Your text here" --streaming
```

### 3. Web UI

```bash
# Start web interface
soprano-webui

# With performance optimizations
soprano-webui --cache-size 1000 --decoder-batch-size 4
```

### 4. API Server

```bash
# Start server
uvicorn soprano.server:app --host 0.0.0.0 --port 8000

# Use API
curl http://localhost:8000/v1/audio/speech \
  -H "Content-Type: application/json" \
  -d '{"input": "Your text here"}' \
  --output speech.wav
```

### 5. Streaming (Low Latency)

```python
from soprano.tts import SopranoTTS
from soprano.utils.streaming import play_stream

model = SopranoTTS(backend='auto', device='cpu')
stream = model.infer_stream("Your text here", chunk_size=1)
play_stream(stream)  # <15ms latency on GPU, <250ms on CPU
```

## Performance Tips

1. **Increase cache size** for faster inference (uses more memory):
   ```python
   model = SopranoTTS(cache_size_mb=1000)
   ```

2. **Increase decoder batch size** for speed (uses more memory):
   ```python
   model = SopranoTTS(decoder_batch_size=4)
   ```

3. **Use GPU** for 2000x real-time generation:
   ```python
   model = SopranoTTS(device='cuda')
   ```

## Usage Tips

- Use **double quotes** instead of single quotes when quoting
- Best results with sentences **2-30 seconds long**
- Convert numbers to phonetic form: `1+1` → `one plus one`
- Regenerate if results are unsatisfactory
- Adjust sampling parameters for variation:
  ```python
  model.infer(text, temperature=0.3, top_p=0.95, repetition_penalty=1.2)
  ```

## Example Scripts

Run the provided example scripts:

```bash
# Simple example
python simple_example.py

# Comprehensive tests
python test_soprano.py

# Streaming demo
python streaming_example.py
```

## Features

- ✅ **20x real-time** on CPU
- ✅ **2000x real-time** on GPU
- ✅ **<250ms latency** streaming on CPU
- ✅ **<15ms latency** streaming on GPU
- ✅ **<1GB memory** usage
- ✅ **32kHz** crystal clear audio
- ✅ Infinite generation length
- ✅ Highly expressive output

## Model Information

- **Model**: Soprano-1.1-80M
- **Parameters**: 80M
- **Sample Rate**: 32kHz
- **Backend**: Transformers (CPU), LMDeploy (GPU - optional)
- **Device**: CPU (current setup)

## Next Steps

1. Run `python test_soprano.py` to generate sample audio
2. Try the web UI with `soprano-webui`
3. Experiment with different sampling parameters
4. For production use, consider setting up the API server
