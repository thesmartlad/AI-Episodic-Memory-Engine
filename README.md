# AI-Episodic-Memory-Engine


```markdown
# AI Episodic Memory Engine

A local, hybrid memory architecture that equips Large Language Models (LLMs) with both short-term transactional memory and long-term semantic episodic retrieval. Built to run locally on consumer hardware using Ollama, SQLite, and ChromaDB.

## 🚀 Architecture Overview

This project implements a dual-layer memory management framework for local AI assistants, mimicking human memory consolidation:

1. **Short-Term Memory (STM):** Managed via **SQLite** (`chat_history.db`). It logs raw, chronological conversation steps line-by-line and feeds the immediate context window.
2. **Long-Term Episodic Memory (LTM):** Managed via **ChromaDB** (`chroma_data/`). Every 15 messages, a background worker consolidates and condenses the raw conversation chunk into a semantic fact snapshot using local embeddings, allowing global associative recall across different chat sessions.

```text
       +-------------------------------------------------+
       |                  User Prompt                    |
       +-------------------------------------------------+
                                |
        +-----------------------+-----------------------+
        |                                               |
        v                                               v
+---------------+                               +---------------+
|  SQLite DB    |                               |   ChromaDB    |
| (Short-Term)  |                               |  (Long-Term)  |
+---------------+                               +---------------+
        |                                               |
  Last 5 Turns                                     Vector Search
   Sequential                                       Semantic Facts
        |                                               |
        +-----------------------+-----------------------+
                                |
                                v
                   +-------------------------+
                   |  Context-Injected LLM   |
                   |       (Qwen 2.5)        |
                   +-------------------------+

```

## 🛠️ Tech Stack

* **LLM Engine:** [Ollama](https://ollama.com/) running `qwen2.5:1.5b` (Inference) and `nomic-embed-text` (Vector Embeddings)
* **Structured DB:** SQLite 3 (Lightweight transactional tracking)
* **Vector DB:** ChromaDB (Persistent local vector storage)
* **Language:** Python 3.14+

## 📁 Project Structure

```text
AI_Memory_Project/
│
├── main.py              # Application orchestrator & dynamic session loop
├── memory_engine.py     # Global vector retrieval and background text consolidation
├── database.py          # Database initializers (SQLite schema & Chroma persistent client)
├── ollama_client.py     # Local API communication endpoints for embeddings & chat
├── showcase.py          # Diagnostic tool generating terminal backend status reports
├── .gitignore           # Keeps database binaries out of version control
└── README.md            # Project documentation

```

## ⚙️ Core Logic Flow

1. **Dynamic Session Selection:** On startup, `main.py` requests a Session ID. Starting a new ID wipes the short-term context window while keeping long-term memory intact via global vector matching.
2. **Global Vector Injection:** Every prompt triggers a global semantic search across ChromaDB collections. Matching memories are formatted straight into the `system` instructions before inference, bypassing session restrictions.
3. **Chunk Consolidation:** When a session's interaction history hits a multiple of 15 records (`msg_count % 15 == 0`), a consolidation prompt condenses the raw text chunk into a 1-2 sentence declarative summary, generates its vector embedding, and commits it asynchronously to ChromaDB.

## 💻 Setup & Installation

### Prerequisite: Ollama Configurations

Ensure Ollama is running locally and you have pulled the required models:

```bash
ollama pull qwen2.5:1.5b
ollama pull nomic-embed-text

```

### Execution

Run the primary conversational entry point:

```bash
python main.py

```

To run a deep-dive backend structural diagnostic showing stored SQLite rows and semantic Chroma summaries:

```bash
python showcase.py

```

```

```
