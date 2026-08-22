import os
from dotenv import load_dotenv
from google import genai
from PIL import Image
import pyttsx3

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def ask_gemini(messages):

    conversation = ""

    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=conversation
    )

    return response.text

def ask_gemini_stream(messages):

    conversation = ""

    for msg in messages:
        conversation += f"{msg['role']}: {msg['content']}\n"

    stream = client.models.generate_content_stream(
        model="gemini-3.5-flash-lite",
        contents=conversation
    )

    return stream

def ask_pdf(question, context):

    prompt = f"""
        You are Gima Ai, a helpful AI assistant.

        Instructions:

        - Answer ONLY using the provided context.
        - Do not use outside knowledge.
        - Use bullet points whenever appropriate.
        - If the user says explain in simple words, Explain as if teaching a beginner.
        - Give a short answer,Answer in 2 to 3 sentences.
        - If the answer is not available in the context, reply:
        "I couldn't find that information in the uploaded document."
        - Keep answers clear and concise.
        - If the question asks for a definition, provide a short definition first, then explain.
        - If the context contains multiple relevant sections, combine them into one coherent answer.
        - Never invent facts.

        Context:
        {context}

        Question:
        {question}

        Answer :
        """

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt
    )

    return response.text

def ask_image(image_path, prompt):

    if not prompt:
        return "Please enter a question about the image."

    image = Image.open(image_path)

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=[
            prompt,
            image
        ]
    )

    return response.text

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