# Fotobankas - # Streamlit Image Gallery with Dropbox Integration

This repository contains a Streamlit web application that allows users to upload images, view them in a gallery, and manage their metadata through integration with Dropbox and a local SQLite database. 

The project is designed to showcase the power of Streamlit for rapid app development combined with cloud storage for scalable image hosting.

---

## Features

- **Image Upload:** Upload images to Dropbox directly through the app.
- **Thumbnail Generation:** Automatically generate lower-resolution thumbnails for efficient gallery viewing.
- **Image Gallery:** View uploaded images and their thumbnails in a grid format.
- **Database Management:** Store metadata of uploaded images in a local SQLite database.
- **Admin Interface:** A separate page to view and manage database entries, including deleting specific records.

---

## Architecture

### Components

1. **Streamlit:** The framework for building the user interface.
2. **Dropbox API:** Used for uploading images and generating thumbnails.
3. **SQLite Database:** Local database for storing metadata (image name, paths, thumbnail URLs, etc.).
4. **Python Utilities:** Custom functions for database operations, API calls, and application logic.

### File Structure
- app.py          # Main application navigation
- main.py         # Image upload functionality
- gallery.py      # Image gallery page
- database.py     # Admin interface for database management
- utils.py        # Helper functions (e.g., database operations, API calls)
- gallery.db      # SQLite database for metadata (auto-created at runtime)
- thumbnails/     # Directory for locally stored thumbnails
- README.md       # Project documentation

## Current Testing Status

### Features Tested
- **Image Upload to Dropbox:** ✅
- **Thumbnail Generation:** ✅
- **Database Metadata Storage:** ✅
- **Gallery Display:** ✅
- **Database Management (View/Delete):** ✅

### Known Issues
- Thumbnail generation and storage need careful exception handling for edge cases.
- User interface could be further improved for error messages and feedback.

---

## How to Run

### Prerequisites
1. Python 3.8+
2. Required libraries (install via `pip install -r requirements.txt`):
   - `streamlit`
   - `dropbox`
   - `sqlite3` (built-in)
3. Dropbox API token (set as an environment variable: `DROPBOX_API_KEY`).

### Steps
1. Clone this repository:
   ```bash
   git clone <repository_url>
   cd <repository_directory>
