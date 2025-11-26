# AI Customer Support Bot

A Python-based customer support chatbot using Streamlit (frontend), Flask (backend), and Gemini/OpenAI API integration.  
Supports contextual memory, escalation logic, and FAQ-style interactions.

## Features
- Contextual chatbot powered by LLM (Gemini/OpenAI).
- Session-based memory to retain previous conversation.
- Escalation simulation when query is not answered.
- Streamlit chat interface.
- RESTful backend API.

## Requirements
- Python 3.8+
- See `requirements.txt` for dependencies

## Setup

1. **Clone the repository**
* git clone https://github.com/Garvvvg/ai-customer-bot
* cd your-repo-name

2. **Install dependencies**
* pip install -r requirements.txt

3. **Create a `.env` file (in project root)**
* GEMINI_API_KEY=your-gemini-key
* OPENAI_API_KEY=your-openai-key
* SECRET_KEY=your-flask-secret-key


4. **Run the backend server**
* python backend/app.py


5. **Run the Streamlit frontend**
* ## Usage

- Access the chat UI on [http://localhost:8501](http://localhost:8501)
- Ask customer queries and see bot responses with escalation handlingstreamlit run frontend/app.py
