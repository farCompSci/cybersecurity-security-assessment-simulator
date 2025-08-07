import streamlit as st
import requests
import uuid

# FastAPI endpoint
FASTAPI_CHAT_URL = "http://localhost:8000/api/chat/owner/chat"
FASTAPI_STATUS_URL = "http://localhost:8000/docs"


def init_session_state():
    """Initialize all required session state variables"""
    if "graph_state" not in st.session_state:
        st.session_state.graph_state = {}

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chat_ended" not in st.session_state:
        st.session_state.chat_ended = False

    if "thread_id" not in st.session_state:
        st.session_state.thread_id = str(uuid.uuid4())

    if "api_status" not in st.session_state:
        st.session_state.api_status = "unknown"


def check_api_status() -> str:
    """Ping the FastAPI server and return online/offline"""
    try:
        response = requests.get(FASTAPI_STATUS_URL, timeout=5)
        return "online" if response.status_code == 200 else "offline"
    except requests.RequestException:
        return "offline"


def call_fastapi_chat(messages, thread_id):
    """Call the FastAPI chat endpoint"""
    try:
        payload = {
            "business": st.session_state.graph_state,
            "messages": messages,
            "thread_id": thread_id
        }

        response = requests.post(
            FASTAPI_CHAT_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
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
    st.title("🏠 Business Owner Chatbot")

    if st.session_state.api_status == "unknown":
        st.session_state.api_status = check_api_status()

    if st.session_state.api_status == "online":
        st.success("✅ Connection Established")
    else:
        st.error("❌ FastAPI server is offline. Please start your FastAPI server.")
        st.stop()

    if not st.session_state.chat_ended:
        business_name = st.session_state.graph_state.get("business_name", "Unknown Business")
        st.markdown(f"💬 *You are currently conversing with the Business Owner of **{business_name}***")
        st.markdown("---")
    else:
        st.markdown("### 🔒 Chat session has ended.")


def render_chat_history():
    """Display previous messages from chat"""
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        role_display = "user" if message["role"] == "human" else message["role"]
        with st.chat_message(role_display):
            st.markdown(message["content"])


def handle_chat_input():
    """Handle new user input"""
    prompt = st.chat_input("Ask a question about the business's security practices. Type 'exit' to end conversation.")
    if not prompt:
        return

    if prompt.strip().lower() == "exit":
        with st.chat_message("assistant"):
            st.markdown("✅ Chat ended. Thank you for your questions!")
        st.session_state.chat_ended = True
        st.rerun()
        return

    st.session_state.messages.append({"role": "human", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            result = call_fastapi_chat(st.session_state.messages, st.session_state.thread_id)
            if result and "conversation" in result:
                conversation = result["conversation"]
                ai_response = next((msg["content"] for msg in reversed(conversation) if msg["role"] == "ai"), None)
                if ai_response:
                    st.markdown(ai_response)
                    st.session_state.messages.append({"role": "ai", "content": ai_response})
                else:
                    st.error("No AI response found.")
            else:
                st.error("Failed to get response from the chatbot.")


def render_chat_controls():
    """Display restart or next-assignment options if chat is ended"""
    if st.session_state.chat_ended:
        if st.button("🔄 Start New Chat"):
            st.session_state.chat_ended = False
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()

        if st.button("🤝 Move to next assignment"):
            st.switch_page("pages/Assignment_2.py")


def main():
    init_session_state()
    render_header()
    render_chat_history()

    if st.session_state.chat_ended:
        render_chat_controls()
    else:
        handle_chat_input()


if __name__ == "__main__":
    main()
