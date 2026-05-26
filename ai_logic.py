import os
from google import genai
from google.genai import types

# Yeh line automatic tumhaari key uthayegi bina code mein dikhaye
api_key = os.environ.get("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

select_model = "gemini-2.5-flash"

system_instruction = (
    "You are a medical jargon translator for patients. "
    "Analyze the uploaded image/document AND the patient's question together. "
    "Translate complex terms into simple words. Do not diagnose. "
    "Be funny and engaging in your explanations. Use emojis to make it more relatable. "
    "Be candid and honest about the limitations of the AI. Always include a disclaimer at the end of your response. "
    "Use the language used by the patient in their question to respond. "
)

def translate_medical_jargon(user_text, file_path):
    content_list = [system_instruction]

    if user_text.strip():
        content_list.append(f"Patient Question: {user_text}")

    if file_path.strip():
        if os.path.exists(file_path):
            with open(file_path, "rb") as f:
                file_bytes = f.read()

            media_part = types.Part.from_bytes(
                mime_type="image/png",
                data=file_bytes
            )
            content_list.append(media_part)

    try:
        response = client.models.generate_content(
            model=select_model,
            contents=content_list,
        )
        return response.text

    except Exception as e:
        return f"Error processing the request: {str(e)}"
    
    
    
    

    
    
    
    
   

    
          


    
    
    
    
    
    
    
    
