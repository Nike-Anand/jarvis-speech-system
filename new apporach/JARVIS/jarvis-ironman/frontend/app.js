/**
 * JARVIS AI - MINIMALIST 3D ORB INTERFACE
 * 3D animated golden AI orb with particle effects
 */

// ============================================================================
// STATE & CONFIGURATION
// ============================================================================

let ws = null;
let isConnected = false;
let isListening = false;

// DOM Elements
const elements = {
    statusBadge: document.getElementById('statusBadge'),
    statusText: document.querySelector('.status-text'),
    statusDot: document.querySelector('.status-dot'),
    chatMessages: document.getElementById('chatMessages'),
    chatInput: document.getElementById('chatInput'),
    sendBtn: document.getElementById('sendBtn'),
    voiceBtn: document.getElementById('voiceBtn'),
    uploadBtn: document.getElementById('uploadBtn'),
    fileInput: document.getElementById('fileInput'),
    chatOverlay: document.getElementById('chatOverlay'),
    notificationContainer: document.getElementById('notificationContainer'),
    aiOrb: document.getElementById('aiOrb')
};

// 3D Orb Animation
let orbCanvas, orbCtx;
let particles = [];
let isAISpeaking = false;
let vibrationIntensity = 0;
let glowIntensity = 1;
let orbRotation = 0;
let animationId = null;

// ============================================================================
// 3D AI ORB ANIMATION
// ============================================================================

class Particle {
    constructor(x, y, z) {
        this.x = x;
        this.y = y;
        this.z = z;
        this.baseX = x;
        this.baseY = y;
        this.baseZ = z;
        this.angle = Math.random() * Math.PI * 2;
        this.speed = 0.001 + Math.random() * 0.002;
        this.radius = 1 + Math.random() * 2;
        this.alpha = 0.3 + Math.random() * 0.7;
        this.vibrationOffset = Math.random() * Math.PI * 2;
    }

    update() {
        this.angle += this.speed;

        // Add vibration when AI is speaking
        let vibX = 0, vibY = 0, vibZ = 0;
        if (isAISpeaking && vibrationIntensity > 0) {
            vibX = Math.sin(this.angle * 10 + this.vibrationOffset) * vibrationIntensity;
            vibY = Math.cos(this.angle * 10 + this.vibrationOffset) * vibrationIntensity;
            vibZ = Math.sin(this.angle * 15 + this.vibrationOffset) * vibrationIntensity;
        }
        this.x = this.baseX + Math.cos(this.angle) * 5 + vibX;
        this.y = this.baseY + vibY;
        this.z = this.baseZ + Math.sin(this.angle) * 5 + vibZ;
    }

    project(centerX, centerY, scale) {
        const perspective = 400;
        const z = this.z + 200;
        const scale3d = perspective / (perspective + z);

        return {
            x: centerX + this.x * scale3d * scale,
            y: centerY + this.y * scale3d * scale,
            radius: this.radius * scale3d,
            alpha: this.alpha * scale3d
        };
    }
}

function initOrb() {
    orbCanvas = elements.aiOrb;
    orbCtx = orbCanvas.getContext('2d');

    // Set canvas size
    orbCanvas.width = window.innerWidth;
    orbCanvas.height = window.innerHeight - 100; // Account for input bar

    // Create particles in a sphere (more for denser look)
    const numParticles = 1200;
    const radius = 100;

    for (let i = 0; i < numParticles; i++) {
        const theta = Math.random() * Math.PI * 2;
        const phi = Math.acos(2 * Math.random() - 1);

        const x = radius * Math.sin(phi) * Math.cos(theta);
        const y = radius * Math.sin(phi) * Math.sin(theta);
        const z = radius * Math.cos(phi);

        particles.push(new Particle(x, y, z));
    }

    animateOrb();
}

function animateOrb() {
    const centerX = orbCanvas.width / 2;
    const centerY = orbCanvas.height / 2;
    const scale = Math.min(orbCanvas.width, orbCanvas.height) / 400;

    // Clear canvas
    orbCtx.fillStyle = 'rgba(0, 0, 0, 0.05)';
    orbCtx.fillRect(0, 0, orbCanvas.width, orbCanvas.height);

    // Update and draw particles
    orbRotation += 0.002;

    // Sort particles by z-index for proper depth
    particles.sort((a, b) => b.z - a.z);

    particles.forEach(particle => {
        particle.update();

        // Rotate particle
        const cosR = Math.cos(orbRotation);
        const sinR = Math.sin(orbRotation);
        const rotatedX = particle.x * cosR - particle.z * sinR;
        const rotatedZ = particle.x * sinR + particle.z * cosR;

        particle.x = rotatedX;
        particle.z = rotatedZ;

        const projected = particle.project(centerX, centerY, scale);

        // Draw particle with golden glow
        const gradient = orbCtx.createRadialGradient(
            projected.x, projected.y, 0,
            projected.x, projected.y, projected.radius * 3
        );
        gradient.addColorStop(0, `rgba(255, 200, 0, ${projected.alpha})`);
        gradient.addColorStop(0.5, `rgba(255, 160, 0, ${projected.alpha * 0.5})`);
        gradient.addColorStop(1, 'rgba(255, 140, 0, 0)');

        orbCtx.fillStyle = gradient;
        orbCtx.beginPath();
        orbCtx.arc(projected.x, projected.y, projected.radius * 3, 0, Math.PI * 2);
        orbCtx.fill();
    });

    // Draw connections between nearby particles (VERY intense like reference)
    const connectionOpacity = isAISpeaking ? 0.6 : 0.2;
    const connectionWidth = isAISpeaking ? 2 : 0.8;
    orbCtx.strokeStyle = `rgba(255, 184, 0, ${connectionOpacity})`;
    orbCtx.lineWidth = connectionWidth;

    for (let i = 0; i < particles.length; i += 3) {
        for (let j = i + 1; j < particles.length; j += 3) {
            const dx = particles[i].x - particles[j].x;
            const dy = particles[i].y - particles[j].y;
            const dz = particles[i].z - particles[j].z;
            const distance = Math.sqrt(dx * dx + dy * dy + dz * dz);

            if (distance < 60) {
                const p1 = particles[i].project(centerX, centerY, scale);
                const p2 = particles[j].project(centerX, centerY, scale);

                orbCtx.beginPath();
                orbCtx.moveTo(p1.x, p1.y);
                orbCtx.lineTo(p2.x, p2.y);
                orbCtx.stroke();
            }
        }
    }

    // Decay vibration intensity
    if (vibrationIntensity > 0) {
        vibrationIntensity *= 0.95;
        if (vibrationIntensity < 0.1) vibrationIntensity = 0;
    }

    animationId = requestAnimationFrame(animateOrb);
}

// ============================================================================
// WEBSOCKET CONNECTION
// ============================================================================

function connectWebSocket() {
    const wsUrl = `ws://${window.location.host}/ws`;
    ws = new WebSocket(wsUrl);

    ws.onopen = () => {
        isConnected = true;
        updateStatus('ONLINE', true);
        showNotification('JARVIS online', 'success');
    };

    ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleWebSocketMessage(data);
    };

    ws.onerror = (error) => {
        updateStatus('ERROR', false);
    };

    ws.onclose = () => {
        isConnected = false;
        updateStatus('OFFLINE', false);
        setTimeout(connectWebSocket, 3000);
    };
}

function handleWebSocketMessage(data) {
    const { type, message, chunk } = data;

    switch (type) {
        case 'system':
            addMessage(message, 'system');
            saveChatHistory();
            break;

        case 'chat_start':
            addMessage(message, 'user');
            const msgDiv = createMessageElement('', 'assistant');
            elements.chatMessages.appendChild(msgDiv);
            scrollToBottom();

            // Trigger INTENSE particle vibration when AI starts speaking
            isAISpeaking = true;
            vibrationIntensity = 15; // Much higher intensity
            break;

        case 'chat_chunk':
            const lastMsg = elements.chatMessages.querySelector('.assistant-message:last-child .message-content');
            if (lastMsg) {
                lastMsg.textContent += chunk;
                scrollToBottom();

                // Maintain STRONG vibration during streaming
                if (vibrationIntensity < 10) {
                    vibrationIntensity = 10;
                }
            }
            break;

        case 'chat_complete':
            // Stop vibration when AI finishes
            isAISpeaking = false;
            saveChatHistory();
            break;
    }
}

function sendMessage(message) {
    if (!isConnected || !message.trim()) return;

    ws.send(JSON.stringify({
        type: 'chat',
        message: message.trim()
    }));

    elements.chatInput.value = '';
}

// ============================================================================
// UI UPDATES
// ============================================================================

function updateStatus(status, online) {
    elements.statusText.textContent = status;
    if (online) {
        elements.statusDot.style.background = '#FFB800';
        elements.statusDot.style.boxShadow = '0 0 10px #FFB800';
    } else {
        elements.statusDot.style.background = '#FF0055';
        elements.statusDot.style.boxShadow = '0 0 10px #FF0055';
    }
}

function createMessageElement(text, type) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${type}-message`;

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    if (type === 'assistant') {
        const strong = document.createElement('strong');
        strong.textContent = 'JARVIS: ';
        contentDiv.appendChild(strong);
        contentDiv.appendChild(document.createTextNode(text));
    } else if (type === 'user') {
        contentDiv.textContent = text;
    } else {
        contentDiv.textContent = text;
    }

    msgDiv.appendChild(contentDiv);
    return msgDiv;
}

function addMessage(text, type) {
    const msgDiv = createMessageElement(text, type);
    elements.chatMessages.appendChild(msgDiv);
    scrollToBottom();
    saveChatHistory();
}

function scrollToBottom() {
    elements.chatOverlay.scrollTop = elements.chatOverlay.scrollHeight;
}

function addImageToChat(imageBase64) {
    const imgDiv = document.createElement('div');
    imgDiv.className = 'message assistant-message';

    const img = document.createElement('img');
    img.src = imageBase64;
    img.style.maxWidth = '300px';
    img.style.borderRadius = '8px';
    img.style.marginTop = '10px';
    img.style.border = '1px solid rgba(255, 184, 0, 0.3)';

    imgDiv.appendChild(img);
    elements.chatMessages.appendChild(imgDiv);
    scrollToBottom();
}

// ============================================================================
// CHAT HISTORY PERSISTENCE
// ============================================================================

function saveChatHistory() {
    const messages = [];
    const messageElements = elements.chatMessages.querySelectorAll('.message');

    messageElements.forEach(msgEl => {
        const content = msgEl.querySelector('.message-content').textContent;
        let type = 'system';
        if (msgEl.classList.contains('user-message')) type = 'user';
        else if (msgEl.classList.contains('assistant-message')) type = 'assistant';

        messages.push({ type, content });
    });

    localStorage.setItem('jarvis_chat_history', JSON.stringify(messages));
}

function loadChatHistory() {
    const saved = localStorage.getItem('jarvis_chat_history');
    if (!saved) return;

    try {
        const messages = JSON.parse(saved);
        messages.forEach(msg => {
            addMessageWithoutSave(msg.content, msg.type);
        });
    } catch (e) {
        console.error('Error loading chat history:', e);
    }
}

function addMessageWithoutSave(text, type) {
    const msgDiv = createMessageElement(text, type);
    elements.chatMessages.appendChild(msgDiv);
    scrollToBottom();
}

function clearChatHistory() {
    elements.chatMessages.innerHTML = '';
    localStorage.removeItem('jarvis_chat_history');
    showNotification('Chat history cleared');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;

    elements.notificationContainer.appendChild(notification);

    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// ============================================================================
// EVENT HANDLERS
// ============================================================================

elements.sendBtn.addEventListener('click', () => {
    sendMessage(elements.chatInput.value);
});

elements.chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage(elements.chatInput.value);
    }
});

elements.voiceBtn.addEventListener('click', () => {
    if (!isListening) {
        startVoiceRecognition();
    } else {
        stopVoiceRecognition();
    }
});

// File upload handling
elements.uploadBtn.addEventListener('click', () => {
    elements.fileInput.click();
});

elements.fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const message = elements.chatInput.value.trim() || 'extract text from this image';

    try {
        // Show uploading message
        addMessage(`Uploading ${file.name}...`, 'system');

        // Create form data
        const formData = new FormData();
        formData.append('file', file);
        formData.append('message', message);

        // Upload to server
        const response = await fetch('/api/upload-image', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();

        if (result.success) {
            addMessage(message, 'user');
            addMessage(result.response, 'assistant');

            // Display image if it's in the response
            if (result.image_base64) {
                addImageToChat(result.image_base64);
            }
        } else {
            addMessage(`Error: ${result.error}`, 'system');
        }

    } catch (error) {
        addMessage(`Upload failed: ${error.message}`, 'system');
    }

    // Clear file input
    elements.fileInput.value = '';
    elements.chatInput.value = '';
});

// ============================================================================
// VOICE RECOGNITION
// ============================================================================

let recognition = null;

function initVoiceRecognition() {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;

            ws.send(JSON.stringify({
                type: 'voice',
                text: transcript
            }));

            stopVoiceRecognition();
        };

        recognition.onerror = () => {
            stopVoiceRecognition();
        };

        recognition.onend = () => {
            stopVoiceRecognition();
        };
    }
}

function startVoiceRecognition() {
    if (!recognition) {
        initVoiceRecognition();
    }

    if (recognition) {
        isListening = true;
        elements.voiceBtn.classList.add('active');
        recognition.start();
        showNotification('Listening...');
    }
}

function stopVoiceRecognition() {
    isListening = false;
    elements.voiceBtn.classList.remove('active');
    if (recognition) {
        recognition.stop();
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

function init() {
    console.log('Initializing JARVIS AI Orb Interface...');

    // Initialize 3D orb
    initOrb();

    // Load chat history
    loadChatHistory();

    // Connect WebSocket
    connectWebSocket();

    // Initialize voice recognition
    initVoiceRecognition();

    // Focus input
    elements.chatInput.focus();
}

// Start when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// Handle window resize
window.addEventListener('resize', () => {
    orbCanvas.width = window.innerWidth;
    orbCanvas.height = window.innerHeight - 100;
});
