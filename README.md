## Dependencies

- Python 3.9+
- ollama (https://ollama.com) with a pulled model: `ollama pull mistral`

To install Python dependencies:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

4. start the server - ollama serve (pull and download ollama if needed)
5. do ingestion to the db - python -m ingest.ingest_docs -> check if it is successfull
6. in a separate terminal run main
7. make your query - if it is in knowledge base app will use that, if not - it will do general web search
