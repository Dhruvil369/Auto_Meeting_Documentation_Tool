
# summarizer.py
import os
import google.generativeai as genai

def generate_summary(text):
    genai.configure(api_key="Enter_Your_Api_Key")
    model = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
    prompt = f"""
You are an AI meeting assistant. Given the transcript below, generate a professional meeting summary with the following sections (only include them if content exists):

## 👥 Participants:
## 🗣️ Key Conversation Summary:
## 📋 Action Items:
## 🔁 Next Meeting Points:
## 💡 Decisions Taken:
## ❗ Issues/Risks:

Transcript:
{text}
"""
    response = model.generate_content(prompt)
    return response.text

