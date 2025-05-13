import os
import sys
import subprocess
import threading
import time
import streamlit as st
from datetime import datetime

class StreamingManager:
    """Manages YouTube streaming functionality using FFmpeg"""
    
    def __init__(self):
        self.process = None
        self.thread = None
        self.is_streaming = False
        self.start_time = None
        self.scheduled_time = None
        self.video_path = None
        self.stream_key = None
        self.is_shorts = False
        self.quality_preset = "veryfast"
        self.bitrate = "2500k"
        self.audio_bitrate = "128k"
    
    def log_message(self, message):
        """Add log message with timestamp to session state logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        
        if 'logs' in st.session_state:
            st.session_state.logs.append(log_entry)
            # Keep only the last 100 logs to prevent memory issues
            if len(st.session_state.logs) > 100:
                st.session_state.logs = st.session_state.logs[-100:]
    
    def start_streaming(self, video_path, stream_key, config):
        """Start streaming to YouTube"""
        if self.is_streaming:
            self.log_message("Already streaming. Please stop current stream first.")
            return False
        
        if not video_path or not stream_key:
            self.log_message("Error: Video path and stream key must be provided.")
            return False
        
        self.video_path = video_path
        self.stream_key = stream_key
        self.is_shorts = config.get('is_shorts', False)
        self.quality_preset = config.get('quality_preset', 'veryfast')
        self.bitrate = config.get('bitrate', '2500k')
        self.audio_bitrate = config.get('audio_bitrate', '128k')
        
        # Start streaming in a new thread
        self.is_streaming = True
        self.start_time = datetime.now()
        self.thread = threading.Thread(
            target=self._run_ffmpeg_stream, 
            daemon=True
        )
        self.thread.start()
        
        self.log_message(f"Started streaming: {os.path.basename(video_path)}")
        return True
    
    def stop_streaming(self):
        """Stop current streaming session"""
        if not self.is_streaming:
            self.log_message("No active stream to stop.")
            return False
        
        self.is_streaming = False
        # Kill ffmpeg process
        try:
            if os.name == 'nt':  # Windows
                subprocess.run(["taskkill", "/F", "/IM", "ffmpeg.exe"], 
                              stdout=subprocess.DEVNULL, 
                              stderr=subprocess.DEVNULL)
            else:  # Unix/Linux
                os.system("pkill -9 ffmpeg")
            
            self.log_message("Streaming stopped successfully.")
        except Exception as e:
            self.log_message(f"Error stopping stream: {str(e)}")
            return False
        
        return True
    
    def _run_ffmpeg_stream(self):
        """Execute FFmpeg command to stream to YouTube"""
        output_url = f"rtmp://a.rtmp.youtube.com/live2/{self.stream_key}"
        
        # Base command
        cmd = [
            "ffmpeg", "-re", "-stream_loop", "-1", "-i", self.video_path,
            "-c:v", "libx264", "-preset", self.quality_preset, 
            "-b:v", self.bitrate, "-maxrate", self.bitrate,
            "-bufsize", f"{int(self.bitrate.replace('k', '')) * 2}k",
            "-g", "60", "-keyint_min", "60",
            "-c:a", "aac", "-b:a", self.audio_bitrate,
            "-f", "flv"
        ]
        
        # Add scale filter for shorts mode
        if self.is_shorts:
            cmd += ["-vf", "scale=720:1280"]
        
        # Add output URL
        cmd.append(output_url)
        
        self.log_message(f"Executing FFmpeg command")
        
        try:
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Read output line by line
            for line in self.process.stdout:
                if not self.is_streaming:
                    break
                if "frame=" in line or "speed=" in line:
                    # For frame statistics, only log every 10 seconds to avoid spam
                    if time.time() % 10 < 1:
                        self.log_message(line.strip())
                elif "error" in line.lower() or "warning" in line.lower():
                    self.log_message(line.strip())
            
            self.process.wait()
            
        except Exception as e:
            self.log_message(f"Streaming error: {str(e)}")
        finally:
            if self.is_streaming:
                self.is_streaming = False
                self.log_message("Stream ended unexpectedly.")
    
    def schedule_stream(self, scheduled_time):
        """Schedule stream to start at a specific time"""
        if self.is_streaming:
            self.log_message("Cannot schedule: Already streaming.")
            return False
        
        self.scheduled_time = scheduled_time
        self.log_message(f"Stream scheduled for {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Calculate time difference in seconds
        now = datetime.now()
        time_diff = (scheduled_time - now).total_seconds()
        
        if time_diff <= 0:
            self.log_message("Scheduled time is in the past.")
            return False
        
        # Start a scheduler thread
        threading.Thread(
            target=self._schedule_timer,
            args=(time_diff,),
            daemon=True
        ).start()
        
        return True
    
    def _schedule_timer(self, delay_seconds):
        """Wait for the scheduled time and start streaming"""
        self.log_message(f"Waiting {delay_seconds:.1f} seconds for scheduled stream")
        
        # Sleep until scheduled time
        time.sleep(delay_seconds)
        
        # Check if streaming was canceled
        if not hasattr(self, 'scheduled_time') or self.scheduled_time is None:
            self.log_message("Scheduled stream was canceled.")
            return
        
        # Reset scheduled time
        self.scheduled_time = None
        
        # Start streaming if video path and stream key are set
        if hasattr(self, 'video_path') and hasattr(self, 'stream_key') and self.video_path and self.stream_key:
            config = {
                'is_shorts': self.is_shorts,
                'quality_preset': self.quality_preset,
                'bitrate': self.bitrate,
                'audio_bitrate': self.audio_bitrate
            }
            self.start_streaming(self.video_path, self.stream_key, config)
        else:
            self.log_message("Cannot start scheduled stream: Missing video or stream key.")
    
    def get_stream_duration(self):
        """Get current stream duration in seconds"""
        if not self.is_streaming or not self.start_time:
            return 0
        
        duration = (datetime.now() - self.start_time).total_seconds()
        return int(duration)
    
    def check_ffmpeg_installed(self):
        """Check if FFmpeg is installed and available"""
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