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
audio_tags = {'comments': 'Converted using pydub!'}

def to_mp3(audio_file, output_audio_file, upload_path, download_path):
    if audio_file.name.split('.')[-1].lower() == "wav":
        audio_data = AudioSegment.from_wav(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower() == "mp3":
        audio_data = AudioSegment.from_mp3(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower() == "ogg":
        audio_data = AudioSegment.from_ogg(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower() == "wma":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name), "wma")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower() == "aac":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name), "aac")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower() == "flac":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name), "flac")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower() == "flv":
        audio_data = AudioSegment.from_flv(os.path.join(upload_path, audio_file.name))
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)

    elif audio_file.name.split('.')[-1].lower() == "mp4":
        audio_data = AudioSegment.from_file(os.path.join(upload_path, audio_file.name), "mp4")
        audio_data.export(os.path.join(download_path, output_audio_file), format="mp3", tags=audio_tags)
    return output_audio_file

def convert_audio(audio_file, output_format):
    if output_format.lower() == "mp3":
        st.warning("Please select a different output format. MP3 is already selected.")
        return None
    
    audio_data = AudioSegment.from_mp3(audio_file)
    output_audio_file = audio_file.split('.')[0] + f'.{output_format}'
    output_file_path = os.path.join(download_path, output_audio_file)
    audio_data.export(output_file_path, format=output_format)
    return output_file_path

st.title("MP3 Converter")
st.info("This app converts MP3 audio files to other formats.")

uploaded_file = st.file_uploader("Upload MP3 audio file", type=["mp3"])

if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.audio(audio_bytes, format='audio/mp3')
    output_format = st.selectbox("Select output format", ["wav", "ogg", "wma", "aac", "flac", "mp3"])
    
    if st.button("Convert"):
        with st.spinner("Converting..."):
            if output_format.lower() == "mp3":
                output_audio_file = to_mp3(uploaded_file, uploaded_file.name, upload_path, download_path)
            else:
                output_audio_file = convert_audio(os.path.join(upload_path, uploaded_file.name), output_format)
            
            if output_audio_file:
                output_file_path = os.path.join(download_path, output_audio_file)
                st.audio(open(output_file_path, 'rb').read(), format=f'audio/{output_format}', label='Download Converted Audio')
                st.success(f"Conversion successful! You can download the converted audio file.")
else:
    st.warning("Please upload an MP3 audio file.")
