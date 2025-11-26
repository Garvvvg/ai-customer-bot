from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
# import google.generativeai as genai
from google import genai

app = Flask(__name__)
app.secret_key = 'your-secret-key'
CORS(app)

# Configure your Gemini API key
# Better: set as environment variable


@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message")
        if not user_msg:
            return jsonify({"response": "Please send a message.", "escalate": False})

        # Get existing chat history or start new
        chat_history = session.get("chat_history", [])
        # Add user message
        chat_history.append({"role": "user", "content": user_msg})

        # Prepare contents for Gemini
        contents = []
        for msg in chat_history:
            contents.append({
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            })

        # Call Gemini
        client = genai.Client()
        resp = client.models.generate_content(
            model="gemini-1.5-pro-latest",
            contents=contents,
            
        )

        # Extract model reply
        bot_msg = resp.text.strip()  # or resp.generations[0].text depending on SDK version

        # Append bot reply to history
        chat_history.append({"role": "assistant", "content": bot_msg})
        session["chat_history"] = chat_history

        # Decide escalate (example logic)
        escalate = False
        if len(bot_msg) < 10:
            escalate = True

        return jsonify({
            "response": bot_msg,
            "escalate": escalate,
            "chat_history": chat_history
        })

    except Exception as e:
        print("Backend Error:", e)
        return jsonify({"response": "Internal server error.", "escalate": True})

@app.route('/end_session', methods=['POST'])
def end_session():
    session.pop("chat_history", None)
    return jsonify({"status":"session ended"})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
