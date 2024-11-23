# Import libraries
import streamlit as st
import streamlit.components.v1 as components
import dropbox
from utils import load_translations
from utils import fetch_images_from_db
import tempfile
import sqlite3

#---------------------------------------------------------------------------------------------------
# Function declaration
#---------------------------------------------------------------------------------------------------

# Translation helper
def t(key):
    return translations[language][key]

def download_full_image(name):
    try:
        # Retrieve Dropbox path from DB
        conn = sqlite3.connect("gallery.db")
        cursor = conn.cursor()
        cursor.execute('SELECT dropbox_path FROM images WHERE name = ?', (name,))
        result = cursor.fetchone()
        conn.close()

        if result:
            dropbox_path = result[0]

            # Download the full-resolution image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                dbx.files_download_to_file(temp_file.name, dropbox_path)
                temp_file_path = temp_file.name

            # Provide download button
            with open(temp_file_path, "rb") as file:
                st.download_button(
                    label="Download Full Image",
                    data=file,
                    file_name=name,
                    mime="image/jpeg",
                )
        else:
            st.error("Image not found!")
    except Exception as e:
        st.error(f"Error downloading image: {e}")

# Render gallery with thumbnails
def render_gallery():
    images = fetch_images_from_db()  # Fetch images from DB
    num_columns = 3  # Number of columns in the grid

    # Create grid layout
    for i in range(0, len(images), num_columns):
        cols = st.columns(num_columns)
        for col, (name, thumbnail_url) in zip(cols, images[i:i+num_columns]):
            with col:
                st.image(thumbnail_url, caption=name, use_container_width=True)
                # Optionally add a download button for the full image
                if st.button(f"Download {name}"):
                    download_full_image(name)

def download_button():
    st.session_state.clicked = True

#---------------------------------------------------------------------------------------------------
# Streamlit app
#---------------------------------------------------------------------------------------------------

# Initialize Dropbox API
dbx = dropbox.Dropbox('sl.CBTP7svIzxil2Q8GidrldnbAmxtHoSnz758pL0xNCScDG6ngReVZHAC2XtHXHLC7VH4IG4jmtVHjcqUSuKwTObSQHPHeFVMsrBgrG78wvF13ccfZmSW01IBeV8eE0EmQxIeoVLQtjKFk')

# Language selection
language = st.sidebar.radio(
    "🌐 Select Language / Pasirinkite kalbą:", ("en", "lt")
)

# Load translations
translations = load_translations()

# Page content
st.title(t("gallery_page"))

# Webpage description
st.write(t("welcome_gallery"))

# Call render_gallery in the gallery page
render_gallery()