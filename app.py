import streamlit as st
import subprocess
import sys

# List of required packages
required_packages = ["streamlit", "dropbox", "sqlite-utils", "python-dotenv"]

# Install missing packages
for package in required_packages:
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

pg = st.navigation([
    st.Page("main.py"),
    st.Page("gallery.py"),
    st.Page("database.py")])
pg.run()