import streamlit as st
import requests
from loguru import logger


def assignment_page():
    business_state = st.session_state.get("graph_state", {})
    business_name = business_state.get('business_name', 'Unknown Business')
    business_description = business_state.get('business_description', 'No description available.')
    business_location = business_state.get('business_location', 'No location provided.')
    business_activity = business_state.get('business_activity', 'No activity provided.')

    base_url = "http://localhost:8000"
    security_assessment_md = requests.get(f"{base_url}/api/retrieve-file/retrieve-security-template").text

    if "threatsGeneratedState" not in st.session_state:
        st.session_state.threatsGeneratedState = False

    st.title('Assignment 2.')
    st.markdown(
        f'#### Now that you talked to the owner of {business_name.title()}, it is time to put together an assessment.')
    with st.expander("Assignment Details and Instructions Below", expanded=True):
        st.markdown("""
            ***Here is a breakdown of what you are expected to do for this assignment:***
            1. Review your notes from your conversation with the business owner. 
            2. Take a look at the **security template provided in an expandable section below**.
            3. Start writing a draft of the **security template** for the company.
            4. If you are stuck, you can **access the TA for this class**, who will help you fill out the security template.
            5. When you are satisfied with your security template, go to the Submission Page at the end of the assessment and Press Submit
        """)
    with st.expander('If you need a reminder, expand to see the business details:', icon="➕", expanded=False):
        st.markdown(f"*Details below for*: ***{business_name}***<br/>"
                    f"**Business Description**:<br/>"
                    f"{business_description}<br/><br/>"
                    f"**Business Activity**:<br/>"
                    f"{business_activity}<br/><br/>"
                    f"**Business Location**:<br/>"
                    f"{business_location}<br/><br/>",
                    unsafe_allow_html=True)

    with st.expander('📋 Expand for Full Security Template'):
        st.markdown(
            f"""
            {security_assessment_md}
            """
        )

    with st.expander('Expand for hints:', icon="💡", expanded=False):
        threats_obj = business_state.get('potential_threats')

        # Fetch threats only if not already fetched
        if (
                not threats_obj
                or not isinstance(threats_obj, dict)
                or not threats_obj.get("threats")
        ) and not st.session_state.get("threatsGeneratedState", False):
            with st.spinner("Fetching hints..."):
                updated_state = requests.post(f"{base_url}/api/threats/generate-threats", json=business_state)
                if updated_state.status_code == 200:
                    updated_state_json = updated_state.json()
                    st.session_state.graph_state = updated_state_json
                    st.session_state.threatsGeneratedState = True
                    business_state = updated_state_json
                    threats_obj = business_state.get('potential_threats')
                else:
                    st.error(f"Failed to fetch hints: {updated_state.status_code} - {updated_state.text}")
                    threats_obj = None

        # Show threats
        if threats_obj is not None and isinstance(threats_obj, dict) and threats_obj.get("threats"):
            st.markdown("<h3>Consider the following potential threats the business could face</h3><br/>"
                        "<p><strong>Can the owner do anything about these threats?</strong></p>", unsafe_allow_html=True)
            for idx, threat in enumerate(threats_obj["threats"]):
                st.markdown(f"""
                *Potential Threat {idx + 1}:* <br/>
                **Category**: <br/>
                {threat.get("category", "N/A")} <br/>
                **Description**: <br/>
                {threat.get("description", "N/A")}<br/><br/>
                """, unsafe_allow_html=True)
        else:
            st.info("No hints found.")

    if st.button("⛑️ If you're stuck, ask the TA for Help"):
        st.switch_page("pages/Assignment_2b_Teaching_Assistant.py")


if __name__ == '__main__':
    assignment_page()
