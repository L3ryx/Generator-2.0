from openai import OpenAI
import os

API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY)

def test_api():
    try:
        response = client.models.list()
        return "✅ API Connectée avec succès !"
    except Exception as e:
        return f"❌ Erreur API : {str(e)}"
