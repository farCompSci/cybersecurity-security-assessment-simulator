import streamlit as st
import requests


def assignment_page():
    business_state = st.session_state.get("graph_state", {})
    business_name = business_state.get('business_name', 'Unknown Business')
    business_description = business_state.get('business_description', 'No description available.')
    business_location = business_state.get('business_location', 'No location provided.')
    business_activity = business_state.get('business_activity', 'No activity provided.')

    base_url = "http://localhost:8000"
    security_assessment_md = requests.get(f"{base_url}/api/retrieve-file/retrieve-security-template").text

    st.title('Assignment 2.')
    st.markdown(
        f'#### Now that you talked to the owner of {str(business_state['business_name']).title()}, it is time to put together an assessment.')
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

    if st.button("⛑️ If you're stuck, ask the TA for Help"):
        st.switch_page("pages/Assignment_2b_Teaching_Assistant.py")


if __name__ == '__main__':
    assignment_page()
