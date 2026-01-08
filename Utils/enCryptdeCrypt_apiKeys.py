from cryptography.fernet import Fernet
import os

def encryptSecretByName(name: str,secret: str):
    key = Fernet.generate_key()
    filename = f"{name}.key"
    keyfilename = f"{name}_key.txt"
    currDir = os.getcwd()
    dirSecret = os.path.join(currDir,"Data",f"{name}")
    os.makedirs(dirSecret,exist_ok=True)
    filepath = os.path.join(dirSecret,filename)
    keyfilepath = os.path.join(dirSecret,keyfilename)
    with open(filepath,"wb") as file:
        file.write(key)
    with open(filepath,"rb") as file:
        key = file.read()
    fernet = Fernet(key)
    encryptedSecret = fernet.encrypt(secret.encode())
    with open(filepath,"wb") as file:
        file.write(encryptedSecret)
    with open(keyfilepath,"wb") as file:
        file.write(key)
    
def decryptSecretByName(name:str):
    filename = f"{name}.key"
    keyfileName = f"{name}_key.txt"
    currDir = os.getcwd()
    dirSecret = os.path.join(currDir,"Data",f"{name}")
    filepath = os.path.join(dirSecret,filename)
    keyfilepath = os.path.join(dirSecret,keyfileName)
    if not os.path.exists(filepath):
        print("Secret does not exist")
    else:
        with open(keyfilepath,"rb") as file:
            key = file.read()
        fernet = Fernet(key)
        with open(filepath,"rb") as file:
            encryptedSecret = file.read()
        try:
            decryptedSecret = fernet.decrypt(encryptedSecret).decode()    
        except Exception as e:
            print("Unable to decrypt secret")
    return decryptedSecret




