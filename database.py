# database.py
import streamlit as st
import sqlite3
from utils import delete_image_from_db

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