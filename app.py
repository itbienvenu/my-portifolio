# app.py
from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=" + GEMINI_API_KEY

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    payload = {
        "contents": [
            {"parts": [{"text": user_message}]}
        ]
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    if response.ok:
        data = response.json()
        try:
            reply = data['candidates'][0]['content']['parts'][0]['text']
        except Exception:
            reply = "Sorry, I couldn't understand the response."
        return jsonify({"reply": reply})
    else:
        return jsonify({"reply": "Error contacting Gemini API."}), 500

if __name__ == '__main__':
    app.run(debug=True)
