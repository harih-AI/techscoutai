def init_state(st):
    if "stage" not in st.session_state:
        st.session_state.stage = 0

    if "profile" not in st.session_state:
        st.session_state.profile = {
            "name": "",
            "email": "",
            "phone": "",
            "experience": "",
            "position": "",
            "location": "",
            "tech_stack": []
        }

    if "questions" not in st.session_state:
        st.session_state.questions = []

    if "current_tech" not in st.session_state:
        st.session_state.current_tech = 0
