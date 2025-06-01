import glob
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from .json_loader import load_json_documents
import logging

logger = logging.getLogger(__name__)
def ingest_documents():
    json_files = glob.glob('./data/**/*.json', recursive=True)
    docs=[]

    for json_file in json_files:
        try:
            file_docs = load_json_documents(json_file)
            docs.extend(file_docs)
        except Exception as e:
            logger.error(f"Error loading {json_file}: {e}")
            continue
    
    if not docs:
        logger.warning("No documents were loaded!")
        return

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embedding_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(chunks, embedding_model, persist_directory="./chroma_db")
    db.persist()
    logger.info("✅ Documents ingested and stored in vector DB")

if __name__ == "__main__":
    ingest_documents()
