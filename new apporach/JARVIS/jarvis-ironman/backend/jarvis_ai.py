"""
JARVIS AI Engine - Conversational AI with Llama3
"""
import ollama
from typing import List, Dict, Optional
import json
import re
from duckduckgo_search import DDGS
from config import (
    OLLAMA_MODEL, OLLAMA_TEMPERATURE, OLLAMA_TOP_P, 
    OLLAMA_MAX_TOKENS, JARVIS_SYSTEM_PROMPT, OLLAMA_BASE_URL,
    WEB_SEARCH_ENABLED, WEB_SEARCH_MAX_RESULTS, WEB_SEARCH_KEYWORDS
)
from jarvis_bridge import JarvisBridge

# Use simple vision service instead of complex dependencies
try:
    from simple_vision import SimpleVisionService
    vision_service = SimpleVisionService()
    _FEATURES_AVAILABLE = True
    print("[JarvisAI] Vision service loaded successfully (using Ollama)")
except Exception as e:
    print(f"[JarvisAI] Vision service not available: {e}")
    vision_service = None
    _FEATURES_AVAILABLE = False


class JarvisAI:
    """JARVIS Conversational AI Engine using Llama3"""
    
    def __init__(self):
        """Initialize JARVIS AI"""
        self.conversation_history: List[Dict[str, str]] = []
        self.jarvis_bridge = JarvisBridge()
        self.system_prompt = JARVIS_SYSTEM_PROMPT
        self.features_available = _FEATURES_AVAILABLE
        
        # Initialize conversation with system prompt
        self.conversation_history.append({
            "role": "system",
            "content": self.system_prompt
        })
        
        # Use simple vision service
        self.vision = vision_service
        self.features_available = _FEATURES_AVAILABLE
        
        print("[JarvisAI] Initialized with Llama3 model:", OLLAMA_MODEL)
        
        # Initialize feature detector
        try:
            from feature_detector import FeatureDetector
            self.feature_detector = FeatureDetector(self)
            print("[JarvisAI] Feature detector initialized")
        except Exception as e:
            print(f"[JarvisAI] Feature detector not available: {e}")
            self.feature_detector = None
    
    def _search_web(self, query: str) -> Optional[str]:
        """Search the web using DuckDuckGo"""
        if not WEB_SEARCH_ENABLED:
            return None
        
        try:
            print(f"[JarvisAI] Searching web for: {query}")
            with DDGS() as ddgs:
                results = list(ddgs.text(query, max_results=WEB_SEARCH_MAX_RESULTS))
            
            if not results:
                return None
            
            # Format results concisely
            search_summary = f"Web search results for '{query}':\n"
            for i, result in enumerate(results, 1):
                title = result.get('title', 'No title')
                snippet = result.get('body', 'No description')
                search_summary += f"{i}. {title}: {snippet[:150]}...\n"
            
            return search_summary
        except Exception as e:
            print(f"[JarvisAI] Web search error: {e}")
            return None
    
    def _needs_web_search(self, message: str) -> bool:
        """Check if message requires web search"""
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in WEB_SEARCH_KEYWORDS)
    
    def _detect_intent(self, user_message: str) -> Optional[Dict]:
        """Detect user intent and extract parameters"""
        user_lower = user_message.lower()
        
        # Time intent
        if any(word in user_lower for word in ["time", "what time", "current time"]):
            return {"intent": "get_time", "params": {}}
        
        # Date intent
        if any(word in user_lower for word in ["date", "what date", "today", "what day"]):
            return {"intent": "get_date", "params": {}}
        
        # Weather intent
        weather_patterns = [
            r"weather\s+(?:in|at|for)?\s*([a-zA-Z\s]+)",
            r"how(?:'s| is) the weather\s+(?:in|at)?\s*([a-zA-Z\s]+)",
            r"what(?:'s| is) the weather\s+(?:in|at)?\s*([a-zA-Z\s]+)"
        ]
        for pattern in weather_patterns:
            match = re.search(pattern, user_lower)
            if match:
                city = match.group(1).strip()
                return {"intent": "get_weather", "params": {"city": city}}
        
        if "weather" in user_lower:
            return {"intent": "get_weather", "params": {"city": "default"}}
        
        # News intent
        if any(word in user_lower for word in ["news", "headlines", "latest news"]):
            return {"intent": "get_news", "params": {}}
        
        # System stats intent
        if any(word in user_lower for word in ["system", "cpu", "ram", "battery", "system stats", "system status"]):
            return {"intent": "get_system_stats", "params": {}}
        
        # Wikipedia intent
        wiki_patterns = [
            r"(?:tell me about|who is|what is|search for)\s+(.+)",
            r"wikipedia\s+(.+)"
        ]
        for pattern in wiki_patterns:
            match = re.search(pattern, user_lower)
            if match:
                topic = match.group(1).strip()
                # Avoid false positives
                if topic and len(topic) > 2 and "weather" not in topic:
                    return {"intent": "search_wikipedia", "params": {"topic": topic}}
        
        # Website opening intent
        website_patterns = [
            r"open\s+([a-zA-Z0-9\-\.]+(?:\.com|\.org|\.net|\.io))",
            r"go to\s+([a-zA-Z0-9\-\.]+(?:\.com|\.org|\.net|\.io))"
        ]
        for pattern in website_patterns:
            match = re.search(pattern, user_lower)
            if match:
                domain = match.group(1).strip()
                return {"intent": "open_website", "params": {"domain": domain}}
        
        # Google search intent
        if "google" in user_lower or "search for" in user_lower:
            search_patterns = [
                r"(?:google|search for)\s+(.+)",
                r"search\s+(.+)"
            ]
            for pattern in search_patterns:
                match = re.search(pattern, user_lower)
                if match:
                    query = match.group(1).strip()
                    return {"intent": "google_search", "params": {"query": query}}
        
        # Joke intent
        if any(word in user_lower for word in ["joke", "make me laugh", "tell me a joke"]):
            return {"intent": "tell_joke", "params": {}}
        
        return None
    
    def _execute_action(self, intent_data: Dict) -> str:
        """Execute detected action and return result"""
        intent = intent_data["intent"]
        params = intent_data["params"]
        
        try:
            if intent == "get_time":
                time_str = self.jarvis_bridge.get_time()
                return f"The current time is {time_str}."
            
            elif intent == "get_date":
                date_str = self.jarvis_bridge.get_date()
                return f"Today is {date_str}."
            
            elif intent == "get_weather":
                city = params.get("city", "default")
                weather_info = self.jarvis_bridge.get_weather(city)
                if weather_info:
                    return f"Weather information: {weather_info}"
                return "I couldn't retrieve the weather information at the moment."
            
            elif intent == "get_news":
                news = self.jarvis_bridge.get_news()
                if news and isinstance(news, list):
                    headlines = "\n".join([f"• {item}" for item in news[:5]])
                    return f"Here are the top headlines:\n{headlines}"
                return "I couldn't fetch the news at the moment."
            
            elif intent == "get_system_stats":
                stats = self.jarvis_bridge.get_system_stats()
                return f"System status: {stats}"
            
            elif intent == "search_wikipedia":
                topic = params.get("topic")
                info = self.jarvis_bridge.search_wikipedia(topic)
                if info:
                    return info
                return f"I couldn't find information about {topic} on Wikipedia."
            
            elif intent == "open_website":
                domain = params.get("domain")
                self.jarvis_bridge.open_website(domain)
                return f"Opening {domain} for you."
            
            elif intent == "google_search":
                query = params.get("query")
                self.jarvis_bridge.google_search(query)
                return f"Searching Google for '{query}'."
            
            elif intent == "tell_joke":
                try:
                    import pyjokes
                    joke = pyjokes.get_joke()
                    return joke
                except:
                    return "Why did the AI go to school? To improve its learning algorithms!"
            
            return "Action executed successfully."
            
        except Exception as e:
            print(f"[JarvisAI] Error executing action: {e}")
            return f"I encountered an error while executing that action: {str(e)}"
    
    def chat(self, user_message: str, image_data: Optional[bytes] = None) -> str:
        """
        Process user message and generate response
        image_data: Optional image bytes for OCR/object detection
        Returns: AI response text
        """
        # Check for feature execution first (especially for image-based features)
        if self.feature_detector and (image_data or self.feature_detector):
            try:
                feature_executed, result = self.feature_detector.detect_and_execute(user_message, image_data)
                if feature_executed and result:
                    if result.get("success"):
                        # Feature executed successfully - format response
                        return self._format_feature_response(user_message, result)
                    else:
                        # Feature failed - return error
                        return f"I tried to execute that, but encountered an error: {result.get('error', 'Unknown error')}"
            except Exception as e:
                print(f"[JarvisAI] Feature detection error: {e}")
        
        # Check if web search is needed
        web_results = None
        if self._needs_web_search(user_message):
            web_results = self._search_web(user_message)
        
        # Detect intent
        intent_data = self._detect_intent(user_message)
        
        # If intent detected, execute action
        action_result = None
        if intent_data:
            print(f"[JarvisAI] Detected intent: {intent_data['intent']}")
            action_result = self._execute_action(intent_data)
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Build context with web results and/or action results
        context_parts = [f"User request: {user_message}"]
        if web_results:
            context_parts.append(f"Web search results:\n{web_results}")
        if action_result:
            context_parts.append(f"Action result: {action_result}")
        
        if web_results or action_result:
            context_parts.append("\nProvide a brief, natural response (1-2 sentences) incorporating this information.")
            context_message = "\n".join(context_parts)
            messages = self.conversation_history[:-1] + [{
                "role": "user",
                "content": context_message
            }]
        else:
            messages = self.conversation_history
        
        try:
            # Generate response using Ollama
            response = ollama.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                options={
                    "temperature": OLLAMA_TEMPERATURE,
                    "top_p": OLLAMA_TOP_P,
                    "num_predict": OLLAMA_MAX_TOKENS
                }
            )
            
            ai_response = response['message']['content']
            
            # Add AI response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": ai_response
            })
            
            # Keep conversation history manageable (last 6 exchanges)
            if len(self.conversation_history) > 13:  # system + 6 exchanges
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-12:]
            
            return ai_response
            
        except Exception as e:
            print(f"[JarvisAI] Error generating response: {e}")
            if action_result:
                return action_result
            if web_results:
                return "Here's what I found: " + web_results
            return "I apologize, but I'm having trouble processing that request at the moment."
    
    def chat_stream(self, user_message: str):
        """
        Stream AI response token by token
        Yields: chunks of response text
        """
        # Check if web search is needed
        web_results = None
        if self._needs_web_search(user_message):
            web_results = self._search_web(user_message)
        
        # Detect intent
        intent_data = self._detect_intent(user_message)
        
        # If intent detected, execute action
        action_result = None
        if intent_data:
            print(f"[JarvisAI] Detected intent: {intent_data['intent']}")
            action_result = self._execute_action(intent_data)
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        # Build context with web results and/or action results
        context_parts = [f"User request: {user_message}"]
        if web_results:
            context_parts.append(f"Web search results:\n{web_results}")
        if action_result:
            context_parts.append(f"Action result: {action_result}")
        
        if web_results or action_result:
            context_parts.append("\nProvide a brief, natural response (1-2 sentences) incorporating this information.")
            context_message = "\n".join(context_parts)
            messages = self.conversation_history[:-1] + [{
                "role": "user",
                "content": context_message
            }]
        else:
            messages = self.conversation_history
        
        try:
            # Stream response using Ollama
            stream = ollama.chat(
                model=OLLAMA_MODEL,
                messages=messages,
                stream=True,
                options={
                    "temperature": OLLAMA_TEMPERATURE,
                    "top_p": OLLAMA_TOP_P,
                    "num_predict": OLLAMA_MAX_TOKENS
                }
            )
            
            full_response = ""
            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    content = chunk['message']['content']
                    full_response += content
                    yield content
            
            # Add complete response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": full_response
            })
            
            # Keep conversation history manageable
            if len(self.conversation_history) > 13:
                self.conversation_history = [self.conversation_history[0]] + self.conversation_history[-12:]
                
        except Exception as e:
            print(f"[JarvisAI] Error streaming response: {e}")
            if action_result:
                yield action_result
            elif web_results:
                yield "Here's what I found: " + web_results
            else:
                yield "I apologize, but I'm having trouble processing that request at the moment."
    
    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = [{
            "role": "system",
            "content": self.system_prompt
        }]
        print("[JarvisAI] Conversation history reset")
