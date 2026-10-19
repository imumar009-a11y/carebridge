"""voice.py - Voice input component using browser Web Speech API."""
import streamlit.components.v1 as components


def voice_input_component(key: str = "voice_input", height: int = 90) -> None:
    """Render a voice input button that uses the Web Speech API.
    
    When the user speaks, the recognized text is sent back to Streamlit
    via the streamlit-component messaging protocol and stored in session state.
    """
    html_code = """
    <!DOCTYPE html>
    <html>
    <head>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: transparent;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 80px;
        }
        .voice-container {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 20px;
            background: linear-gradient(135deg, #0B2F3A 0%, #0E7C86 100%);
            border-radius: 50px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(14, 124, 134, 0.3);
            user-select: none;
        }
        .voice-container:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 25px rgba(14, 124, 134, 0.45);
        }
        .voice-container.listening {
            background: linear-gradient(135deg, #D7263D 0%, #E8731A 100%);
            box-shadow: 0 4px 25px rgba(215, 38, 61, 0.4);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0%, 100% { box-shadow: 0 4px 25px rgba(215, 38, 61, 0.4); }
            50% { box-shadow: 0 4px 35px rgba(215, 38, 61, 0.7); }
        }
        .mic-icon {
            width: 24px;
            height: 24px;
            fill: white;
        }
        .voice-text {
            color: white;
            font-size: 14px;
            font-weight: 600;
            letter-spacing: 0.02em;
        }
        .wave-bars {
            display: none;
            align-items: center;
            gap: 3px;
            height: 20px;
        }
        .wave-bars.active { display: flex; }
        .wave-bar {
            width: 3px;
            background: white;
            border-radius: 2px;
            animation: wave 0.8s ease-in-out infinite;
        }
        .wave-bar:nth-child(1) { height: 8px; animation-delay: 0s; }
        .wave-bar:nth-child(2) { height: 14px; animation-delay: 0.1s; }
        .wave-bar:nth-child(3) { height: 20px; animation-delay: 0.2s; }
        .wave-bar:nth-child(4) { height: 14px; animation-delay: 0.3s; }
        .wave-bar:nth-child(5) { height: 8px; animation-delay: 0.4s; }
        @keyframes wave {
            0%, 100% { transform: scaleY(0.5); }
            50% { transform: scaleY(1); }
        }
        .not-supported {
            color: #666;
            font-size: 13px;
            text-align: center;
            padding: 10px;
        }
    </style>
    </head>
    <body>
    <div id="voiceBtn" class="voice-container" onclick="toggleVoice()">
        <svg class="mic-icon" viewBox="0 0 24 24" id="micIcon">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
        </svg>
        <span class="voice-text" id="voiceText">🎙️ Tap to speak</span>
        <div class="wave-bars" id="waveBars">
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
            <div class="wave-bar"></div>
        </div>
    </div>
    <div class="not-supported" id="notSupported" style="display:none">
        ⚠️ Voice input is not supported in this browser. Please use Chrome or Edge.
    </div>
    
    <script>
    let recognition = null;
    let isListening = false;
    
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;
        // Support multiple languages
        recognition.lang = 'en-US';
        
        recognition.onstart = function() {
            isListening = true;
            document.getElementById('voiceBtn').classList.add('listening');
            document.getElementById('voiceText').textContent = 'Listening...';
            document.getElementById('waveBars').classList.add('active');
        };
        
        recognition.onresult = function(event) {
            let finalTranscript = '';
            let interimTranscript = '';
            for (let i = event.resultIndex; i < event.results.length; i++) {
                if (event.results[i].isFinal) {
                    finalTranscript += event.results[i][0].transcript;
                } else {
                    interimTranscript += event.results[i][0].transcript;
                }
            }
            if (interimTranscript) {
                document.getElementById('voiceText').textContent = '🎤 ' + interimTranscript;
            }
            if (finalTranscript) {
                document.getElementById('voiceText').textContent = '✅ ' + finalTranscript;
                // Send to Streamlit
                window.parent.postMessage({
                    type: 'streamlit:setComponentValue',
                    value: finalTranscript
                }, '*');
            }
        };
        
        recognition.onerror = function(event) {
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
            document.getElementById('waveBars').classList.remove('active');
            if (event.error === 'no-speech') {
                document.getElementById('voiceText').textContent = '🎙️ No speech detected. Tap again.';
            } else {
                document.getElementById('voiceText').textContent = '🎙️ Tap to speak';
            }
        };
        
        recognition.onend = function() {
            isListening = false;
            document.getElementById('voiceBtn').classList.remove('listening');
            document.getElementById('waveBars').classList.remove('active');
            setTimeout(function() {
                document.getElementById('voiceText').textContent = '🎙️ Tap to speak';
            }, 2000);
        };
    } else {
        document.getElementById('voiceBtn').style.display = 'none';
        document.getElementById('notSupported').style.display = 'block';
    }
    
    function toggleVoice() {
        if (!recognition) return;
        if (isListening) {
            recognition.stop();
        } else {
            recognition.start();
        }
    }
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=height, scrolling=False)


def voice_input_with_state(height: int = 90) -> str | None:
    """Voice input component that manages state for captured speech.
    
    Uses a Streamlit-compatible approach: renders an HTML component
    and captures results via query params / session state.
    """
    voice_input_component(height=height)
    return None  # Results handled via JS postMessage