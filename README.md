# Cybersecurity Assessment Simulator
A full-stack application for interactive security assessment guidance, powered by FastAPI, Streamlit, and Ollama LLMs. This project provides a chatbot that helps users understand and navigate a security assessment template, with retrieval-augmented generation and section-aware responses.

## Features
1. FastAPI backend for chat and knowledge retrieval

2. Streamlit frontend for a modern, interactive UI

3. Ollama LLM integration for both chat and embeddings

4. ChromaDB vectorstore for document retrieval

5. Docker Compose for easy multi-service orchestration

## Requirements
Docker & Docker Compose (recommended)

(Optional) Python 3.10+ and pip for local development

## Quick Start (Recommended: Docker Compose)
Clone the repository:

`git clone <repo-url>`<br/>
`cd cybersecurity-assessment-final-version`<br/>

Start all services:<br/>
`docker compose up --build`

This will:

* Start the Ollama LLM server and pull required models (llama3.2, mxbai-embed-large)

* Start the FastAPI backend (http://localhost:8000)

* Start the Streamlit frontend (http://localhost:8501)

## Open the app:

Go to http://localhost:8501 in your browser.

The chatbot will guide you through security assessment sections and answer your questions.

## Environment Variables
1. OLLAMA_BASE_URL _(default: http://ollama:11434)_

2. BACKEND_URL _(default: http://backend:8000)_

These are set automatically in docker-compose.yml.

## Local Development (Optional)
Install Python dependencies:

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Start Ollama locally:

**Download and install from https://ollama.com/download**

**Pull required models:**
```
ollama pull llama3.2
ollama pull mxbai-embed-large
```

**Run the backend:**
`OLLAMA_BASE_URL=http://localhost:11434 fastapi dev backend/fastapi/api/main_app.py --host 0.0.0.0 --port 8000`

**Run the frontend:**
`BACKEND_URL=http://localhost:8000 streamlit run frontend/Start_Page.py`

### Project Structure
`backend/` - FastAPI app, LangGraph agents, vectorstore logic

`frontend/` - Streamlit UI

`docker-compose.yml` - Multi-service orchestration

`requirements.txt` - Python dependencies

`input_files/` - Security assessment template and docs

### Troubleshooting
Ollama connection errors:

* Ensure the backend can reach http://ollama:11434 (see README troubleshooting section)
* Make sure models are fully pulled before backend starts

* Model not found:
  * Double-check model names in `docker-compose.yml` and your code

* Frontend shows API 500 error:
    * Check backend logs for details


## Credits
* [Ollama](https://ollama.com/)
* [LangChain](https://www.langchain.com/)
* [ChromaDB](https://www.trychroma.com/)
* [Streamlit](https://streamlit.io/)
* [FastAPI](https://fastapi.tiangolo.com/)