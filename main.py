# Import libraries
import streamlit as st
import streamlit.components.v1 as components
import dropbox
from utils import load_translations
from utils import add_image_to_db
from utils import initialize_dropbox_client

#---------------------------------------------------------------------------------------------------
# Function declaration
#---------------------------------------------------------------------------------------------------

# Translation helper
def t(key):
    return translations[language][key]

# Function to upload image to Dropbox
def upload_image_to_dropbox():
    # Select one image from computer
    uploaded_file = st.file_uploader(t("upload_image"), type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        st.write(t("image_selected"))
        st.image(uploaded_file, caption=t("selected_image"), use_container_width=True)
        st.write(t("please_confirm_selection"))
    
    if uploaded_file is not None:
        # Define dropbox upload path
        dropbox_path = f"/Uploaded_Images/{uploaded_file.name}"

    # Confirm the selection of image
    if uploaded_file is not None:
        if st.button(t("confirm_selection")):
            file_data = uploaded_file.read()
            # Upload image to Dropbox
            try:
                dbx.files_upload(file_data, dropbox_path, mode=dropbox.files.WriteMode('overwrite'))
                st.write(t("upload_success"))
                try:
                    # Get and save thumbnail
                    save_thumbnail(uploaded_file.name)
                except Exception as e:
                    st.error(f"Error generating thumbnail: {e}")
            except Exception as e:
                st.error(f"Error uploading image to Dropbox: {e}")

def save_thumbnail(image_name):
    dropbox_path = f"/Uploaded_Images/{image_name}"
    try:
        # Generate thumbnail (raw bytes)
        thumbnail_result = dbx.files_get_thumbnail_v2(dropbox.files.PathOrLink.path(dropbox_path), size=dropbox.files.ThumbnailSize.w640h480)

        # Extract the raw thumbnail bytes from the response (2nd item in tuple)
        thumbnail_bytes = thumbnail_result[1].content

        # Build thumbnail file name
        thumbnail_file_name = f"{image_name.rsplit('.', 1)[0]}_thumb.jpg"

        # Save thumbnail locally (example) or serve via your app
        with open(f"thumbnails/{thumbnail_file_name}", "wb") as f:
            f.write(thumbnail_bytes)

        # Optionally, store the thumbnail path or data in the DB
        thumbnail_local_path = f"thumbnails/{thumbnail_file_name}"
        add_image_to_db(image_name, dropbox_path, thumbnail_local_path)
        st.success("Thumbnail generated and stored!")
    except Exception as e:
        st.error(f"Error generating thumbnail: {e}")

def upload_button():
    st.session_state.clicked = True

def thumbnail_button():
    st.session_state.clicked_thumbnail = True

#---------------------------------------------------------------------------------------------------
# Streamlit app
#---------------------------------------------------------------------------------------------------

# Dropbox Python API Documentation https://dropbox-sdk-python.readthedocs.io/en/latest/
# Initialize Dropbox API
try:
    dbx = initialize_dropbox_client()
except ValueError as e:
    st.error(f"Error initializing Dropbox API: {e}")

# Language selection
language = st.sidebar.radio(
    "🌐 Select Language / Pasirinkite kalbą:", ("en", "lt")
)

# Load translations
translations = load_translations()

# Webpage title
st.title(t("main_page"))

# Webpage description
st.write(t("welcome_main"))

# Button to upload image
st.button("Upload Image", on_click=upload_button)

# Upload button session state
if 'clicked' not in st.session_state:
    st.session_state.clicked = False

if st.session_state.clicked:
    upload_image_to_dropbox()

# Button to show thumbnail
st.write("---")
st.button("Get test thumbnail", on_click=thumbnail_button)

# Thumbnail button session state
if 'clicked_thumbnail' not in st.session_state:
    st.session_state.clicked_thumbnail = False

if st.session_state.clicked_thumbnail:
    save_thumbnail("autumn-lithuania.jpg")