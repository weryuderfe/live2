import sys
import subprocess
import os
import time
import streamlit as st

def check_dependencies(packages):
    """Check if required packages are installed"""
    missing_packages = []
    
    for package in packages:
        try:
            __import__(package.replace('-', '_').split('>=')[0].split('==')[0])
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        return False
    return True

def install_missing_dependencies(packages):
    """Install missing dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + packages)
        return True
    except Exception as e:
        st.error(f"Failed to install dependencies: {str(e)}")
        return False

def check_ffmpeg_installed():
    """Check if FFmpeg is installed and accessible"""
    try:
        result = subprocess.run(
            ["ffmpeg", "-version"], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        return True
    except:
        return False

def get_video_info(video_path):
    """Get video information using FFmpeg"""
    if not os.path.exists(video_path):
        return None
    
    try:
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", 
             "format=duration,size", "-show_streams", 
             "-of", "default=noprint_wrappers=1", video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        output = result.stdout
        
        # Parse the output to extract video information
        info = {}
        
        # Get duration
        duration_match = output.find("duration=")
        if duration_match >= 0:
            duration_str = output[duration_match:].split("\n")[0].split("=")[1]
            try:
                duration = float(duration_str)
                info["duration"] = duration
                
                # Format duration
                hours, remainder = divmod(int(duration), 3600)
                minutes, seconds = divmod(remainder, 60)
                info["duration_str"] = f"{hours:02}:{minutes:02}:{seconds:02}"
            except:
                info["duration"] = 0
                info["duration_str"] = "00:00:00"
        
        # Get dimensions
        width_match = output.find("width=")
        height_match = output.find("height=")
        if width_match >= 0 and height_match >= 0:
            width_str = output[width_match:].split("\n")[0].split("=")[1]
            height_str = output[height_match:].split("\n")[0].split("=")[1]
            try:
                info["width"] = int(width_str)
                info["height"] = int(height_str)
                info["resolution"] = f"{width_str}x{height_str}"
            except:
                info["width"] = 0
                info["height"] = 0
                info["resolution"] = "Unknown"
        
        # Get file size
        size_match = output.find("size=")
        if size_match >= 0:
            size_str = output[size_match:].split("\n")[0].split("=")[1]
            try:
                size_bytes = int(size_str)
                info["size_bytes"] = size_bytes
                
                # Format size
                if size_bytes < 1024:
                    info["size_str"] = f"{size_bytes} bytes"
                elif size_bytes < 1024 * 1024:
                    info["size_str"] = f"{size_bytes/1024:.2f} KB"
                elif size_bytes < 1024 * 1024 * 1024:
                    info["size_str"] = f"{size_bytes/(1024*1024):.2f} MB"
                else:
                    info["size_str"] = f"{size_bytes/(1024*1024*1024):.2f} GB"
            except:
                info["size_bytes"] = 0
                info["size_str"] = "Unknown"
        
        return info
    except Exception as e:
        return None

def update_mock_analytics_data():
    """Update mock analytics data for simulated real-time updates"""
    if 'analytics_data' in st.session_state:
        # Simple logic to add some randomness and trends to the mock data
        import random
        
        data = st.session_state.analytics_data
        
        # Add some random variation
        views = data['views'][-1] + random.randint(-5, 10)
        likes = data['likes'][-1] + random.randint(-1, 3)
        comments = data['comments'][-1] + random.randint(-1, 2)
        
        # Enforce minimums
        views = max(views, 0)
        likes = max(likes, 0)
        comments = max(comments, 0)
        
        # Update the data by removing the first element and adding the new one
        data['views'] = data['views'][1:] + [views]
        data['likes'] = data['likes'][1:] + [likes]
        data['comments'] = data['comments'][1:] + [comments]
        
        st.session_state.analytics_data = data