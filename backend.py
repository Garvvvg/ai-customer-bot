from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-default-secret-key')
CORS(app)

MAX_HISTORY_LENGTH = 10  # Limit chat history size to last 10 messages


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

        # Keep chat history manageable in size
        if len(chat_history) > MAX_HISTORY_LENGTH:
            chat_history = chat_history[-MAX_HISTORY_LENGTH:]

        # Prepare contents for Gemini with system prompt for customer care persona
        contents = [{
            "role": "model",
            "parts": [{
                "text": (
                    "You are a helpful customer care assistant for Unthinkable Solution, a tech solutions company. "
                    "Answer politely and assist users with their queries about our products, services, and support."
                )
            }]
        }]

        for msg in chat_history:
            contents.append({
                "role": msg["role"],
                "parts": [{"text": msg["content"]}]
            })

        # Call Gemini API
        client = genai.Client()
        resp = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
        )

        # Extract model reply
        bot_msg = resp.text.strip()  # Use resp.generations[0].text if needed depending on SDK version

        # Append bot reply to history
        chat_history.append({"role": "assistant", "content": bot_msg})
        session["chat_history"] = chat_history

        # Decide escalate (example: escalate if short response maybe insufficient)
        escalate = len(bot_msg) < 10

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
    return jsonify({"status": "session ended"})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
