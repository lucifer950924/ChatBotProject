def ruleBasedChatBot(userInput="continue"):
    while userInput == "continue":
        userInput = str(input("You: "))
        if userInput.lower() == "hi":
            print("Bot: Hello, Iam your Chatbot")
            userInput = "continue"
        elif "my name is" in userInput.lower():
            userName =  userInput.split("My Name is".lower())[-1].strip()
            print("Bot: Hello, " + f"{userName}" + " How are you today?")
            userInput = "continue"
        elif userInput.lower() == "i am fine":
            print("Bot: How can I help?")
            userInput = "continue"
        elif userInput.lower() == "quit":
            print("Bot: GoodBye")
            break



    
if __name__ == "__main__":
    ruleBasedChatBot()    