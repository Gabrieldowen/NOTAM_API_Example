import google.generativeai as genai
from credentials import GEMINI_API_KEY
        
def callGemini(untranslated):
    # set up model
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')

    # set up prompt
    prompt = "Translate the following NOTAM into plain language that someone who is not a pilot could understand. Do not include any newlines or special characters."
    response = model.generate_content(prompt +  untranslated)
    
    return response.text

