import os
import streamlit as st
from pydub import AudioSegment

st.set_page_config(
    page_title="MP3 Converter",
    page_icon="musical_note",
    layout="wide",
    initial_sidebar_state="auto",
)

upload_path = "uploads/"
download_path = "downloads/"

def convert_audio(audio_file, output_format):
    audio_data = AudioSegment.from_mp3(audio_file)
    output_audio_file = audio_file.split('.')[0] + f'.{output_format}'
    audio_data.export(os.path.join(download_path, output_audio_file), format=output_format)
    return output_audio_file

st.title("MP3 Converter")
st.info("This app converts MP3 audio files to other formats.")

uploaded_file = st.file_uploader("Upload MP3 audio file", type=["mp3"])

if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(audio_bytes, format='audio/mp3')
    output_format = st.selectbox("Select output format", ["wav", "ogg", "wma", "aac", "flac"])
    
    if st.button("Convert"):
        with st.spinner("Converting..."):
            output_audio_file = convert_audio(os.path.join(upload_path, uploaded_file.name), output_format)
            output_file_path = os.path.join(download_path, output_audio_file)
            st.audio(open(output_file_path, 'rb').read(), format=f'audio/{output_format}', label='Download Converted Audio')
            st.success(f"Conversion successful! You can download the converted audio file.")
else:
    st.warning("Please upload an MP3 audio file.")

