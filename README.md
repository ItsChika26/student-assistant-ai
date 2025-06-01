# Student Assistant AI

## Overview

This application is a chatbot powered by LangChain and ChromaDB. It ingests knowledge base documents and provides answers based on the ingested data or performs general web searches when the information is not available in the knowledge base.

## Dependencies

- **Python**: Version 3.9 or higher.
- **Ollama**: Install Ollama from [https://ollama.com](https://ollama.com) and pull the required model:
  ```bash
  ollama pull llama3.2
  ```

## Installation

1. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Step 1: Start the Ollama server
Run the following command to start the Ollama server:
```bash
ollama serve
```

### Step 2: Ingest documents into the database
Run the ingestion script to process and store the knowledge base documents:
```bash
python -m ingest.ingest_docs
```
Check the logs to ensure the ingestion was successful.

### Step 3: Start the main application
In a separate terminal, run the main application:
```bash
python main.py
```

### Step 4: Make queries
You can now interact with the chatbot. If the query matches the knowledge base, the chatbot will use the ingested data. Otherwise, it will perform a general web search.

## Project Structure

```
student-assistant-ai/
├── ingest/
│   ├── __init__.py
│   ├── ingest_docs.py
│   ├── json_loader.py
├── data/
│   ├── food.json
│   ├── professors.json
├── chroma_db/
│   ├── chroma.sqlite3
│   ├── [other database files]
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
├── env/
│   ├── [virtual environment files]
└── __pycache__/
```

## Notes

- Ensure the `data/` directory contains valid `.json` files for ingestion.
- The `chroma_db/` directory will store the vector database files after ingestion.
- Use the `.gitignore` file to exclude unnecessary files from version control.
