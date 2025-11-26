import streamlit as st
import requests

st.set_page_config(page_title="AI Customer Support Bot")
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("AI Customer Support Bot")

def end_chat():
    requests.post("http://localhost:5000/end_session")
    st.session_state.chat_history = []

with st.form(key="chat_form"):
    user_input = st.text_input("Your message:", "")
    submit_button = st.form_submit_button("Send")

if submit_button and user_input:
    res = requests.post(
        "http://localhost:5000/chat",
        json={"message": user_input}
    )

    if res.status_code == 200:
        response = res.json()

        bot_msg = response.get("response", "No response from server.")
        st.write("**🤖 Support Bot:**", bot_msg)

        if "chat_history" in response:
            st.session_state.chat_history = response["chat_history"]

        if response.get("escalate"):
            st.warning("Your query has been escalated.")

    else:
        st.error("Backend ERROR! Please start Flask backend first.")

st.write("### Chat History 🗂️")
if st.session_state.chat_history:
    for msg in st.session_state.chat_history:
        role = "🧑 You" if msg["role"] == "user" else "🤖 Bot"
        st.write(f"**{role}:** {msg['content']}")

if st.button("End Chat"):
    end_chat()
    st.info("Session Ended!")
