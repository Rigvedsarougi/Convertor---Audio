# converter.py

import os
from io import BytesIO
from pydub import AudioSegment

def convert_audio(uploaded_file, output_format):
    input_format = uploaded_file.name.split('.')[-1].lower()
    output_file = f"converted.{output_format}"
    
    with BytesIO(uploaded_file.read()) as audio_bytes:
        audio = AudioSegment.from_file(audio_bytes, format=input_format)
        audio.export(output_file, format=output_format)
    
    return output_file
