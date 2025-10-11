import streamlit as st
from app.utils.helpers import (
    load_css,
    display_header,
    get_current_timestamp,
    get_mongo_client,
)
import json
import os
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode, ClientSettings
import av
import numpy as np
from ai_crew.main import run




def main():
    load_css("app/static/css/styles.css")
    display_header()

    st.markdown("---")
    st.header("Patients Page")

    # Clear the report file
    report_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "analysis_outputs", "final_report.txt")
    open(report_path, 'w').close()

    if "logged_in" in st.session_state and st.session_state["logged_in"]:
        if st.session_state["role"] == "patient":
            st.write("""
                Welcome to the **Patients Dashboard**. You can input your symptoms below to help healthcare providers understand your condition.
            """)

            with st.form("symptom_form"):
                symptoms = st.text_area("Describe your symptoms here:", height=200)
                submit = st.form_submit_button("Submit Symptoms")

            if submit:
                if symptoms.strip() == "":
                    st.error("Please enter your symptoms before submitting.")
                else:
                    symptom_data = {
                        "username": st.session_state["username"],
                        "symptoms_text": symptoms.strip(),
                        "submitted_at": get_current_timestamp(),
                    }

                    client = get_mongo_client()
                    if client:
                        db = client["myDatabase"]
                        symptoms_collection = db["symptoms"]
                        user_collection = db["users"]

                        def get_user_profile(username):
                            return user_collection.find_one({"username": username})
                        user_profile = get_user_profile(st.session_state["username"])

                        try:
                            symptoms_collection.insert_one(symptom_data)
                            st.success(
                                "Your symptoms have been successfully submitted!"
                            )
                        except Exception as e:
                            st.error(
                                f"An error occurred while submitting your symptoms: {e}"
                            )
                        run(symptoms.strip(), user_profile.get("name","Name not specified"), user_profile.get("ethnicity","Ethnicity not defined"), user_profile.get("sex", "Sex is not defined"))
                    else:
                        st.error(
                            "Failed to connect to the database. Please try again later."
                        )

                        
        else:
            st.error("Access Denied: You do not have permission to view this page.")
    else:
        st.warning("Please log in to access the Patients page.")
    # Specify the path to your text file
    file_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "analysis_outputs", "final_report.txt")

    try:
        # Open the file and read its contents
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        # Display the contents
        st.text_area("Doctor Recommendation and Potential Diagnoses", content, height=300)
    except FileNotFoundError:
        st.error("File not found. Please check the file path.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
