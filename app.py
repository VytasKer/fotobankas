import streamlit as st

pg = st.navigation([
    st.Page("main.py"),
    st.Page("gallery.py"),
    st.Page("database.py")])
pg.run()