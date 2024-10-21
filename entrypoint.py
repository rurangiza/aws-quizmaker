import streamlit as st

PAGE_DIR = "_pages/"

pg = st.navigation(
    [
        st.Page(
            PAGE_DIR + "quiz.py",
            title="Quiz",
            icon=":material/quiz:",
            default=True
        ),
        st.Page(
            PAGE_DIR + "settings.py",
            title="Settings",
            icon=":material/settings:",
        ),
    ]
)

pg.run()