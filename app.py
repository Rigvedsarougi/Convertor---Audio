# app.py

import os
import whisper
import streamlit as st
import pandas as pd
from converter import convert_audio   # Importing the convert_audio function

st.set_page_config(
    page_title="Audio File Converter",
    layout="wide",
    initial_sidebar_state="auto",
)

st.title("Audio File Converter")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "ogg", "wma", "aac", "flac", "mp4", "flv"])
output_format = st.selectbox("Select output format", ["mp3", "wav", "ogg", "wma", "aac", "flac"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/' + uploaded_file.type.split('/')[-1])
    
    if st.button("Convert"):
        with st.spinner("Converting..."):
            output_file = convert_audio(uploaded_file.name, output_format)  # Pass the file name instead of the uploaded_file object
        
        st.success(f"Conversion complete. Download your converted file [here](output_file).")
