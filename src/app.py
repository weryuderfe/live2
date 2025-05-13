import os
import sys
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import streamlit.components.v1 as components

# Local imports
from utils import check_dependencies, install_missing_dependencies
from components import (
    render_header, render_sidebar, render_footer,
    render_upload_section, render_stream_config, 
    render_analytics_dashboard, render_stream_logs
)
from streaming import StreamingManager
from styles import apply_custom_styles

# Ensure dependencies are installed
required_packages = [
    "streamlit", "streamlit-extras", "plotly", 
    "pandas", "watchdog", "pillow"
]

if not check_dependencies(required_packages):
    with st.spinner("Installing required dependencies..."):
        install_missing_dependencies(required_packages)
        st.experimental_rerun()

# Initialize session state variables if they don't exist
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"
if 'streaming' not in st.session_state:
    st.session_state.streaming = False
if 'logs' not in st.session_state:
    st.session_state.logs = []
if 'stream_manager' not in st.session_state:
    st.session_state.stream_manager = StreamingManager()
if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = "Stream"
if 'analytics_data' not in st.session_state:
    st.session_state.analytics_data = {
        'views': [0, 10, 25, 40, 60, 75, 90, 85, 70, 65],
        'likes': [0, 2, 5, 8, 12, 15, 18, 17, 14, 13],
        'comments': [0, 1, 3, 5, 7, 8, 10, 9, 8, 7],
    }

def main():
    # Apply custom CSS styles
    apply_custom_styles()
    
    # Configure page settings
    st.set_page_config(
        page_title="StreamHub Pro - YouTube Streaming",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Render header with logo and title
    render_header()
    
    # Render sidebar with navigation
    render_sidebar()
    
    # Main content area based on selected tab
    if st.session_state.selected_tab == "Stream":
        col1, col2 = st.columns([3, 2])
        
        with col1:
            # Video upload/selection section
            render_upload_section()
            
            # Stream configuration section
            render_stream_config()
        
        with col2:
            # Stream logs section
            render_stream_logs()
    
    elif st.session_state.selected_tab == "Analytics":
        render_analytics_dashboard()
    
    # Render footer with credits
    render_footer()

if __name__ == "__main__":
    main()