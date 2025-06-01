from langchain.chains import RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama

def load_vector_db():
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    return Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)

def load_llm():
    return Ollama(model="llama3.2")

def build_rag_chain():
    db = load_vector_db()
    llm = load_llm()
    search = DuckDuckGoSearchRun()
    
    rag_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template=(
            "Answer in the same language and style as the question. "
            "Answer the question below using only the provided context. "
            "Do not mention the context or provide suggestions. "
            "Be direct and factual.\n\n"
            "Context:\n{context}\n\n"
            "Question: {question}\n"
            "Answer:"
        )
    )
        
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever(), chain_type_kwargs={"prompt": rag_prompt})
    
    web_search_prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template="""Question: {query}
Search Results: {search_results}
Please provide a concise answer based on the search results above."""
    )
    web_chain = web_search_prompt | llm
    
    def enhanced_query(query: str) -> str:
        try:
            rag_response = rag_chain.invoke({"query": query})
            answer = rag_response.get("result", "").strip()
            fallback_phrases = [
            "don't know", "not sure", "no information", "no context", "cannot answer",
            "i'm not sure", "i do not know", "no relevant information", "I cannot provide an answer",
            "I don't have enough information", "I cannot assist with that", "I couldn't find any information",
        ]
            if answer and all(phrase not in answer for phrase in fallback_phrases):
                return f"From knowledge base: {answer}"

            search_results = search.run(query)
            web_response = web_chain.invoke({
                "query": query,
                "search_results": search_results
            })
            return f"From web search: {web_response}"
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    return enhanced_query