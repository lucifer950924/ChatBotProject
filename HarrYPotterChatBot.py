import chatBOT as cb


def AskRAG(userPrompt: str):
    chunks = cb.splitTheKnowledgeBase()
    retriever = cb.EmbedTheChunks(chunks)
    response = cb.RAGChatbot(userPrompt,retriever)

    return response

