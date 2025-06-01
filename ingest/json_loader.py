import json
from langchain_core.documents import Document
def load_json_documents(path: str):
    with open(path, 'r', encoding='utf-8') as file:
      data = json.load(file)
    
    documents = []
    for entry in data:
        content = f"Q: {entry['question']}\nA: {entry['answer']}"
        metadata = {"id": entry["id"]}
        documents.append(Document(page_content=content, metadata=metadata))
    
    return documents
