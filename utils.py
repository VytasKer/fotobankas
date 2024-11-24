# Import libraries
import streamlit as st
import json
import sqlite3
import dropbox
import os
import requests
from dotenv import set_key, load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_auth_url(app_key):
    """
    Displays the Dropbox authorization URL and sets the app to wait for the auth code.
    """
    redirect_uri = "http://localhost:8501/database"
    auth_url = (
        f"https://www.dropbox.com/oauth2/authorize"
        f"?client_id={app_key}"
        f"&token_access_type=offline"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
    )

    st.write(f"1. Visit this URL to authorize the app: [Authorize App]({auth_url})")
    st.write("After authorization, you'll be redirected back here. Please wait.")

def exchange_auth_code_for_token(app_key, app_secret, auth_code):
    """
    Exchanges the authorization code for a refresh token.
    """
    token_url = "https://api.dropboxapi.com/oauth2/token"
    redirect_uri = "http://localhost:8501/database"
    payload = {
        "code": auth_code,
        "grant_type": "authorization_code",
        "client_id": app_key,
        "client_secret": app_secret,
        "redirect_uri": redirect_uri,
    }

    try:
        response = requests.post(token_url, data=payload)
        response_data = response.json()

        # Display response for debugging
        st.write(response_data)

        # Extract and save the refresh token
        if "refresh_token" in response_data:
            refresh_token = response_data["refresh_token"]

            # Test
            st.write(f"Refresh token: {refresh_token}")

            # Save refresh token locally
            if os.path.exists(".env"):
                load_dotenv()
                set_key(".env", "DROPBOX_REFRESH_TOKEN", refresh_token)
                st.write("Refresh token saved to .env file.")
            else:
                st.write(f"Refresh token: {refresh_token}")

            return refresh_token
        else:
            st.error(f"Error: {response_data.get('error_description', 'Unknown error')}")
            return None

    except Exception as e:
        st.error(f"Error during token exchange: {e}")
        return None

def initialize_dropbox_client():
    """
    Initializes the Dropbox client and refreshes the access token if needed.
    Returns:
        dropbox.Dropbox: The Dropbox client instance.
    Raises:
        ValueError: If the access token or refresh token is not found.
    """
    # Reload .env dynamically to fetch the latest variables
    override_env_file()
    
    access_token = os.getenv("DROPBOX_ACCESS_TOKEN")
    refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")
    app_key = os.getenv("DROPBOX_APP_KEY")
    app_secret = os.getenv("DROPBOX_APP_SECRET")

    if not all([access_token, refresh_token, app_key, app_secret]):
        raise ValueError(
            "Missing Dropbox credentials. Please set the 'DROPBOX_ACCESS_TOKEN', 'DROPBOX_REFRESH_TOKEN', "
            "'DROPBOX_APP_KEY', and 'DROPBOX_APP_SECRET' environment variables."
        )

    dbx = dropbox.Dropbox(
        oauth2_access_token=access_token,
        oauth2_refresh_token=refresh_token,
        app_key=app_key,
        app_secret=app_secret,
    )

    try:
        # Refresh the token if necessary
        dbx.check_and_refresh_access_token()

        # Update the refreshed access token in .env or environment variables
        new_access_token = dbx._oauth2_access_token

        if os.path.exists(".env"):
            set_key(".env", "DROPBOX_ACCESS_TOKEN", new_access_token)
        else:
            os.environ["DROPBOX_ACCESS_TOKEN"] = new_access_token
        
    except Exception as e:
        raise ValueError(f"Failed to refresh Dropbox access token: {e}")

    return dbx

def override_env_file():
    # Reload .env dynamically to fetch the latest variables
    if os.path.exists(".env"):
        load_dotenv(override=True)

def load_translations(file_path="translations.json"):
    """
    Load translations from a JSON file.

    Args:
        file_path (str): Path to the translations JSON file.
    
    Returns:
        dict: Translations dictionary.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            dropbox_path TEXT,
            thumbnail_url TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Add image metadata to the database
def add_image_to_db(name, dropbox_path, thumbnail_url):
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO images (name, dropbox_path, thumbnail_url)
        VALUES (?, ?, ?)
    ''', (name, dropbox_path, thumbnail_url))
    conn.commit()
    conn.close()

# Fetch all images from the database
def fetch_images_from_db():
    conn = sqlite3.connect("gallery.db")
    cursor = conn.cursor()
    cursor.execute('SELECT name, thumbnail_url FROM images')
    images = cursor.fetchall()
    conn.close()
    return images

def delete_image_from_db(image_name):
    """
    Deletes a specific entry from the 'images' table in gallery.db based on the image name.
    Returns True if deletion was successful, otherwise False.
    """
    try:
        conn = sqlite3.connect("gallery.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM images WHERE name = ?", (image_name,))
        conn.commit()
        conn.close()
        return cursor.rowcount > 0  # Returns True if a row was deleted
    except Exception as e:
        print(f"Error deleting image: {e}")
        return False

# Initialize the database
# init_db()