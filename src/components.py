import os
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import streamlit.components.v1 as components
from PIL import Image
import io
import base64

def render_header():
    """Render application header with logo and title"""
    st.markdown(
        """
        <div class="header">
            <div class="logo-container">
                <div class="logo-icon">🎬</div>
                <div class="logo-text">StreamHub<span class="highlight">Pro</span></div>
            </div>
            <div class="theme-toggle" onclick="toggleTheme()">
                <span id="theme-icon">🌙</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_sidebar():
    """Render sidebar with navigation and user options"""
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-header">
                <div class="sidebar-title">Navigation</div>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Navigation buttons with active state
        nav_items = ["Stream", "Analytics"]
        
        for item in nav_items:
            active_class = "active" if st.session_state.selected_tab == item else ""
            icon = "📺" if item == "Stream" else "📊"
            
            if st.button(
                f"{icon} {item}", 
                key=f"nav_{item}", 
                use_container_width=True,
                type="primary" if st.session_state.selected_tab == item else "secondary"
            ):
                st.session_state.selected_tab = item
                st.experimental_rerun()
        
        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        
        # Stream status indicator
        status = "🟢 Active" if st.session_state.get('streaming', False) else "⚪ Inactive"
        st.markdown(
            f"""
            <div class="status-indicator">
                <div class="status-label">Stream Status:</div>
                <div class="status-value {'status-active' if st.session_state.get('streaming', False) else ''}">
                    {status}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Stream duration if active
        if st.session_state.get('streaming', False) and 'stream_manager' in st.session_state:
            duration = st.session_state.stream_manager.get_stream_duration()
            hours, remainder = divmod(duration, 3600)
            minutes, seconds = divmod(remainder, 60)
            duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
            
            st.markdown(
                f"""
                <div class="duration-indicator">
                    <div class="duration-label">Duration:</div>
                    <div class="duration-value">{duration_str}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("<div class='sidebar-divider'></div>", unsafe_allow_html=True)
        
        # App info section
        st.markdown(
            """
            <div class="app-info">
                <div class="info-title">About StreamHub Pro</div>
                <div class="info-text">
                    A professional YouTube streaming solution designed for content creators.
                </div>
                <div class="app-version">Version 1.0.0</div>
            </div>
            """,
            unsafe_allow_html=True
        )

def render_footer():
    """Render application footer with credits and links"""
    st.markdown(
        """
        <div class="footer">
            <div class="footer-content">
                <div class="footer-text">
                    StreamHub Pro © 2025 | Created with ❤️
                </div>
                <div class="footer-links">
                    <a href="#" class="footer-link">Documentation</a>
                    <a href="#" class="footer-link">Support</a>
                    <a href="#" class="footer-link">Updates</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_upload_section():
    """Render video upload and selection section"""
    with st.expander("📁 Video Selection", expanded=True):
        st.markdown(
            """
            <div class="section-title">
                <span>Select or Upload Video</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Get available video files
        video_files = [f for f in os.listdir('.') if f.endswith(('.mp4', '.flv', '.mov', '.avi'))]
        
        # Create tabs for selection and upload
        tab1, tab2 = st.tabs(["Select Existing", "Upload New"])
        
        with tab1:
            if video_files:
                selected_video = st.selectbox(
                    "Available videos", 
                    options=video_files, 
                    format_func=lambda x: f"{x} ({os.path.getsize(x)/1024/1024:.1f} MB)"
                )
                
                if selected_video:
                    st.session_state.video_path = selected_video
                    
                    # Display video info 
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        st.markdown(f"**File:** {selected_video}")
                        st.markdown(f"**Size:** {os.path.getsize(selected_video)/1024/1024:.2f} MB")
                    
                    with col2:
                        st.markdown(f"**Last Modified:** {time.ctime(os.path.getmtime(selected_video))}")
                        
                    # Video preview (show first frame as image)
                    st.markdown("### Preview")
                    st.video(selected_video, start_time=0)
            else:
                st.info("No video files found. Please upload a video file.")
        
        with tab2:
            uploaded_file = st.file_uploader(
                "Upload video file", 
                type=['mp4', 'flv', 'mov', 'avi'],
                help="Upload a video file to stream to YouTube"
            )
            
            if uploaded_file:
                # Save uploaded file
                file_path = os.path.join('.', uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                st.session_state.video_path = file_path
                st.success(f"Video uploaded successfully: {uploaded_file.name}")
                
                # Show preview
                st.video(file_path, start_time=0)

def render_stream_config():
    """Render stream configuration options"""
    with st.expander("⚙️ Stream Configuration", expanded=True):
        st.markdown(
            """
            <div class="section-title">
                <span>Streaming Settings</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Stream key input
        stream_key = st.text_input(
            "YouTube Stream Key", 
            type="password",
            help="Your YouTube stream key from your YouTube Studio dashboard",
            value=st.session_state.get('stream_key', '')
        )
        
        if stream_key:
            st.session_state.stream_key = stream_key
        
        # Create columns for settings
        col1, col2 = st.columns(2)
        
        with col1:
            # Video format settings
            st.markdown("##### Video Settings")
            
            is_shorts = st.toggle(
                "YouTube Shorts Mode (Vertical 720x1280)", 
                value=st.session_state.get('is_shorts', False),
                help="Enable for vertical YouTube Shorts format"
            )
            st.session_state.is_shorts = is_shorts
            
            quality_options = {
                "ultrafast": "Lowest Quality / Fastest",
                "superfast": "Lower Quality / Fast",
                "veryfast": "Standard (Recommended)",
                "faster": "Better Quality / Slower",
                "medium": "Good Quality / Slow"
            }
            
            quality_preset = st.select_slider(
                "Quality Preset",
                options=list(quality_options.keys()),
                value=st.session_state.get('quality_preset', 'veryfast'),
                format_func=lambda x: quality_options[x]
            )
            st.session_state.quality_preset = quality_preset
            
            bitrate = st.select_slider(
                "Video Bitrate",
                options=["1000k", "1500k", "2000k", "2500k", "3000k", "3500k", "4000k"],
                value=st.session_state.get('bitrate', '2500k')
            )
            st.session_state.bitrate = bitrate
        
        with col2:
            # Schedule settings
            st.markdown("##### Stream Schedule")
            
            use_schedule = st.toggle(
                "Schedule Stream", 
                value=st.session_state.get('use_schedule', False),
                help="Set a specific time to start streaming"
            )
            st.session_state.use_schedule = use_schedule
            
            if use_schedule:
                schedule_date = st.date_input(
                    "Date",
                    value=datetime.now().date(),
                    min_value=datetime.now().date()
                )
                
                schedule_time = st.time_input(
                    "Time",
                    value=datetime.now().time()
                )
                
                # Combine date and time
                scheduled_datetime = datetime.combine(schedule_date, schedule_time)
                
                # Check if scheduled time is in the past
                if scheduled_datetime < datetime.now():
                    st.warning("Scheduled time must be in the future")
            
            # Audio settings
            st.markdown("##### Audio Settings")
            
            audio_bitrate = st.select_slider(
                "Audio Bitrate",
                options=["64k", "96k", "128k", "160k", "192k"],
                value=st.session_state.get('audio_bitrate', '128k')
            )
            st.session_state.audio_bitrate = audio_bitrate
        
        # Control buttons
        st.markdown("<div class='control-buttons'>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button(
                "▶️ Start Streaming", 
                type="primary",
                use_container_width=True,
                disabled=st.session_state.get('streaming', False)
            ):
                if not hasattr(st.session_state, 'video_path') or not st.session_state.video_path:
                    st.error("Please select or upload a video first")
                elif not stream_key:
                    st.error("Please enter your YouTube stream key")
                else:
                    # Gather configuration
                    config = {
                        'is_shorts': st.session_state.is_shorts,
                        'quality_preset': st.session_state.quality_preset,
                        'bitrate': st.session_state.bitrate,
                        'audio_bitrate': st.session_state.audio_bitrate
                    }
                    
                    if st.session_state.get('use_schedule', False) and scheduled_datetime > datetime.now():
                        # Schedule stream
                        success = st.session_state.stream_manager.schedule_stream(scheduled_datetime)
                        if success:
                            st.success(f"Stream scheduled for {scheduled_datetime.strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        # Start stream immediately
                        success = st.session_state.stream_manager.start_streaming(
                            st.session_state.video_path, 
                            stream_key,
                            config
                        )
                        if success:
                            st.session_state.streaming = True
                            st.success("Streaming started!")
                            st.experimental_rerun()
        
        with col2:
            if st.button(
                "⏹️ Stop Streaming", 
                type="secondary",
                use_container_width=True,
                disabled=not st.session_state.get('streaming', False)
            ):
                success = st.session_state.stream_manager.stop_streaming()
                if success:
                    st.session_state.streaming = False
                    st.warning("Streaming stopped")
                    st.experimental_rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)

def render_stream_logs():
    """Render streaming logs with real-time updates"""
    with st.expander("📊 Stream Status & Logs", expanded=True):
        st.markdown(
            """
            <div class="section-title">
                <span>Live Stream Logs</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Stream status visualization
        if st.session_state.get('streaming', False):
            # Create a progress bar that updates
            progress_val = (time.time() % 10) / 10  # Cycles every 10 seconds
            st.progress(progress_val, "Stream Active")
            
            # Display stream duration
            if 'stream_manager' in st.session_state:
                duration = st.session_state.stream_manager.get_stream_duration()
                hours, remainder = divmod(duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = f"{hours:02}:{minutes:02}:{seconds:02}"
                
                st.markdown(
                    f"""
                    <div class="duration-display">
                        <div class="duration-label">Stream Duration</div>
                        <div class="duration-timer">{duration_str}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            if st.session_state.stream_manager.scheduled_time:
                # Display countdown to scheduled stream
                now = datetime.now()
                time_diff = (st.session_state.stream_manager.scheduled_time - now).total_seconds()
                
                if time_diff > 0:
                    hours, remainder = divmod(int(time_diff), 3600)
                    minutes, seconds = divmod(remainder, 60)
                    countdown = f"{hours:02}:{minutes:02}:{seconds:02}"
                    
                    st.markdown(
                        f"""
                        <div class="countdown-display">
                            <div class="countdown-label">Stream starts in</div>
                            <div class="countdown-timer">{countdown}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            else:
                st.info("Stream is not active. Click 'Start Streaming' to begin.")
        
        # Log display area with auto-scroll
        st.markdown("<div class='log-container'>", unsafe_allow_html=True)
        
        logs = st.session_state.get('logs', [])
        if logs:
            log_text = "\n".join(logs)
            
            st.code(log_text, language="bash")
            
            # Auto-scroll log container
            st.markdown(
                """
                <script>
                    const logElement = document.querySelector('.log-container pre');
                    if (logElement) {
                        logElement.scrollTop = logElement.scrollHeight;
                    }
                </script>
                """,
                unsafe_allow_html=True
            )
        else:
            st.text("No logs available yet.")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Add clear logs button
        if st.button("Clear Logs", key="clear_logs"):
            st.session_state.logs = []
            st.experimental_rerun()

def render_analytics_dashboard():
    """Render analytics dashboard with visualizations"""
    st.markdown(
        """
        <div class="dashboard-header">
            <div class="dashboard-title">Stream Analytics</div>
            <div class="dashboard-subtitle">Performance metrics and insights</div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Create mock data for demonstration
    data = st.session_state.analytics_data
    
    # Create tabs for different analytics sections
    tab1, tab2, tab3 = st.tabs(["Overview", "Audience", "Performance"])
    
    with tab1:
        # Key metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            render_metric_card("Total Views", data['views'][-1], "+15%", "📈")
        
        with col2:
            render_metric_card("Peak Viewers", max(data['views']), "", "👥")
        
        with col3:
            render_metric_card("Total Likes", data['likes'][-1], "+20%", "👍")
        
        with col4:
            render_metric_card("Comments", data['comments'][-1], "+5%", "💬")
        
        # Charts
        st.markdown("### Viewer Engagement")
        
        # Create time series data
        current_time = datetime.now()
        timestamps = [(current_time - timedelta(minutes=i*10)).strftime("%H:%M") 
                     for i in range(len(data['views'])-1, -1, -1)]
        
        # Create DataFrame
        df = pd.DataFrame({
            'Time': timestamps,
            'Views': data['views'],
            'Likes': data['likes'],
            'Comments': data['comments']
        })
        
        # Create interactive chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['Time'], 
            y=df['Views'],
            mode='lines+markers',
            name='Views',
            line=dict(color='#4361ee', width=3),
            marker=dict(size=8)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Time'], 
            y=df['Likes'],
            mode='lines+markers',
            name='Likes',
            line=dict(color='#3a0ca3', width=2),
            marker=dict(size=6)
        ))
        
        fig.add_trace(go.Scatter(
            x=df['Time'], 
            y=df['Comments'],
            mode='lines+markers',
            name='Comments',
            line=dict(color='#7209b7', width=2),
            marker=dict(size=6)
        ))
        
        fig.update_layout(
            xaxis_title='Time',
            yaxis_title='Count',
            template='plotly_white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=20, r=20, t=30, b=20),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.markdown("### Audience Demographics")
        
        # Mock demographic data
        age_data = {
            'Age Group': ['13-17', '18-24', '25-34', '35-44', '45-54', '55-64', '65+'],
            'Percentage': [12, 28, 35, 15, 6, 3, 1]
        }
        
        gender_data = {
            'Gender': ['Male', 'Female', 'Non-binary', 'Other'],
            'Percentage': [65, 30, 3, 2]
        }
        
        location_data = {
            'Country': ['United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 'Other'],
            'Viewers': [45, 15, 10, 8, 7, 15]
        }
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # Age distribution chart
            fig_age = go.Figure(go.Bar(
                x=age_data['Age Group'],
                y=age_data['Percentage'],
                marker_color='#4cc9f0',
                text=age_data['Percentage'],
                textposition='auto',
            ))
            
            fig_age.update_layout(
                title='Age Distribution (%)',
                xaxis_title='Age Group',
                yaxis_title='Percentage',
                template='plotly_white',
                height=300
            )
            
            st.plotly_chart(fig_age, use_container_width=True)
        
        with col2:
            # Gender distribution chart - pie chart
            fig_gender = go.Figure(go.Pie(
                labels=gender_data['Gender'],
                values=gender_data['Percentage'],
                hole=.4,
                marker=dict(colors=['#480ca8', '#4361ee', '#4cc9f0', '#f72585'])
            ))
            
            fig_gender.update_layout(
                title='Gender Distribution',
                template='plotly_white',
                height=300,
                margin=dict(l=20, r=20, t=60, b=20)
            )
            
            st.plotly_chart(fig_gender, use_container_width=True)
        
        # Location data
        st.markdown("### Geographic Distribution")
        
        fig_location = go.Figure(go.Bar(
            x=location_data['Country'],
            y=location_data['Viewers'],
            marker_color='#4361ee',
            text=location_data['Viewers'],
            textposition='auto',
        ))
        
        fig_location.update_layout(
            xaxis_title='Country',
            yaxis_title='Viewers (%)',
            template='plotly_white',
            height=300
        )
        
        st.plotly_chart(fig_location, use_container_width=True)
    
    with tab3:
        st.markdown("### Stream Performance")
        
        # Mock performance data
        performance_data = {
            'Metric': ['Stream Health', 'Buffering', 'Resolution', 'Frame Rate', 'Audio Quality'],
            'Score': [92, 85, 90, 95, 88]
        }
        
        # Performance gauge charts
        cols = st.columns(3)
        
        for i, (metric, score) in enumerate(zip(performance_data['Metric'], performance_data['Score'])):
            with cols[i % 3]:
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': metric},
                    gauge = {
                        'axis': {'range': [0, 100]},
                        'bar': {'color': get_color_for_score(score)},
                        'steps': [
                            {'range': [0, 50], 'color': "#ffadad"},
                            {'range': [50, 75], 'color': "#ffd6a5"},
                            {'range': [75, 90], 'color': "#caffbf"},
                            {'range': [90, 100], 'color': "#9bf6ff"}
                        ]
                    }
                ))
                
                fig.update_layout(height=250)
                st.plotly_chart(fig, use_container_width=True)
        
        # Stream quality over time
        st.markdown("### Stream Quality Over Time")
        
        # Mock quality data
        quality_times = [(current_time - timedelta(minutes=i*10)).strftime("%H:%M") 
                         for i in range(10-1, -1, -1)]
        quality_data = [85, 88, 92, 95, 94, 90, 92, 96, 98, 95]
        
        fig_quality = go.Figure()
        
        fig_quality.add_trace(go.Scatter(
            x=quality_times, 
            y=quality_data,
            mode='lines+markers',
            name='Stream Quality',
            line=dict(color='#4361ee', width=3),
            marker=dict(size=8)
        ))
        
        fig_quality.update_layout(
            xaxis_title='Time',
            yaxis_title='Quality Score',
            template='plotly_white',
            height=300
        )
        
        st.plotly_chart(fig_quality, use_container_width=True)

def render_metric_card(title, value, change, icon):
    """Render a metric card with icon and value"""
    change_color = "text-green-500" if "+" in str(change) else "text-red-500"
    
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-icon">{icon}</div>
            <div class="metric-info">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-change {change_color}">{change}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def get_color_for_score(score):
    """Return appropriate color based on score"""
    if score >= 90:
        return "#00b4d8"  # Blue
    elif score >= 75:
        return "#06d6a0"  # Green
    elif score >= 50:
        return "#ffd166"  # Yellow
    else:
        return "#ef476f"  # Red