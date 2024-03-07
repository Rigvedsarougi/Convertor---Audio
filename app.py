import streamlit as st
from converter import convert_audio

st.title("Audio File Converter")

uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "ogg", "wma", "aac", "flac", "mp4", "flv"])
output_format = st.selectbox("Select output format", ["mp3", "wav", "ogg", "wma", "aac", "flac"])

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/' + uploaded_file.type.split('/')[-1])
    
    if st.button("Convert"):
        with st.spinner("Converting..."):
            output_file = convert_audio(uploaded_file, output_format)
        
        st.success(f"Conversion complete. Download your converted file [here](output_file).")
