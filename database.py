# database.py
import streamlit as st
import sqlite3
import os
from utils import delete_image_from_db
from utils import override_env_file
from utils import exchange_auth_code_for_token
from utils import get_auth_url

#---------------------------------------------------------------------------------------------------
# Function declaration
#---------------------------------------------------------------------------------------------------

# Function to display database content
def display_images_table():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM images")
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        st.write("### Table: Images")
        st.write("Showing all entries:")
        for row in rows:
            st.write(row)
    else:
        st.info("No entries found in the database.")

def get_refresh_token():
    # Add "Get Refresh Token" section
    st.subheader("Dropbox Authorization")
    st.write("Use this button to authenticate and retrieve a new Dropbox refresh token.")

    app_key = os.getenv("DROPBOX_APP_KEY")
    app_secret = os.getenv("DROPBOX_APP_SECRET")

    # Check for session state variables
    if "oauth_in_progress" not in st.session_state:
        st.session_state["oauth_in_progress"] = False
    if "auth_code" not in st.session_state:
        st.session_state["auth_code"] = None

    if not st.session_state["oauth_in_progress"]:
        # Start the OAuth process
        if st.button("Get Auth Code"):
            if app_key:
                # Begin OAuth process
                st.session_state["oauth_in_progress"] = True
                get_auth_url(app_key)
            else:
                st.error("Missing DROPBOX_APP_KEY or DROPBOX_APP_SECRET in environment variables.")
    else:
        st.write("oauth_in_progress is True and this is else statement block")
        # Handle after redirect
        auth_code = st.query_params["code"]

        if auth_code:
            st.session_state["auth_code"] = auth_code
            st.success(f"Authorization code detected: {auth_code}")

            # Exchange code for tokens
            refresh_token = exchange_auth_code_for_token(app_key, app_secret, auth_code)
            if refresh_token:
                st.success("Refresh token successfully retrieved!")
                st.session_state["oauth_in_progress"] = False
        else:
            st.warning("Redirected back, but no authorization code detected. Please try again.")

#---------------------------------------------------------------------------------------------------
# Streamlit app
#---------------------------------------------------------------------------------------------------

# Page content
st.title("Database Viewer")
st.write("This page displays the `images` table and allows you to delete specific entries.")

# Display database content
display_images_table()

# Image deletion form
st.write("---")
image_to_delete = st.text_input("Enter Image Name to Delete")
if st.button("Delete Image"):
    if image_to_delete.strip():
        success = delete_image_from_db(image_to_delete)
        if success:
            st.success(f"Image '{image_to_delete}' deleted successfully!")
        else:
            st.error(f"Error: Could not find or delete image '{image_to_delete}'.")
    else:
        st.error("Please enter a valid image name.")

# Get refresh token section
st.write("---")
get_refresh_token()

# Get app key and secret
app_key = os.getenv("DROPBOX_APP_KEY")
app_secret = os.getenv("DROPBOX_APP_SECRET")

# Update refresh_token with given auth_code
st.write("---")
auth_code = st.text_input("Enter the authorization code:")
if st.button("Update Refresh Token") and auth_code:
    exchange_auth_code_for_token(app_key, app_secret, auth_code)

# Show environment variables
st.write("---")
if st.button("Show Environment Variables"):
    st.write({
        "DROPBOX_ACCESS_TOKEN": os.getenv("DROPBOX_ACCESS_TOKEN"),
        "DROPBOX_REFRESH_TOKEN": os.getenv("DROPBOX_REFRESH_TOKEN"),
        "DROPBOX_APP_KEY": os.getenv("DROPBOX_APP_KEY"),
        "DROPBOX_APP_SECRET": os.getenv("DROPBOX_APP_SECRET"),
    })

# Override .env file
st.write("---")
if st.button("Override Environment Variables"):
    try:
        st.write("Overriding environment variables...")
        override_env_file()
        st.write("Environment variables succesfully overriden.")
    except Exception as e:
        st.error(f"Error overriding environment variables: {e}")

# Restart the app
st.write("---")
if st.button("Restart App"):
    try:
        st.write("Restarting app...")
        st.rerun()
    except Exception as e:
        st.error(f"Error restarting app: {e}")