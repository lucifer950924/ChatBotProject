from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import FaithfulnessMetric,AnswerRelevancyMetric,ContextualPrecisionMetric,ContextualRelevancyMetric
from ragas import evaluate
from ragas.metrics.collections import Faithfulness,AnswerRelevancy,ContextPrecision,ContextRecall
from groq import Groq
from datasets import Dataset
from Utils.enCryptdeCrypt_apiKeys import decryptSecretByName
# from AskRAGAboutPdf import AskRAGaboutPdf
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
        out , retriever = func(args)
        docs = retriever.invoke(args)
        data = Dataset.from_dict(
            {
                'question': [args],
                'answer': [out],
                'contexts': [[doc.page_content for doc in docs]]
            }
        )
        client = Groq(api_key=decryptSecretByName('GroqAPI'))
        evaluator = client.chat.completions.create(model = 'gemma2-9b-it')
        score = evaluate(dataset=data,metrics =[Faithfulness(),AnswerRelevancy(),ContextPrecision(),ContextRecall()],llm=evaluator)
        print(score)

    return wrapper



