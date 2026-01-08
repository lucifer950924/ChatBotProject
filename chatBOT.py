from google import genai
import os
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName as decN
### Save the environment variables

api_key = decN("ChatBot001")

os.environ['GEMINI_API_KEY'] = api_key
### Setting up chat client
client = genai.Client()

respnse = client.models.generate_content(
    model = "gemini-3-pro-preview",
    contents= "who is US President?"
)
print(respnse.text)