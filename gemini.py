import openai
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the API key from the environment
openai.api_key = os.getenv("OPENAI_API_KEY")

# Path to your audio file
audio_file_path = '66db51b15a3029a0fc9bc5b6-REC-2844.mp3'

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    try:
        with open(file_path, 'rb') as audio_file:
            response = openai.audio.transcriptions.create(
                model='whisper-1',
                file=audio_file,
                response_format='text'  # Requesting text format directly
            )
            
            # Return the transcribed text
            return response if isinstance(response, str) else response.get('text')
    except Exception as e:
        print(f"An error occurred during transcription: {e}")
        return None

# Function to identify speakers and format conversation
def identify_speakers(transcribed_text):
    if not transcribed_text:
        print("No transcribed text available for speaker identification.")
        return None

    prompt = (
        "The following is a transcription of a conversation between multiple speakers. "
        "Identify each speaker and format the text as a dialogue with speaker labels.\n\n"
        "Transcribed Text:\n"
        f"{transcribed_text}\n\n"
        "Formatted Conversation:"
    )

    try:
        response = openai.chat.completions.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are an assistant that can identify speakers in a conversation and format the text with speaker labels."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,  # Adjust based on the length of your transcribed text
            temperature=0.5,
        )

        # Access the first message choice's content in the completion response
        formatted_conversation = response.choices[0].message.content.strip()
        return formatted_conversation
    except Exception as e:
        print(f"An error occurred during speaker identification: {e}")
        return None

# Main execution
if __name__ == "__main__":
    # Step 1: Transcribe the audio
    transcribed_text = transcribe_audio(audio_file_path)
    
    if transcribed_text:
        print("Transcribed Text:\n")
        print(transcribed_text)
    else:
        print("Failed to transcribe audio.")
        exit(1)
    
    # Step 2: Identify speakers and format conversation
    formatted_conversation = identify_speakers(transcribed_text)
    
    if formatted_conversation:
        print("\nFormatted Conversation:\n")
        print(formatted_conversation)
    else:
        print("Failed to identify speakers.")
