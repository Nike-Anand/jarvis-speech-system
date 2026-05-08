# JARVIS Setup Guide

## ✅ Completed Steps:
1. Repository cloned successfully
2. Essential packages installed
3. Config file prepared

## 🔧 Required API Keys Setup:

### 1. **Email Configuration**
- Update `JARVIS/config/config.py` with your Gmail credentials
- Use Gmail App Password (not regular password)
- Enable 2-factor authentication and generate app password

### 2. **Wolframalpha API**
- Visit: https://developer.wolframalpha.com/
- Create free account and get API key
- Add to config file

### 3. **OpenWeather API** 
- Visit: https://openweathermap.org/api
- Get free API key
- Add to config file

### 4. **Google Calendar API** (Optional)
- Visit: https://console.developers.google.com/
- Enable Calendar API
- Download credentials.json

## 🚀 Running JARVIS:

```bash
cd "c:\D\Projects\jarvis\new apporach\JARVIS"
python main.py
```

## 🎯 Voice Commands Examples:
- "Hello Jarvis" - Activate
- "What time is it?" - Current time
- "Open Google" - Open websites
- "Weather in London" - Weather info
- "Tell me about Python" - Wikipedia search
- "Play music" - YouTube search
- "Take screenshot" - Screen capture
- "System status" - PC stats
- "Goodbye" - Exit

## 📝 Notes:
- Ensure microphone permissions are enabled
- Chrome browser required for web automation
- Some features may need additional setup