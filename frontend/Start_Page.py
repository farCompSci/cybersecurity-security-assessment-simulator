import streamlit as st
import requests


def main_page():
    st.header('Welcome to the Cyber Assessment Simulation!')

    st.html(
        """
        <div style="border: 2px solid orange; border-radius: 10px; padding: 20px; margin-bottom: 30px; background-color: #fffbe6;">
            <h3 style="margin-top: 0; margin-bottom: 0;">Purpose of this tool</h3>
            <p>This platform was designed to help you work through a cybersecurity assessment for a company.</p>

            <h3 style="margin-top: 0; margin-bottom: 0;">What the process is:</h3>
            <ol style="list-style-position: outside; padding-left: 4em;">
                <li>You will be assigned a business to assess.</li>
                <li>You will be provided a file with the business description and its summary.</li>
                <li>You will be given the chance to ask questions to the business owner.</li>
            </ol>

            <h3 style="margin-top: 0; margin-bottom: 0;">How to get started?</h3>
            <p>Click on the button below, and it will take you to the assessment.</p>
        </div>
        """)


if __name__ == "__main__":
    url = "http://localhost:8000"
    st.set_page_config(
        page_title="Cyber Assessment Simulation",
        page_icon="🧢",
        initial_sidebar_state="collapsed"
    )

    main_page()

    with st.spinner("Loading resources in background..."):
        if "graph_state" not in st.session_state:
            try:
                response = requests.get(f"{url}/api/business/generate-business")
                response.raise_for_status()  # Raises an error if status != 200
                st.session_state.graph_state = response.json()
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to fetch business data: {e}")

    if st.button("🚀 Get Started"):
        st.switch_page("pages/Assignment_1a_Business_Description.py")
