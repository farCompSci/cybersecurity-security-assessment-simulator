import streamlit as st
import requests
import uuid
import os

# FastAPI endpoint
url = os.environ.get("BACKEND_URL", "http://localhost:8000")
FASTAPI_CHAT_URL = f"{url}/api/chat/assessment-assistant"
FASTAPI_STATUS_URL = f"{url}/docs"

MSG_KEY = "assessment_messages"
ENDED_KEY = "assessment_chat_ended"
THREAD_KEY = "assessment_thread_id"
API_KEY = "assessment_api_status"

def init_assessment_session_state():
    """Initialize all required session state variables for the assessment assistant"""
    if MSG_KEY not in st.session_state:
        st.session_state[MSG_KEY] = []

    if ENDED_KEY not in st.session_state:
        st.session_state[ENDED_KEY] = False

    if THREAD_KEY not in st.session_state:
        st.session_state[THREAD_KEY] = str(uuid.uuid4())

    if API_KEY not in st.session_state:
        st.session_state[API_KEY] = "unknown"

def check_api_status() -> str:
    """Ping the FastAPI server and return online/offline"""
    try:
        response = requests.get(FASTAPI_STATUS_URL, timeout=5)
        return "online" if response.status_code == 200 else "offline"
    except requests.RequestException:
        return "offline"

def call_fastapi_chat(messages, thread_id):
    """Call the FastAPI security assistant chat endpoint"""
    try:
        payload = {
            "messages": messages,
            "thread_id": thread_id
        }

        response = requests.post(
            FASTAPI_CHAT_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=180
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None

    except requests.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def render_header():
    """Show header and API status"""
    st.title("📚 Security Assessment Teaching Assistant")

    if st.session_state[API_KEY] == "unknown":
        st.session_state[API_KEY] = check_api_status()

    if st.session_state[API_KEY] == "online":
        st.success("✅ TA is able to help!")
    else:
        st.error("❌ FastAPI server is offline. Please start your FastAPI server.")
        st.stop()

    if not st.session_state[ENDED_KEY]:
        st.markdown("🎓 *Ask me about the Security Assessment Template sections and guidelines*")
        st.markdown("💡 Try asking: 'List all sections' or 'Tell me about section 3'")
        st.markdown("---")
    else:
        st.markdown("### 🔒 Chat session has ended.")

def render_chat_history():
    """Display previous messages from chat"""
    for message in st.session_state[MSG_KEY]:
        if message["role"] == "system":
            continue
        role_display = "user" if message["role"] == "human" else message["role"]
        with st.chat_message(role_display):
            st.markdown(message["content"])

def handle_chat_input():
    """Handle new user input"""
    prompt = st.chat_input(
        "Ask about security assessment sections, guidelines, or best practices. Type 'exit' to end conversation.")
    if not prompt:
        return

    if prompt.strip().lower() == "exit":
        with st.chat_message("assistant"):
            st.markdown("✅ Chat ended. Good luck with your security assessment!")
        st.session_state[ENDED_KEY] = True
        st.rerun()
        return

    st.session_state[MSG_KEY].append({"role": "human", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching knowledge base..."):
            result = call_fastapi_chat(st.session_state[MSG_KEY], st.session_state[THREAD_KEY])
            if result and "conversation" in result:
                conversation = result["conversation"]
                ai_response = next((msg["content"] for msg in reversed(conversation) if msg["role"] == "ai"), None)
                if ai_response:
                    st.markdown(ai_response)
                    st.session_state[MSG_KEY].append({"role": "ai", "content": ai_response})
                else:
                    st.error("No AI response found.")
            else:
                st.error("Failed to get response from the teaching assistant.")

def render_chat_controls():
    """Display restart or navigation options if chat is ended"""
    if st.session_state[ENDED_KEY]:
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("🔄 Start New Chat"):
                st.session_state[ENDED_KEY] = False
                st.session_state[MSG_KEY] = []
                st.session_state[THREAD_KEY] = str(uuid.uuid4())
                st.rerun()

        with col2:
            if st.button("📋 Back to Assessment"):
                st.switch_page("pages/Assignment_2.py")

        with col3:
            if st.button("🤝 Go to Submission Page"):
                st.switch_page("pages/Assignment_2.py")

def main():
    init_assessment_session_state()
    render_header()
    render_chat_history()

    if st.session_state[ENDED_KEY]:
        render_chat_controls()
    else:
        handle_chat_input()

if __name__ == "__main__":
    main()