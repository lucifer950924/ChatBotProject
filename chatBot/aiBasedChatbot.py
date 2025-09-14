from transformers import AutoModelForCausalLM,AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")


chatHistoryIds = None
while True:
    userInput = input("You: ")
    if userInput.lower() == "quit":
        break


    
    encodedInput = tokenizer(userInput + tokenizer.eos_token, return_tensors = 'pt')
    newInputIds = encodedInput["input_ids"]
    attentionMask = encodedInput["attention_mask"]


    botInputIds = torch.cat([chatHistoryIds,newInputIds],dim=-1) if chatHistoryIds is not None else newInputIds
    attentionMask = torch.ones(botInputIds.shape, device=botInputIds.device)
    chatHistoryIds = model.generate(botInputIds,max_length = 1000,attention_mask=attentionMask,pad_token_id = tokenizer.eos_token_id,do_sample=True,top_k=50,top_p=0.95,temperature=0.7)


    response = tokenizer.decode(chatHistoryIds[:,botInputIds.shape[-1]:][0],skip_special_tokens=True)

    print("Bot: ",response)