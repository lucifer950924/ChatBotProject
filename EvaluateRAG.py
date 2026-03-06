from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric,AnswerRelevancyMetric,ContextualPrecisionMetric,ContextualRelevancyMetric
from ragas import evaluate
from ragas.metrics.collections import Faithfulness,AnswerRelevancy,ContextPrecision,ContextRecall
from langchain_community.embeddings import HuggingFaceEmbeddings
from ragas.llms import LangchainLLMWrapper
from langchain_groq import ChatGroq
from datasets import Dataset
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
from Utils.jsonreader import readconifgJson
from Utils.logger_file import setUpLogger
from langchain_ollama import OllamaLLM
import os
# from AskRAGAboutPdf import AskRAGaboutPdf

logger = setUpLogger()

def evalRAGDeepEval(func):
    def wrapper(args:str):
        out , retriever = func(args)
        contexts = retriever.invoke(args)
        testcase = LLMTestCase(
        input= args,
        actual_output= out,
        expected_output=f'The name {args} is present in the SIR 2026 list',
        retrieval_context = [doc.page_content for doc in contexts]
        )
        score = evaluate([testcase],metrics=[FaithfulnessMetric(),AnswerRelevancyMetric(),ContextualPrecisionMetric(),ContextualRelevancyMetric()])
        print(score)
    
    return wrapper 

def evalRAGRAGAS(func):
    def wrapper(args:str):
        logger.info('Starting the RAG')
        out , retriever = func(args)
        logger.info('RAG executed')
        docs = retriever.invoke(args)
        logger.info('Retrieveing the docs')
        data = Dataset.from_dict(
            {
                'question': [args],
                'answer': [out],
                'contexts': [[doc.page_content for doc in docs]]
            }
        )
        logger.info(f'Creating the dataset {data}')
        os.environ['GROQ_API_KEY'] = decryptSecretByName('GroqAPI')

        
        evaluator = LangchainLLMWrapper(ChatGroq(model='meta-llama/llama-4-scout-17b-16e-instruct',
                              temperature = 0.1,
                              verbose = True))
        logger.info(f'setting up the llm {evaluator}')
        score_data = readconifgJson('metrics_config.json')['RAGAS']
        logger.info(f'Read the Thresold Score {score_data}')
        score = evaluate(dataset=data,metrics =[AnswerRelevancy(llm=evaluator,embeddings=HuggingFaceEmbeddings(model = 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')),ContextPrecision(),ContextRecall()],llm=evaluator)
        logger.info('Evaluation ended')
        logger.info(f'The score is: \n {score}')
        

    return wrapper



