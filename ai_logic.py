import os
from dotenv import load_dotenv
import google.generativeai as genai
from groq import Groq

# .env file se keys load karne ke liye
load_dotenv()

# Dono API keys ko environment variables se nikalna
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
GROQ_KEY = os.getenv("GROQ_API_KEY")

# Engines ko initialize karna
if GEMINI_KEY:
    genai.configure(api_key=GEMINI_KEY)

if GROQ_KEY:
    groq_client = Groq(api_key=GROQ_KEY)

def decode_medical_report(image_data, user_prompt=None):
    """
    Yeh function report ko decode karega. 
    Agar Gemini fail hota hai, toh Groq backup par chalega!
    """
    
    # AI ke liye ekdam solid aur friendly system prompt
    system_instruction = """
    You are an expert Medical Report Decoder AI. Your job is to simplify complex medical jargon, 
    lab reports, and prescriptions into easy-to-understand language for a common layman.
    
    Guidelines:
    1. Be highly empathetic, supportive, and friendly. Use relatable emojis.
    2. Break down heavy medical terms into simple explanations.
    3. Keep your tone light, clear, and comforting to reduce patient anxiety.
    4. ALWAYS add a professional medical disclaimer at the very end stating you are an AI, not a doctor.
    """

    final_prompt = user_prompt if user_prompt else "Please decode this medical report and simplify it for me."
    
    # ---------------------------------------------------------
    # ENGINE 1: GOOGLE GEMINI (Primary Engine)
    # ---------------------------------------------------------
    try:
        print("⚡ Attempting to decode using Gemini 2.5 Flash...")
        
        # Gemini 2.5 Flash model setup
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        
        # Agar image provide ki gayi hai
        if image_data:
            # image_data streamlit se bytes ke roop mein aayega
            image_parts = [{"mime_type": "image/jpeg", "data": image_data}]
            response = model.generate_content([final_prompt, image_parts[0]])
        else:
            response = model.generate_content(final_prompt)
            
        return response.text

    # ---------------------------------------------------------
    # ENGINE 2: GROQ LLAMA 3 (Backup Engine - If Gemini Fails)
    # ---------------------------------------------------------
    except Exception as gemini_error:
        print(f"⚠️ Gemini Failed with error: {gemini_error}")
        print("🚀 Switching to Backup Engine: Groq (Llama 3)...")
        
        if not GROQ_KEY:
            return "❌ Error: Gemini failed and Groq API Key is missing in .env file!"

        try:
            # Groq Client se Llama 3 call karna
            # Note: Groq text-based analysis karega agar Gemini ka image parser fail hota hai
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    {"role": "user", "content": f"{final_prompt}\n[Context: Image extraction failed, analyzing provided text/queries]"}
                ],
                model="llama3-8b-8192", # Ekdam superfast Llama 3 model
            )
            
            groq_response = chat_completion.choices[0].message.content
            # User ko batane ke liye ki backup engine chal raha hai
            return f"⚠️ *Note: Gemini server is currently busy. Response generated via Backup Engine (Llama 3).*\n\n{groq_response}"
            
        except Exception as groq_error:
            return f"😭 Absolute Crash! Gemini and Groq both failed. Error: {groq_error}"
            
        
    
    
    
    

    
    
    
    
   

    
          


    
    
    
    
    
    
    
    
