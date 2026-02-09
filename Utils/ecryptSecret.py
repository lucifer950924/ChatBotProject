import enCryptdeCrypt_apiKeys as en

secretName = input("Enter filename :")
secret = input("Enter secret :")

en.encryptSecretByName(secretName,secret)