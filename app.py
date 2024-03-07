import os
import whisper
import streamlit as st
from pydub import AudioSegment
import pandas as pd

st.set_page_config(
    page_title="Whisper based ASR",
    page_icon="musical_note",
    layout="wide",
    initial_sidebar_state="auto",
)

audio_tags = {'comments': 'Converted using pydub!'}

upload_path = "uploads/"
download_path = "downloads/"
transcript_path = "transcripts/"

fraud_keywords = [
    'Class after token payment',
    'Upfront Payment',
    'Bootcamp',
    'Token amount is refundable',
    'Get server after 50 percent of total fee',
    'Job guarantee',
    '100% placement guarantee',
    'Personal account',
    'Refund',
    'S4 Hana',
    'Server Access',
    'Free classes',
    'Free',
    'Free Days',
    'Free trial',
    'Trial classes',
    'My account',
    'First month free',
    'Free services',
    'cancellation policy',
    'Cancel'
]


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

def process_audio(filename, model_type):
    model = whisper.load_model(model_type)
    result = model.transcribe(filename)
    return result["text"]

def save_transcript(transcript_data, txt_file):
    with open(os.path.join(transcript_path, txt_file), "w") as f:
        f.write(transcript_data)

st.title("Automatic Speech Recognition")
st.info('Supports Audio formats - WAV, MP3, MP4, OGG, WMA, AAC, FLAC, FLV')
uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "ogg", "wma", "aac", "flac", "mp4", "flv"])

audio_file = None

if uploaded_file is not None:
    audio_bytes = uploaded_file.read()
    with open(os.path.join(upload_path, uploaded_file.name), "wb") as f:
        f.write((uploaded_file).getbuffer())
    with st.spinner(f"Processing Audio"):
        output_audio_file = uploaded_file.name.split('.')[0] + '.mp3'
        output_audio_file = to_mp3(uploaded_file, output_audio_file, upload_path, download_path)
        audio_file = open(os.path.join(download_path, output_audio_file), 'rb')
        audio_bytes = audio_file.read()
    print("Opening ", audio_file)
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("Feel free to play your uploaded audio file")
        st.audio(audio_bytes)
    with col2:
        whisper_model_type = st.radio("Please choose your model type", ('Tiny', 'Base', 'Small', 'Medium', 'Large'))

    if st.button("Generate Transcript"):
        with st.spinner(f"Generating Transcript"):
            transcript = process_audio(str(os.path.abspath(os.path.join(download_path, output_audio_file))),
                                       whisper_model_type.lower())

            output_txt_file = str(output_audio_file.split('.')[0] + ".txt")

            save_transcript(transcript, output_txt_file)
            output_file = open(os.path.join(transcript_path, output_txt_file), "r")
            output_file_data = output_file.read()

            # Fraud detection
            detected_keywords = [keyword for keyword in fraud_keywords if keyword.lower() in output_file_data.lower()]
            fraud_detected = len(detected_keywords) > 0

            output_df = pd.DataFrame({
                'Uploaded File Name': [uploaded_file.name],
                'Output File Data': [output_file_data],
                'Detected Keywords': [detected_keywords],
                'Fraud Detected': [fraud_detected]
            })

        if st.download_button(
                label="Download Transcript",
                data=output_file_data,
                file_name=output_txt_file,
                mime='text/plain'
        ):
            st.balloons()
            st.success(' Download Successful ')

else:
    st.warning(' Please upload your audio file ')

# Display the result dataframe
if 'output_df' in locals():
    st.subheader("Fraud Detection Result:")
    st.write(output_df)

st.markdown(
    "<br><hr><center>Made by <a href='mailto:rigved.sarougi@henryharvin.com?subject=ASR Whisper WebApp!&body=Please specify the issue you are facing with the app.'><strong>Rigved Sarougi</strong><hr>",
    unsafe_allow_html=True)
