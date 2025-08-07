import streamlit as st
import requests


def assignment_page():
    url = "http://localhost:8000"

    st.title('Assignment 1.')

    # Initialize session state keys if not set
    if "graph_state" not in st.session_state:
        st.session_state.graph_state = {}

    if "assetsGeneratedState" not in st.session_state:
        st.session_state.assetsGeneratedState = False

    business_state = st.session_state.graph_state

    business_name = business_state.get('business_name', 'Unknown Business')
    business_description = business_state.get('business_description', 'No description available.')
    business_location = business_state.get('business_location', 'No location provided.')
    business_activity = business_state.get('business_activity', 'No activity provided.')

    st.markdown(f'#### The business that was assigned to you is called:\n### "{business_name}"')

    with st.expander("Assignment Details and Instructions Below", expanded=True):
        st.markdown("""
            ***Here is a breakdown of what you are expected to do for this assignment:***
            1. Take a look at the **business description, location, activities, and assets**. 
            2. Once you have a good idea of what the business does and what assets they have, **prepare a list of questions you have regarding their security practices**.
            3. When your list is ready, **go to the business owner and start the chat.** (*Note: They can only meet you a few times! Being a founder is difficult!*)
            4. **Ask the business owner the questions you prepared** for them, and *take notes* of their answers. (*Note: They are non-technical, so you will need to do some interpretation!*)
            5. Once you have the answers to your questions, you are ready to move to the next stage of this project!
        """)

    with st.expander('Expand to see the business details:', icon="➕", expanded=False):
        st.markdown(f"*Details below for*: ***{business_name}***<br/>"
                    f"**Business Description**:<br/>"
                    f"{business_description}<br/><br/>"
                    f"**Business Activity**:<br/>"
                    f"{business_activity}<br/><br/>"
                    f"**Business Location**:<br/>"
                    f"{business_location}<br/><br/>",
                    unsafe_allow_html=True)

    with st.expander('Expand to see the business assets:', icon="💾", expanded=False):
        assets_obj = business_state.get('assets')

        # Fetch assets only if not already fetched
        if not st.session_state.assetsGeneratedState:
            if not assets_obj or not isinstance(assets_obj, dict) or not assets_obj.get("assets"):
                with st.spinner("Fetching assets..."):
                    updated_state = requests.post(f"{url}/api/assets/generate-assets", json=business_state)
                    if updated_state.status_code == 200:
                        updated_state_json = updated_state.json()
                        st.session_state.graph_state = updated_state_json
                        st.session_state.assetsGeneratedState = True
                        business_state = updated_state_json
                        assets_obj = business_state.get('assets')
                    else:
                        st.error(f"Failed to fetch assets: {updated_state.status_code} - {updated_state.text}")
                        assets_obj = None

        # Show assets
        if assets_obj is not None:
            for idx, asset in enumerate(assets_obj['assets']):
                st.markdown(f"""
                *Asset {idx + 1}:* <br/>
                **Category**: <br/>
                {asset["category"]} <br/>
                **Description**: <br/>
                {asset["description"]}<br/><br/>
                """, unsafe_allow_html=True)
        else:
            st.info("No assets found.")

    if st.button("👔 Talk to the business owner"):
        st.switch_page("pages/Assignment_1b_Business_Owner.py")


if __name__ == '__main__':
    assignment_page()
