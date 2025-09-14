from openai import OpenAI
import os


client = OpenAI(api_key="sk-abcdqrstefgh5678abcdqrstefgh5678abcdqrst")


chat_history = [
    {"role": "system", "content": "You are a friendly AI assistant."}
]

while True:
    userInput = input("You: ")
    if userInput.lower() == "quit":
        break

    chat_history.append({"role": "system", "content": userInput})

    response = client.chat.completions.create( model="gpt-5-nano",
        messages=chat_history,
        temperature=0.7,
        max_tokens=500)
    
    reply = response.choices[0].message.content.strip()

    print(f"Bot: {reply}")

    chat_history.append({"role": "system", "content": reply})