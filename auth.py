import os
import streamlit as st
from dotenv import load_dotenv



# LOAD LOGIN DETAILS

load_dotenv()

VALID_USERNAME = os.getenv(
    "APP_USERNAME",
    "admin"
)

VALID_PASSWORD = os.getenv(
    "APP_PASSWORD",
    "admin123"
)



# LOGIN FUNCTION


def login():

    # Already logged in
    if st.session_state.get("authenticated", False):
        return True

    st.title("🔐 Enterprise AI Assistant")

    st.subheader("Please Login")

    username = st.text_input(
        "Username"
    )

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("🔑 Login"):

        if (
            username == VALID_USERNAME
            and password == VALID_PASSWORD
        ):

            st.session_state.authenticated = True

            st.success(
                "Login successful!"
            )

            st.rerun()

        else:

            st.error(
                "Invalid username or password."
            )

    return False



# LOGOUT FUNCTION


def logout():

    if st.sidebar.button("🚪 Logout"):

        st.session_state.authenticated = False

        st.rerun()