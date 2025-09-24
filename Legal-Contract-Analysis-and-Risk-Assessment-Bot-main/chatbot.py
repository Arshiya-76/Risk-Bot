# chatbot.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def get_chat_response(query: str, chat_history: list, contract_text: str, language: str = 'en'):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return "Chatbot Error: Google API key not found. Please check your .env file."
    
    genai.configure(api_key=api_key)
    
    lang_map = {'en': 'English', 'hi': 'Hindi'}
    lang_name = lang_map.get(language, "English")

    system_prompt = f"""
    You are a helpful AI assistant for an Indian SMB owner. Your task is to answer questions about the legal contract provided below.

    **CRITICAL RULES:**
    1. Base your answers primarily on the text of the contract provided.
    2. If a question is about a legal term or concept mentioned in the contract (e.g., 'Companies Act, 1956'), but not explained in detail, you may use your external knowledge to provide a concise and relevant explanation.
    3. If a question is entirely irrelevant to the contract or asks for information not mentioned, you MUST state: "That information is not available in the document."
    4. Respond to the user in {lang_name}.

    **Full Contract Text:**
    ---
    {contract_text}
    ---
    """
    
    model = genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        system_instruction=system_prompt
    )

    gemini_history = []
    for message in chat_history:
        role = "model" if message["role"] == "assistant" else "user"
        gemini_history.append({"role": role, "parts": [message["content"]]})

    try:
        chat = model.start_chat(history=gemini_history)
        response = chat.send_message(query)
        return response.text
    except Exception as e:
        return f"Sorry, an error occurred: {e}"