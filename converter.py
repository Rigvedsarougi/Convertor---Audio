import os
import tempfile
from pydub import AudioSegment

def convert_audio(input_file, output_format):
    input_format = input_file.split('.')[-1].lower()
    output_file = f"converted.{output_format}"
    
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(input_file.read())
        temp_file_path = temp_file.name
    
    audio = AudioSegment.from_file(temp_file_path, format=input_format)
    audio.export(output_file, format=output_format)
    
    os.unlink(temp_file_path)  # Delete the temporary file
    
    return output_file
