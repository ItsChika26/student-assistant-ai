from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings


def load_vector_db():
    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
    return db

def load_llm():
    return Ollama(model="deepseek-r1:8b")

def build_rag_chain():

    db = load_vector_db()
    llm = load_llm()
    return RetrievalQA.from_chain_type(llm=llm, retriever=db.as_retriever())


def main():
    rag_chain = build_rag_chain()
    print("RAG system is ready. Type your query below:")
    while True:
        query = input(">> ")
        if query.lower() in ["exit", "quit"]:
            break
        result = rag_chain.run(query)
        print(result)

if __name__ == "__main__":
    main()
