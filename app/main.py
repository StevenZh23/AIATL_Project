"""
AIATL - AI-Assisted Triage and Learning System
Main Streamlit Application Entry Point
"""

import streamlit as st
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.pages.home import main as home_main

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="AIATL - Healthcare Management System",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Run the home page
    home_main()

if __name__ == "__main__":
    main()
