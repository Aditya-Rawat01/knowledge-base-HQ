# AI Assistant with Long-Term Memory (Mem0 + Qdrant + Groq)

This project implements an intelligent assistant that utilizes **Mem0** for long-term memory management, **Qdrant** as a vector database for storage, **Ollama** for local embeddings, and **Groq** for high-speed LLM inference.

## 🚀 Features
- **Persistent Memory:** Remembers user preferences and past interactions across sessions.
- **Local Embeddings:** Uses `nomic-embed-text` via Ollama for privacy and cost-efficiency.
- **High Performance:** Leverages Groq's API for near-instant LLM responses.
- **Vector Search:** Uses Qdrant for efficient semantic retrieval of relevant memories.

## 🛠️ Prerequisites

Ensure you have the following installed and running:

1.  **Python 3.10+**
2.  **Docker** (to run Qdrant and Ollama)
3.  **Ollama**: Pull the embedding model:
    ```bash
    ollama pull nomic-embed-text
    ```
4.  **Qdrant**: Run via Docker:
    ```bash
    docker run -p 6333:6333 qdrant/qdrant
    ```

## 📦 Installation

1. Clone this repository or copy the script.
2. Install the required Python packages:
    ```bash
    uv add mem0ai qdrant-client openai python-dotenv
    ```

## ⚙️ Configuration

Create a `.env` file in the root directory and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here