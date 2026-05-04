import os

try:
    import pyttsx3
    engine = pyttsx3.init()
    # Set properties
    engine.setProperty('rate', 150)    # Speed percent (can go over 100)
    engine.setProperty('volume', 0.9)  # Volume 0-1
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("TTS (pyttsx3) not found. Falling back to console output.")

def speak(text):
    print(f"Assistant: {text}")
    if TTS_AVAILABLE:
        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print(f"TTS Error: {e}")
