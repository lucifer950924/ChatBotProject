from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_core.runnables import RunnablePassthrough
import os , asyncio , tracemalloc
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName


os.environ['OPENAI_API_KEY'] = decryptSecretByName('RAGChatBot_deepseek')
os.environ['OPENAI_API_BASE'] = 'https://api.deepseek.com'
tracemalloc.start()

prompt_generator_model = OllamaLLM(
    model = 'llama3:latest',
    temperature = 0.5,
    verbosity = True

)

response_generator_model = ChatOllama(
    model = 'llama3:latest',
    temperature = 0.5,
    verbosity = True
)

async def get_context(topic:str = '') -> str:
    prompt_template = ChatPromptTemplate.from_messages([
        ('system',f''' You will generate context regarding the {topic},
        Rule:
        1. Generate more than one context for {topic}
        2. Always stick to the topic
        3. Assume the role of a {topic} expert        

        Output :
        Return the context of the topic as a string
    '''),
    ('human','''
        Your Contexts are :''')
    ])

    chain = ({'question':RunnablePassthrough()} | prompt_template | prompt_generator_model)
    response = chain.invoke(topic)
    
        
    
    return response


async def generate_prompt_by_context(context:str):
    
    prompt_template = ChatPromptTemplate.from_messages([
        ('system',f'You assume the role of an expert in {context}. Rule: 1. Generate a list of Prompts to get the important points on the topic , Rule 2: Do not hallucinate regarding the context Rule 3: Return a python list of 5 prompts'),
        ('human','Your prompts are: ')

    ])

    chain= ({'question':RunnablePassthrough()} | prompt_template | prompt_generator_model)

    prompts = chain.invoke(context)
    

    return prompts

async def generate_response(prompts:str):
    prompt_template = ChatPromptTemplate.from_messages([
        ('system',f'Rate the prompts in {prompts} Rule: 1. Take the best prompt 2. Generate a paragraph within 300 words with all important events'),
        ('human','Your discussion on the topis is:')
    ])
    
    chain = ({'question': RunnablePassthrough()} | prompt_template |response_generator_model)
    response = chain.invoke(prompts)    
    return response





async def main():
    context = await get_context(input('Enter the Topic: '))
    prompts = await generate_prompt_by_context(context)
    response = await generate_response(prompts)
    print(response.content)



if __name__ == '__main__':

    asyncio.run(main())
        





