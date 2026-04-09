import os
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName as dn

def setEnvironVariable(model: str):
    '''
    Sets the environvent Variable for the API Key based on the provided model name.
    Args:
        model (str): The name of the model for which the API key is to be set. Supported values are 'llama' and 'groq'
    '''
    model_Name = {
        'llama' : ['RAGChatBot_deepseek','OPENAI_API_KEY'],
        'groq' : ['GroqAPI','GROQ_API_KEY']
    }

    if model.lower() in model_Name.keys():
        secrets_name = model_Name[model.lower()]
        os.environ[secrets_name[-1]] = dn(secrets_name[0])

    if model.lower() == 'llama':
        os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'

    

