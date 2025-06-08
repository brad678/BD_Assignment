# 🧠 Agentic RAG with LangGraph + Azure OpenAI

This project implements a **simplified Agentic Retrieval-Augmented Generation (RAG)** system using:
- **LangGraph** for building self-critiquing LLM pipelines,
- **Azure OpenAI** (`gpt-4o` or `gpt-4`) for LLM and embeddings,
- **Chroma** for fast semantic search and persistent vector storage.

---

## 🚀 Features

- 🔍 Vector-based retrieval from a local knowledge base
- 💬 LLM-generated answers with citation support
- 🧠 Self-critiquing mechanism to detect gaps
- 🔁 Optional answer refinement step based on critique
- 🌐 REST API using Flask (`/rag` endpoint)

---

## 🗂 Project Structure

```

agentic_RAG_with_langgraph/
├── app.py                     # Flask API for the RAG pipeline
├── agentic_rag_simplified.py # LangGraph pipeline & nodes
├── index_kb.py                # Embedding & Chroma vector DB logic
├── prompts.py                 # Prompt templates for LLM
├── self_critique_loop_dataset.json # Local KB (software best practices)
├── requirements.txt
└── chroma_db/                 # Auto-created persistent Chroma store

````

---

## ⚙️ Setup Instructions

### 1. 🔐 Create `.env` file

```env
AZURE_OPENAI_API_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o  # or your actual deployment name
````

### 2. 📦 Install dependencies

```bash
pip install -r requirements.txt
```

### 3. 📚 Index Knowledge Base

```bash
python -m agentic_RAG_with_langgraph.index_kb
```

This will:

* Embed all entries from `self_critique_loop_dataset.json`
* Store them into a persistent Chroma vector DB at `./chroma_db/`

### 4. 🧪 Run Flask API

```bash
python -m agentic_RAG_with_langgraph.app
```

---

## 📡 API Usage

### POST `/rag`

#### Request:

```json
{
  "question": "What are best practices for caching?"
}
```

#### Response:

```json
{
  "answer": "Start with read-through caching, invalidate on writes, and use versioned keys. [KB003] [KB013]"
}
```

---

## 🧪 Testing Tips

* Use `curl`:

```bash
curl -X POST http://localhost:5000/rag \
     -H "Content-Type: application/json" \
     -d '{"question": "What are best practices for caching?"}'
```

* Or use Postman / Insomnia

---

## ✅ Sample Questions to Try

* What are best practices for caching?
* How should I set up CI/CD pipelines?
* What should I consider for error handling?
* How do I version my APIs?

---

## 🧠 Tech Stack

* [LangGraph](https://github.com/langchain-ai/langgraph)
* [Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
* [ChromaDB](https://www.trychroma.com/)
* [Flask](https://flask.palletsprojects.com/)

---

## 📄 License

MIT License

```
