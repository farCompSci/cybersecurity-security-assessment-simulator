import streamlit as st

st.title("Assignment Final Submission")
st.markdown(
"""
Welcome to the final part of the assessment! Once you are happy with your results, you can submit them here.
""")
if "submitted" not in st.session_state:
    st.session_state.submitted = False

if not st.session_state.submitted:
    with st.form(key="final-submission"):
        uploaded_file = st.file_uploader("Upload your file here")
        submit_button = st.form_submit_button(label="Submit")

        if submit_button:
            if uploaded_file is not None:
                st.session_state.submitted = True
                st.success("File submitted!")
                st.balloons()
            else:
                st.warning("Please upload a file before submitting.")
else:
    st.success("You have already submitted the file. Thank you!")