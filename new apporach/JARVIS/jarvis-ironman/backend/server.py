"""
JARVIS Iron Man - Web Server
FastAPI server with WebSocket support for real-time communication
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import json
from pathlib import Path
import uvicorn

from jarvis_ai import JarvisAI
from jarvis_bridge import JarvisBridge
from config import SERVER_HOST, SERVER_PORT, DEBUG_MODE, CORS_ORIGINS
from fastapi import File, UploadFile, Form
import base64

# Initialize FastAPI app
app = FastAPI(title="JARVIS Iron Man", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS + ["*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize JARVIS AI
jarvis_ai = JarvisAI()
jarvis_bridge = JarvisBridge()

# Store active WebSocket connections
active_connections: list[WebSocket] = []


# ============================================================================
# STATIC FILES & ROOT
# ============================================================================

# Mount frontend directory
frontend_dir = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


@app.get("/")
async def root():
    """Serve the main HTML page"""
    html_file = frontend_dir / "index.html"
    with open(html_file, "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())


# ============================================================================
# WEBSOCKET ENDPOINT
# ============================================================================

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    active_connections.append(websocket)
    
    print(f"[WebSocket] Client connected. Total connections: {len(active_connections)}")
    
    # Send welcome message
    await websocket.send_json({
        "type": "system",
        "message": "JARVIS online and ready, sir."
    })
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            if message_type == "chat":
                # Handle chat message
                user_message = data.get("message", "")
                print(f"[WebSocket] Received: {user_message}")
                
                # Send acknowledgment
                await websocket.send_json({
                    "type": "chat_start",
                    "message": user_message
                })
                
                # Stream AI response
                full_response = ""
                for chunk in jarvis_ai.chat_stream(user_message):
                    full_response += chunk
                    await websocket.send_json({
                        "type": "chat_chunk",
                        "chunk": chunk
                    })
                    await asyncio.sleep(0.01)  # Small delay for smooth streaming
                
                # Send completion
                await websocket.send_json({
                    "type": "chat_complete",
                    "message": full_response
                })
                
                # Speak the response using TTS
                if jarvis_bridge.available:
                    # Run TTS in background to not block WebSocket
                    asyncio.create_task(speak_async(full_response))
            
            elif message_type == "voice":
                # Handle voice input
                voice_text = data.get("text", "")
                print(f"[WebSocket] Voice input: {voice_text}")
                
                # Process same as chat
                await websocket.send_json({
                    "type": "chat_start",
                    "message": voice_text
                })
                
                full_response = ""
                for chunk in jarvis_ai.chat_stream(voice_text):
                    full_response += chunk
                    await websocket.send_json({
                        "type": "chat_chunk",
                        "chunk": chunk
                    })
                    await asyncio.sleep(0.01)
                
                await websocket.send_json({
                    "type": "chat_complete",
                    "message": full_response
                })
                
                # Speak response
                if jarvis_bridge.available:
                    asyncio.create_task(speak_async(full_response))
            
            elif message_type == "reset":
                # Reset conversation
                jarvis_ai.reset_conversation()
                await websocket.send_json({
                    "type": "system",
                    "message": "Conversation reset."
                })
            
            elif message_type == "system_stats":
                # Get system stats
                if jarvis_bridge.available:
                    stats = jarvis_bridge.get_system_stats()
                    await websocket.send_json({
                        "type": "system_stats",
                        "data": stats
                    })
    
    except WebSocketDisconnect:
        active_connections.remove(websocket)
        print(f"[WebSocket] Client disconnected. Total connections: {len(active_connections)}")
    except Exception as e:
        print(f"[WebSocket] Error: {e}")
        if websocket in active_connections:
            active_connections.remove(websocket)


async def speak_async(text: str):
    """Speak text asynchronously"""
    try:
        # Run TTS in executor to avoid blocking
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, jarvis_bridge.speak, text)
    except Exception as e:
        print(f"[TTS] Error: {e}")


# ============================================================================
# REST API ENDPOINTS
# ============================================================================

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "online",
        "jarvis_available": jarvis_bridge.available,
        "model": "llama3.2:latest"
    }


@app.get("/api/system-stats")
async def get_system_stats():
    """Get system statistics"""
    if jarvis_bridge.available:
        stats = jarvis_bridge.get_system_stats()
        return {"success": True, "data": stats}
    return {"success": False, "error": "JARVIS bridge not available"}


@app.post("/api/speak")
async def speak_text(data: dict):
    """Speak text using TTS"""
    text = data.get("text", "")
    if jarvis_bridge.available and text:
        success = jarvis_bridge.speak(text)
        return {"success": success}
    return {"success": False}


@app.post("/api/upload-image")
async def upload_image(file: UploadFile = File(...), message: str = Form(...)):
    """Handle image upload and process with features"""
    try:
        # Read image data
        image_data = await file.read()
        
        # Process with JARVIS AI (includes feature detection)
        response = jarvis_ai.chat(message, image_data=image_data)
        
        return {
            "success": True,
            "response": response
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


@app.post("/api/execute-feature")
async def execute_feature(data: dict):
    """Execute a specific feature"""
    try:
        feature = data.get("feature")
        params = data.get("params", {})
        
        result = None
        
        if feature == "screenshot" and hasattr(jarvis_ai, 'automation'):
            result = jarvis_ai.automation.screenshot()
        elif feature == "analyze" and hasattr(jarvis_ai, 'ml'):
            numbers = params.get("numbers", [])
            result = jarvis_ai.ml.analyze_data(numbers)
        elif feature == "scrape" and hasattr(jarvis_ai, 'scraper'):
            url = params.get("url")
            result = jarvis_ai.scraper.scrape_url(url)
        elif feature == "generate_ppt" and hasattr(jarvis_ai, 'ppt'):
            title = params.get("title", "Presentation")
            content = params.get("content", "")
            result = jarvis_ai.ppt.create_from_text(content, title)
        
        return result if result else {"success": False, "error": "Feature not available"}
        
    except Exception as e:
        return {"success": False, "error": str(e)}


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Start the server"""
    print("=" * 60)
    print("JARVIS IRON MAN - Starting Server")
    print("=" * 60)
    print(f"Server: http://{SERVER_HOST}:{SERVER_PORT}")
    print(f"WebSocket: ws://{SERVER_HOST}:{SERVER_PORT}/ws")
    print("=" * 60)
    
    uvicorn.run(
        app,
        host=SERVER_HOST,
        port=SERVER_PORT,
        log_level="info" if DEBUG_MODE else "warning"
    )


if __name__ == "__main__":
    main()
