import requests
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName as decN


deep_seek_key = decN("RAGChatBot_deepseek")

url = "https://api.deepseek.com/v1/models"
headers = {
    "Authorization": f"Bearer {deep_seek_key}"
}

print(requests.get(url, headers=headers).status_code)
