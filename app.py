# app.py
from flask import Flask, render_template, request, jsonify
import threading
import os
from transcription import start_transcription, stop_transcription, get_transcript
from summarizer import generate_summary

app = Flask(__name__)

recording_thread = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global recording_thread
    if recording_thread and recording_thread.is_alive():
        return jsonify({"status": "Recording already in progress."})
    recording_thread = threading.Thread(target=start_transcription)
    recording_thread.start()
    return jsonify({"status": "recording started"})

@app.route('/stop', methods=['POST'])
def stop():
    global recording_thread
    stop_transcription()
    if recording_thread:
        recording_thread.join()  # Wait for recording to finish
    transcript = get_transcript()
    print("Raw transcript object:", transcript)
    print("Type of transcript:", type(transcript))
    # Ensure transcript is string
    if not isinstance(transcript, str):
        try:
            transcript = str(transcript)
            print("Transcript converted to string.")
        except Exception as e:
            print("Error converting transcript to string:", e)
            return jsonify({"error": "Transcript could not be processed."})
    print("Transcript (string):", transcript)
    if not transcript.strip():
        return jsonify({"error": "No transcript recorded. Please speak during the session."})
    summary = generate_summary(transcript)
    print("Generated summary:", summary)
    with open('output/meeting_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    return jsonify({"report": summary})

if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    app.run(debug=True,port=5500)



