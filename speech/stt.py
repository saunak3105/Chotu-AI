import os
import json
from utils.constants import VOSK_MODEL_PATH

try:
    from vosk import Model, KaldiRecognizer
    import pyaudio
    VOSK_AVAILABLE = True
except ImportError:
    VOSK_AVAILABLE = False
    print("Vosk or PyAudio not found. Falling back to text input.")

def listen(item_list=None):
    if not VOSK_AVAILABLE or not os.path.exists(VOSK_MODEL_PATH):
        return None

    try:
        model = Model(VOSK_MODEL_PATH)
        
        # Build Grammar to 'train' the recognizer on our specific words
        if item_list:
            # Include common commands and numbers in the grammar
            commands = ["add", "remove", "bill", "stock", "sales", "kharcha", "becha", "daalo"]
            numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "ek", "do", "teen", "char"]
            grammar = json.dumps(item_list + commands + numbers + ["[unk]"])
            rec = KaldiRecognizer(model, 16000, grammar)
        else:
            rec = KaldiRecognizer(model, 16000)

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
        stream.start_stream()

        print("Listening...")
        while True:
            data = stream.read(4000)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
    except Exception as e:
        print(f"STT Error: {e}")
        return input("User (Fallback to Text): ")
