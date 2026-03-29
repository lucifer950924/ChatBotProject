from sentence_transformers import SentenceTransformer, util
import nltk, json
from Utils.context_generation_tool import context_generator




class Metrics:
    def __init__(self):
        self.metrics = {}
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('tokenizers/punkt_tab')
        except:
            nltk.download('punkt')
            nltk.download('punkt_tab')
            
    def _tokenize_text(self,text):
        return nltk.sent_tokenize(text)


    
    def _calculate_faithfulness(self,answer:str,question:str,threshold:float):
        '''
        Calculates the faithfulness of the system
        Args:
            answer: Takes the AI generated answer
            question: Takes the User question in str
            threshold: Takes the threshold score

        Returns:
            the calculated faithfulness metrics in str
        '''
        
        context = context_generator(question)
        
        statements = self._tokenize_text(answer)
        context_chunks = self._tokenize_text(context)
        supported = 0
        context_embed = self.model.encode(context_chunks)

        for statement in statements:
            stmt_embed = self.model.encode(statement)
            similarity = util.cos_sim(stmt_embed,context_embed)

            score = similarity.max().item()

            if score >= threshold:
                supported += 1

        faithfulness = supported / len(statements) if statements else 0

        self.metrics['faithfulness'] = faithfulness

        return str(self.metrics['faithfulness'])
    
    
    def _calculate_answer_relevance(self,answer:str,question:str):
        '''
        Calculates the Answer Relevance of the system
        Args:
            answer: Takes the AI generated answer
            question: Takes the User question in str

        Returns:
            the calculated Answer Relevance metrics in str
        '''
        
        question_tokens = self._tokenize_text(question)
        answer_tokens = self._tokenize_text(answer)

        q_embed = self.model.encode(question_tokens)
        
        
        for ans in answer_tokens:
            a_embed = self.model.encode(ans)
            similarity = util.cos_sim(a_embed,q_embed)
            score = similarity.max().item()

        self.metrics['answer_relevance'] = score

        return str(self.metrics['answer_relevance'])
    
            
            
