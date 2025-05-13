import streamlit as st

def apply_custom_styles():
    """Apply custom CSS styles to the Streamlit app"""
    
    # CSS for light and dark themes with transitions
    st.markdown(
        """
        <style>
        /* Global Variables */
        :root {
            --primary-color: #4361ee;
            --secondary-color: #3a0ca3;
            --accent-color: #7209b7;
            --success-color: #06d6a0;
            --warning-color: #ffd166;
            --error-color: #ef476f;
            --background-color: #f8f9fa;
            --card-background: #ffffff;
            --text-color: #212529;
            --text-secondary: #6c757d;
            --border-color: #e9ecef;
            --shadow-color: rgba(0, 0, 0, 0.05);
            --font-main: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        [data-theme="dark"] {
            --primary-color: #4cc9f0;
            --secondary-color: #4361ee;
            --accent-color: #7209b7;
            --success-color: #06d6a0;
            --warning-color: #ffd166;
            --error-color: #ef476f;
            --background-color: #1f1f1f;
            --card-background: #2d2d2d;
            --text-color: #f8f9fa;
            --text-secondary: #adb5bd;
            --border-color: #495057;
            --shadow-color: rgba(0, 0, 0, 0.2);
        }
        
        /* Base Styles */
        body {
            font-family: var(--font-main);
            background-color: var(--background-color);
            color: var(--text-color);
            transition: background-color 0.3s ease, color 0.3s ease;
        }
        
        /* Header Styling */
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 0;
            margin-bottom: 1.5rem;
            border-bottom: 1px solid var(--border-color);
        }
        
        .logo-container {
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .logo-icon {
            font-size: 1.75rem;
            animation: pulse 2s infinite ease-in-out;
        }
        
        .logo-text {
            font-size: 1.5rem;
            font-weight: 700;
            letter-spacing: 0.5px;
        }
        
        .highlight {
            color: var(--primary-color);
        }
        
        .theme-toggle {
            cursor: pointer;
            font-size: 1.25rem;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background-color: var(--card-background);
            box-shadow: 0 2px 5px var(--shadow-color);
            transition: all 0.3s ease;
        }
        
        .theme-toggle:hover {
            transform: scale(1.1);
        }
        
        /* Sidebar Styling */
        .sidebar-header {
            margin-bottom: 1.5rem;
        }
        
        .sidebar-title {
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--primary-color);
        }
        
        .sidebar-divider {
            height: 1px;
            background-color: var(--border-color);
            margin: 1.5rem 0;
        }
        
        .status-indicator {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 0.75rem;
        }
        
        .status-label, .duration-label {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }
        
        .status-value {
            font-weight: 600;
        }
        
        .status-active {
            color: var(--success-color);
            animation: pulse 2s infinite;
        }
        
        .duration-indicator {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        
        .duration-value {
            font-weight: 600;
            font-family: monospace;
        }
        
        .app-info {
            margin-top: 2rem;
            padding: 1rem;
            background-color: var(--card-background);
            border-radius: 0.5rem;
            box-shadow: 0 2px 5px var(--shadow-color);
        }
        
        .info-title {
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        
        .info-text {
            font-size: 0.9rem;
            margin-bottom: 0.75rem;
            color: var(--text-secondary);
        }
        
        .app-version {
            font-size: 0.8rem;
            color: var(--text-secondary);
        }
        
        /* Section Styling */
        .section-title {
            display: flex;
            align-items: center;
            margin-bottom: 1rem;
            gap: 0.5rem;
        }
        
        .section-title span {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--primary-color);
        }
        
        /* Control Buttons Styling */
        .control-buttons {
            margin-top: 1.5rem;
        }
        
        /* Log Container Styling */
        .log-container {
            height: 300px;
            overflow-y: auto;
            background-color: var(--card-background);
            border-radius: 0.5rem;
            padding: 0.5rem;
            border: 1px solid var(--border-color);
            margin-top: 1rem;
        }
        
        .log-container pre {
            margin: 0;
            color: var(--text-color);
            font-family: 'Courier New', monospace;
            font-size: 0.85rem;
            line-height: 1.5;
        }
        
        /* Duration Display */
        .duration-display, .countdown-display {
            display: flex;
            flex-direction: column;
            align-items: center;
            margin: 1rem 0;
            padding: 1rem;
            background-color: var(--card-background);
            border-radius: 0.5rem;
            box-shadow: 0 2px 5px var(--shadow-color);
        }
        
        .duration-timer, .countdown-timer {
            font-size: 2rem;
            font-weight: 700;
            font-family: monospace;
            color: var(--primary-color);
            margin-top: 0.5rem;
        }
        
        /* Dashboard Styling */
        .dashboard-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .dashboard-title {
            font-size: 1.75rem;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 0.25rem;
        }
        
        .dashboard-subtitle {
            font-size: 1rem;
            color: var(--text-secondary);
        }
        
        .metric-card {
            display: flex;
            align-items: center;
            padding: 1.25rem;
            background-color: var(--card-background);
            border-radius: 0.5rem;
            box-shadow: 0 2px 5px var(--shadow-color);
            margin-bottom: 1rem;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 10px var(--shadow-color);
        }
        
        .metric-icon {
            font-size: 1.75rem;
            margin-right: 1rem;
            color: var(--primary-color);
        }
        
        .metric-info {
            flex: 1;
        }
        
        .metric-title {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-bottom: 0.25rem;
        }
        
        .metric-value {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }
        
        .metric-change {
            font-size: 0.85rem;
            font-weight: 600;
        }
        
        .text-green-500 {
            color: var(--success-color);
        }
        
        .text-red-500 {
            color: var(--error-color);
        }
        
        /* Footer Styling */
        .footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-color);
        }
        
        .footer-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }
        
        .footer-text {
            font-size: 0.9rem;
            color: var(--text-secondary);
        }
        
        .footer-links {
            display: flex;
            gap: 1.5rem;
        }
        
        .footer-link {
            color: var(--primary-color);
            text-decoration: none;
            font-size: 0.9rem;
            transition: color 0.2s ease;
        }
        
        .footer-link:hover {
            color: var(--accent-color);
            text-decoration: underline;
        }
        
        /* Animations */
        @keyframes pulse {
            0% {
                opacity: 1;
            }
            50% {
                opacity: 0.6;
            }
            100% {
                opacity: 1;
            }
        }
        
        /* Theme Toggle Script */
        </style>
        
        <script>
            function toggleTheme() {
                const body = document.body;
                const icon = document.getElementById('theme-icon');
                
                if (body.getAttribute('data-theme') === 'dark') {
                    body.removeAttribute('data-theme');
                    icon.textContent = '🌙';
                    localStorage.setItem('theme', 'light');
                } else {
                    body.setAttribute('data-theme', 'dark');
                    icon.textContent = '☀️';
                    localStorage.setItem('theme', 'dark');
                }
            }
            
            // Apply saved theme on load
            document.addEventListener('DOMContentLoaded', () => {
                const savedTheme = localStorage.getItem('theme');
                const icon = document.getElementById('theme-icon');
                
                if (savedTheme === 'dark') {
                    document.body.setAttribute('data-theme', 'dark');
                    if (icon) icon.textContent = '☀️';
                } else {
                    if (icon) icon.textContent = '🌙';
                }
            });
        </script>
        """,
        unsafe_allow_html=True
    )