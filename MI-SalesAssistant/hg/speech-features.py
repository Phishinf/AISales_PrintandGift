import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode
import streamlit_js_eval
import base64
from io import BytesIO
import asyncio
from gtts import gTTS

# Add these imports to your existing imports

def add_speech_recognition():
    """
    Add a speech recognition button that allows users to speak their query
    """
    # Create a container for the speech recognition button
    speech_container = st.container()
    
    with speech_container:
        col1, col2 = st.columns([1, 5])
        
        with col1:
            # Add a microphone button
            mic_clicked = st.button("🎤", key="mic_button", help="Click to start speaking")
        
        with col2:
            # Status indicator for speech recognition
            if "speech_recognition_status" not in st.session_state:
                st.session_state.speech_recognition_status = "Click the microphone to speak"
            
            status_placeholder = st.empty()
            status_placeholder.info(st.session_state.speech_recognition_status)
        
        if mic_clicked:
            # Update status
            st.session_state.speech_recognition_status = "Listening... (speak now)"
            status_placeholder.warning(st.session_state.speech_recognition_status)
            
            try:
                # Use JavaScript to access the browser's speech recognition API
                result = streamlit_js_eval.get_geolocation()
                transcript = streamlit_js_eval.create_proxy("speechRecognition")()
                
                if transcript:
                    # Update the chat input with the transcribed text
                    st.session_state.speech_text = transcript
                    st.session_state.speech_recognition_status = "Success! Your speech was recognized."
                    status_placeholder.success(st.session_state.speech_recognition_status)
                    
                    # The main chat input component will reference this session state value
                    return True
                else:
                    st.session_state.speech_recognition_status = "No speech detected. Please try again."
                    status_placeholder.error(st.session_state.speech_recognition_status)
            except Exception as e:
                st.session_state.speech_recognition_status = f"Error: {str(e)}"
                status_placeholder.error(st.session_state.speech_recognition_status)
    
    return False

def text_to_speech(text, language='en'):
    """
    Convert text to speech and return the audio file as base64
    """
    try:
        # Use gTTS to convert text to speech
        tts = gTTS(text=text, lang=language, slow=False)
        
        # Save the audio to a BytesIO object
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        # Encode the audio file as base64
        audio_base64 = base64.b64encode(audio_buffer.read()).decode()
        
        # Create an HTML audio element with the base64 audio
        audio_html = f"""
        <audio id="audio-player" controls autoplay>
            <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        
        return audio_html
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None

# JavaScript for speech recognition - add to your custom CSS section
def add_speech_recognition_js():
    """
    Add JavaScript for speech recognition
    """
    speech_js = """
    <script>
    function speechRecognition() {
        return new Promise((resolve, reject) => {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                reject("Speech recognition not supported in this browser.");
                return;
            }
            
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            
            recognition.lang = 'en-US';
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            recognition.continuous = false;
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                resolve(transcript);
            };
            
            recognition.onerror = (event) => {
                reject("Error in speech recognition: " + event.error);
            };
            
            recognition.onend = () => {
                resolve(null);  // No speech detected
            };
            
            recognition.start();
        });
    }
    
    // Function to play text-to-speech on a button click
    function playTextToSpeech(elementId) {
        const audioElement = document.getElementById(elementId);
        if (audioElement) {
            audioElement.play();
        }
    }
    </script>
    """
    
    st.markdown(speech_js, unsafe_allow_html=True)

# Example of how to use these functions in your main function:

def get_chat_input_with_speech():
    """
    Get chat input with speech recognition option
    """
    # Add speech recognition JavaScript
    add_speech_recognition_js()
    
    # Add the speech recognition button and status
    speech_triggered = add_speech_recognition()
    
    # Initialize the speech text session state if not present
    if "speech_text" not in st.session_state:
        st.session_state.speech_text = ""
    
    # Get the speech text if available or use an empty string
    initial_text = st.session_state.speech_text if speech_triggered else ""
    
    # Use the standard chat input with the speech text as the initial value
    prompt = st.chat_input(
        "What theology topic would you like to explore?", 
        disabled=st.session_state.get("api_key_missing", False),
        key="chat_input",
        value=initial_text
    )
    
    # Reset the speech text after using it
    if speech_triggered:
        st.session_state.speech_text = ""
    
    return prompt

def add_tts_button_to_message(message_content, message_idx):
    """
    Add a text-to-speech button to a message
    """
    # Create a unique ID for the audio element
    audio_id = f"audio-{message_idx}"
    
    # Create a button with a JavaScript onclick handler to play the audio
    tts_button_html = f"""
    <button 
        onclick="playTextToSpeech('{audio_id}')" 
        style="background-color: #4B5563; color: white; border: none; padding: 5px 10px; 
               border-radius: 5px; cursor: pointer; margin-top: 5px;"
    >
        🔊 Listen
    </button>
    """
    
    # Generate the audio element but set it to hidden initially
    audio_html = text_to_speech(message_content)
    if audio_html:
        # Modify the audio element ID to match the one referenced in the button
        audio_html = audio_html.replace('id="audio-player"', f'id="{audio_id}" style="display:none;"')
        
        # Combine the button and audio elements
        return f"{tts_button_html}\n{audio_html}"
    
    return None
