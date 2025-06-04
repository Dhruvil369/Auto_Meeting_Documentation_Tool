# transcription.py

import sounddevice as sd
import scipy.io.wavfile as wav
import numpy as np
from faster_whisper import WhisperModel
import time
import os
import threading

model = WhisperModel("base", device="cpu")  # Load your whisper model
recording_event = threading.Event()
transcript = []

# File path for saving temporary audio
AUDIO_PATH = "output/temp.wav"


def start_transcription():
    global transcript
    transcript = []
    fs = 16000  # Sampling rate
    duration = 100  # 10 seconds per chunk
    print("Recording started...")
    recording_event.set()
    while recording_event.is_set():
        print("🎤 Listening...")
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        # Convert audio to 1D array for wav saving
        audio_1d = np.squeeze(audio)
        
        # Save audio chunk
        wav.write(AUDIO_PATH, fs, audio_1d)

        # Transcribe this chunk
        segments, _ = model.transcribe(AUDIO_PATH, beam_size=5)
        for segment in segments:
            print("Transcribed segment:", segment.text)
            transcript.append(segment.text)
    print("Recording stopped.")

def stop_transcription():
    recording_event.clear()

def get_transcript():
    print("Returning transcript:", transcript)
    return ' '.join(transcript)
