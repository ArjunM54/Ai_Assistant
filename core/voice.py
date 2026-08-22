from streamlit_mic_recorder import mic_recorder
from google import genai
from dotenv import load_dotenv
import pyttsx3
import os


load_dotenv()


client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def record_voice():

    audio = mic_recorder(
        start_prompt="🎤 Start Recording",
        stop_prompt="⏹ Stop Recording",
        just_once=True,
        use_container_width=True,
        format="wav",
        key="voice_recorder"
    )

    return audio


def speech_to_text(audio_bytes):

    if not audio_bytes:
        return ""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            {
                "inline_data": {
                    "mime_type": "audio/wav",
                    "data": audio_bytes
                }
            },
            """
            Transcribe this audio into text.

            Rules:
            - Return only the spoken words.
            - Do not explain anything.
            - Do not add extra text.
            - Preserve the meaning of the speaker.
            """
        ]
    )

    return response.text.strip()

def text_to_speech(text):

    if not text:
        return None

    engine = pyttsx3.init()

    engine.setProperty("rate", 170)
    engine.setProperty("volume", 1.0)

    output_file = "audio/response.wav"

    os.makedirs("audio", exist_ok=True)

    engine.save_to_file(
        text,
        output_file
    )

    engine.runAndWait()

    return output_file