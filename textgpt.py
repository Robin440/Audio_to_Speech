
import openai

import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to your audio file
audio_file_path = '66de8c6bb7fe369d2e3c2f33-REC-2850.mp3'

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    with open(file_path, 'rb') as audio_file:
        response = openai.audio.transcriptions.create(
            model='whisper-1',
            file=audio_file,
            response_format='text'  # Requesting text format directly
        )
        
        # Print raw response to inspect its structure
        print("Raw response:", response)
        
        # Since the response is text directly, just return it
        return response

# Transcribe the audio and print the result
transcribed_text = transcribe_audio(audio_file_path)
print("Transcribed Text:\n", transcribed_text)
