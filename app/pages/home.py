# app.py

import streamlit as st
from app.utils.helpers import load_css, display_header


def main():
    load_css("app/static/css/styles.css")
    display_header()

    st.markdown("---")
    st.title("Welcome to the Healthcare Management System")
    st.write("""
        This platform allows patients to input their symptoms and doctors to manage patient information.
    """)

    # Add an overview or features
    st.subheader("Features")
    features = [
        "User-friendly interface for patients and doctors.",
        "Symptom input for patients via text or speech.",
        "Comprehensive dashboards for managing healthcare activities.",
    ]

    for feature in features:
        st.markdown(f"- {feature}")


if __name__ == "__main__":
    main()
