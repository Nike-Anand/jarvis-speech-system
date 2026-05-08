# JARVIS Iron Man - AI Assistant

> *"Sometimes you gotta run before you can walk."* - Tony Stark

An Iron Man-inspired AI assistant with a stunning web interface, powered by Llama3 for conversational AI and featuring all the capabilities of the original JARVIS system.

![JARVIS Status](https://img.shields.io/badge/STATUS-ONLINE-00FF88?style=for-the-badge)
![AI Model](https://img.shields.io/badge/AI-Llama3.2-00D9FF?style=for-the-badge)
![TTS](https://img.shields.io/badge/TTS-Soprano-FFD700?style=for-the-badge)

## ✨ Features

### 🤖 Conversational AI
- **Natural Language Understanding** powered by Llama3.2
- **Context-Aware Conversations** with memory across turns
- **JARVIS Personality** - witty, intelligent, and helpful

### 🎨 Premium UI
- **Iron Man Aesthetics** - Arc reactor blue theme with gold accents
- **Glassmorphism Design** - Frosted glass panels with backdrop blur
- **Voice Visualizer** - Circular waveform with arc reactor styling
- **Smooth Animations** - Pulse effects, glows, and micro-interactions
- **Responsive Layout** - Adapts to all screen sizes

### 🎤 Voice Interaction
- **Bidirectional Voice** - Speak to JARVIS and hear responses
- **Soprano TTS** - High-quality text-to-speech
- **Web Speech API** - Browser-based voice recognition
- **Real-time Visualization** - See your voice as you speak

### ⚡ System Integration
All features from the original JARVIS:
- ⏰ Time and date
- 🌤️ Weather information
- 📰 News headlines
- 📊 System statistics (CPU, RAM, Battery)
- 📚 Wikipedia search
- 🌐 Web search and website opening
- 🚀 Application launcher
- 😂 Jokes and entertainment

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed
2. **Ollama** installed with Llama3 model
   ```bash
   # Install Ollama from https://ollama.ai
   # Then pull the model:
   ollama pull llama3.2
   ```
3. **Soprano TTS** (already integrated from existing JARVIS)

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd "c:\D\Projects\jarvis\new apporach\JARVIS\jarvis-ironman"
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Ollama is running:**
   ```bash
   ollama list
   # Should show llama3.2:latest
   ```

### Running JARVIS

1. **Start the server:**
   ```bash
   cd backend
   python server.py
   ```

2. **Open your browser:**
   ```
   http://localhost:5000
   ```

3. **Start talking to JARVIS!**
   - Type messages in the chat input
   - Click the microphone button for voice input
   - Use quick action buttons for common tasks

## 🏗️ Architecture

```
jarvis-ironman/
├── backend/
│   ├── server.py           # FastAPI server with WebSocket
│   ├── jarvis_ai.py        # Llama3 conversational AI engine
│   ├── jarvis_bridge.py    # Integration with existing JARVIS
│   └── config.py           # Configuration settings
├── frontend/
│   ├── index.html          # Main UI structure
│   ├── styles.css          # Iron Man-inspired styling
│   └── app.js              # Frontend application logic
└── requirements.txt        # Python dependencies
```

### Technology Stack

**Backend:**
- FastAPI - Modern web framework
- WebSocket - Real-time bidirectional communication
- Ollama - Llama3 model integration
- Soprano TTS - High-quality speech synthesis

**Frontend:**
- Vanilla JavaScript - No framework overhead
- WebSocket API - Real-time chat streaming
- Web Speech API - Voice recognition
- Canvas API - Voice visualization

## 💬 Usage Examples

### Chat Commands

```
"What time is it?"
"Tell me the weather in New York"
"What's in the news today?"
"Show me system stats"
"Tell me about quantum computing"
"Search for Python tutorials"
"Open google.com"
"Tell me a joke"
```

### Voice Commands

Click the microphone button and say:
- "Hey JARVIS, what's the weather like?"
- "JARVIS, tell me the time"
- "What's my system status?"

### Quick Actions

Use the sidebar buttons for instant access to:
- ⏰ Current time
- 🌤️ Weather updates
- 📰 Latest news
- ⚙️ System statistics

## 🎨 UI Customization

Edit `backend/config.py` to customize:

```python
UI_THEME = {
    "primary_color": "#00D9FF",      # Arc reactor blue
    "secondary_color": "#0099CC",    # Darker blue
    "accent_color": "#FFD700",       # Gold
    # ... more colors
}
```

## 🔧 Configuration

### Ollama Settings
```python
OLLAMA_MODEL = "llama3.2:latest"
OLLAMA_TEMPERATURE = 0.7
OLLAMA_TOP_P = 0.9
```

### Server Settings
```python
SERVER_HOST = "localhost"
SERVER_PORT = 5000
```

### Voice Settings
```python
WAKE_WORDS = ["jarvis", "hey jarvis", "ok jarvis"]
VOICE_RECOGNITION_LANGUAGE = "en-in"
```

## 🐛 Troubleshooting

### WebSocket Connection Failed
- Ensure the server is running on port 5000
- Check firewall settings
- Try accessing via `http://127.0.0.1:5000`

### Ollama Not Found
```bash
# Verify Ollama is installed and running
ollama list
ollama serve  # Start Ollama service if needed
```

### Voice Recognition Not Working
- Use Chrome or Edge browser (best support)
- Allow microphone permissions
- Check browser console for errors

### TTS Not Working
- Verify Soprano TTS path in `config.py`
- Check existing JARVIS integration
- Fallback to PowerShell TTS is automatic

## 🎯 Roadmap

- [ ] Multi-language support
- [ ] Custom wake word training
- [ ] Mobile app version
- [ ] Advanced voice commands
- [ ] Integration with smart home devices
- [ ] Persistent conversation history

## 📝 License

MIT License - Same as original JARVIS project

## 🙏 Credits

- **Original JARVIS** - Base functionality and features
- **Soprano TTS** - High-quality text-to-speech
- **Ollama & Llama3** - Conversational AI capabilities
- **Iron Man** - Inspiration for the UI design

---

**Built with ❤️ and inspired by Tony Stark's JARVIS**

*"JARVIS, sometimes you gotta run before you can walk."*
