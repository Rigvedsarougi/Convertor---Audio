import os
from pydub import AudioSegment

def convert_audio(input_file, output_format):
    input_format = input_file.split('.')[-1].lower()
    output_file = f"converted.{output_format}"
    
    audio = AudioSegment.from_file(input_file, format=input_format)
    audio.export(output_file, format=output_format)
    
    return output_file
