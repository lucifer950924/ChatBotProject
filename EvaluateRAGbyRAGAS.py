from RAG import RAG
from datasets import Dataset
from ragas.llms import LangchainLLMWrapper
from langchain_ollama import OllamaLLM
from ragas.metrics import (
    faithfulness,
    answer_relevancy,
    context_precision,
    context_recall
)
from ragas import evaluate
evaluator_llm = LangchainLLMWrapper(OllamaLLM(model='phi3:mini'))

answer = RAG('Who is Harry Potter?')
data = Dataset.from_dict({
    'question': [answer['question']],
    'answer': [answer['answer']],
    'contexts': [answer['contexts']]
}
)

results = evaluate(
    dataset=data,
    metrics=[
        faithfulness,
        answer_relevancy,
        context_precision,
        context_recall
    ],
    llm = evaluator_llm
)


print(results)
