import json
import sqlite3

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