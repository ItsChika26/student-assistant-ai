from typing import Any, Dict
from langchain.chains import RetrievalQA
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.llms import Ollama
import logging

logger = logging.getLogger(__name__)

def load_vector_db():
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
    return db

def load_llm():
    return Ollama(model="llama3.2")

def build_rag_chain():
    db = load_vector_db()
    llm = load_llm()
    search = DuckDuckGoSearchRun()
    rag_chain = RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())
    
    # Updated web search prompt to be more specific
    web_search_prompt = PromptTemplate(
        input_variables=["query", "search_results"],
        template="""Question: {query}
Search Results: {search_results}
Please provide a concise answer based on the search results above."""
    )
    web_chain = web_search_prompt | llm
    
    def enhanced_query(query: str) -> str:
        try:
            # Try knowledge base first
            rag_response = rag_chain.invoke({"query": query})
            if rag_response and rag_response["result"].strip() and "don't know" not in rag_response["result"].lower():
                return f"From knowledge base: {rag_response['result']}"
            
            # Fallback to web search
            search_results = search.run(query)
            web_response = web_chain.invoke({
                "query": query,
                "search_results": search_results
            })
            return f"From web search: {web_response}"
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            return f"Error: {str(e)}"
    
    return enhanced_query

def main():
    try:
        query_chain = build_rag_chain()
        print("Enhanced RAG system is ready. Type your query below:")
        while True:
            query = input(">> ")
            if query.lower() in ["exit", "quit"]:
                print("\nExiting the RAG system.")
                break
            
            result = query_chain(query)  
            print(result)
            
    except KeyboardInterrupt:
        print("\nExiting the RAG system.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print("An error occurred. Please check the logs for details.")

if __name__ == "__main__":
    main()