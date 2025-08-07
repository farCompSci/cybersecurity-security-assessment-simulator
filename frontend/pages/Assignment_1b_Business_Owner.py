import streamlit as st
import requests
import uuid
import json

# FastAPI endpoint configuration
FASTAPI_URL = "http://localhost:8000/api/chat/owner/chat"

business_state = st.session_state.get("graph_state", {})
st.session_state.thread = uuid.uuid4()


def call_fastapi_chat(messages, thread_id=st.session_state.get("thread", uuid.uuid4())):
    """Call the FastAPI chat endpoint"""
    try:
        payload = {
            "business": business_state,
            "messages": messages,
            "thread_id": thread_id
        }

        response = requests.post(
            FASTAPI_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30  # 30 second timeout
        )

        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        st.error(f"Connection error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None


# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat_ended = False
    st.session_state.thread_id = None

if "api_status" not in st.session_state:
    st.session_state.api_status = "unknown"

st.title("🏠 Business Owner Chatbot")

# API Status indicator
def check_api_status():
    try:
        response = requests.get("http://localhost:8000/docs", timeout=5)
        return "online" if response.status_code == 200 else "offline"
    except:
        return "offline"

# Check API status on first load
if st.session_state.api_status == "unknown":
    st.session_state.api_status = check_api_status()

# Show API status
if st.session_state.api_status == "online":
    st.success("✅ Connection Established")
else:
    st.error("❌ FastAPI server is offline. Please start your FastAPI server.")
    st.stop()

# Show header
if not st.session_state.chat_ended:
    st.markdown(f"💬 *You are currently conversing with the Business Owner of **{business_state['business_name']}***")
    st.markdown("---")
else:
    st.markdown("### 🔒 Chat session has ended.")

# Display chat history (skip system messages for display)
for message in st.session_state.messages:
    if message['role'] == 'system':
        continue

    role_display = "user" if message['role'] == 'human' else message['role']
    with st.chat_message(role_display):
        st.markdown(message["content"])

# Restart button if chat ended
if st.session_state.chat_ended:
    if st.button("🔄 Start New Chat"):
        st.session_state.chat_ended = False
        st.session_state.messages = []
        st.session_state.thread_id = None
        st.rerun()

    # Option to move to next assignment if chat has ended
    if st.button("🤝 Move to next assignment"):
        st.switch_page("pages/Assignment_2.py")

# Chat input
if not st.session_state.chat_ended:
    if prompt := st.chat_input("Ask a question about the business's security practices. Type 'exit' to end conversation."):
        if prompt.strip().lower() == "exit":
            with st.chat_message("assistant"):
                st.markdown("✅ Chat ended. Thank you for your questions!")
            st.session_state.chat_ended = True
            st.rerun()
        else:
            # Add user message to session state
            st.session_state.messages.append({"role": "human", "content": prompt})

            # Display user message
            with st.chat_message("user"):
                st.markdown(prompt)

            # Call FastAPI endpoint
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    # Prepare messages for API call
                    api_messages = [msg for msg in st.session_state.messages]

                    # Call the API
                    result = call_fastapi_chat(
                        messages=api_messages,
                        thread_id=st.session_state.thread_id
                    )

                    if result and "conversation" in result:
                        # Extract the latest AI response
                        conversation = result["conversation"]

                        # Find the last AI message
                        ai_response = None
                        for msg in reversed(conversation):
                            if msg["role"] == "ai":
                                ai_response = msg["content"]
                                break

                        if ai_response:
                            st.markdown(ai_response)
                            # Add AI response to session state
                            st.session_state.messages.append({"role": "ai", "content": ai_response})
                        else:
                            st.error("No AI response found in the conversation.")
                    else:
                        st.error("Failed to get response from the chatbot. Please try again.")
