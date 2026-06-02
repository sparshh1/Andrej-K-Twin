# 🧠 Andrej Karpathy Digital Twin

> A production-ready RAG-powered AI agent that emulates the voice, reasoning style, and technical depth of Andrej Karpathy — built for AIMS DTU Summer Project 2026.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-red?style=flat-square&logo=streamlit)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Local_Vectors-green?style=flat-square)
![Gemini](https://img.shields.io/badge/Gemini_2.5_Flash-LLM-orange?style=flat-square&logo=google)
![License](https://img.shields.io/badge/License-Academic_CO101-lightgrey?style=flat-square)

---

## 📌 What This Is

This project builds a **Digital Twin of Andrej Karpathy** — not just a chatbot that knows AI facts, but an agent that reasons, explains, and teaches the way Karpathy actually does: from first principles, deep into the math, with genuine enthusiasm for neural networks.

It is built on three pillars:

1. **RAG Pipeline** — Answers are grounded in Karpathy's actual blog posts and GitHub READMEs via a local ChromaDB vector store, so the agent cites real ideas instead of hallucinating.
2. **Conversation Memory** — Multi-turn memory within each session by passing full conversation history into every prompt.
3. **Persona Consistency** — A carefully engineered system prompt keeps the voice, values, and teaching style locked to Karpathy throughout every conversation.

---

## 🏗️ Architecture

```
[ User Query ]
      │
      ▼
┌──────────────┐    Local Semantic Search    ┌──────────────────────┐
│ retriever.py │ ──────────────────────────> │ Local ChromaDB       │
└──────────────┘                             │ (karpathy_corpus)    │
      │                                      │ all-MiniLM-L6-v2     │
      ◄──────────────────────────────────────┘
      │ (Query + Top-3 Matching Context Paragraphs)
      ▼
┌──────────────────────────────────────────────────────────────────┐
│  Dynamic Prompt Compiler                                         │
│  Persona Instructions + Retrieved Context + Conversation History │
└──────────────────────────────────────────────────────────────────┘
      │
      ▼
┌─────────────────┐    Retry with Backoff    ┌──────────────────────┐
│     app.py      │ ──────────────────────>  │ gemini-2.5-flash     │
│  (Streamlit UI) │ <──────────────────────  │ (with 503 retry)     │
└─────────────────┘      Response            └──────────────────────┘
```

### Component Breakdown

| Component | Responsibility | Stack |
|---|---|---|
| **Data Ingestion** | Scrapes Karpathy's blogs, chunks into ~800-char segments | BeautifulSoup4, LangChain Text Splitters |
| **Vector Storage** | On-device embeddings, persistent text index | ChromaDB + `all-MiniLM-L6-v2` |
| **Context Retrieval** | Semantic similarity search over corpus | ChromaDB query API |
| **UI — Landing Page** | Full biography, timeline, project showcase | Streamlit + custom HTML/CSS |
| **UI — Chat Page** | Multi-turn conversation with sidebar & RAG expander | Streamlit chat components |
| **Resilience** | Exponential backoff retry on Gemini 503 errors | Python `try/except` + `time.sleep` |

---

## 📂 Repository Structure

```
karpathy-digital-twin/
├── app.py                  # Main Streamlit app: landing page + chat UI + retry logic
├── src/
│   ├── ingest_blogs.py     # Web scraper + ChromaDB ingestion engine
│   └── retriever.py        # Semantic query module
├── chroma_db/              # Local vector database (auto-generated, git-ignored)
├── .env                    # API credentials (git-ignored)
├── .gitignore              # Blocks .env, chroma_db/, venv, __pycache__
└── README.md               # This file
```

---

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.10+
- A Google GenAI API key → [Get one at Google AI Studio](https://aistudio.google.com/app/apikey)

---

### Step 1 — Clone & Create Virtual Environment

```bash
git clone https://github.com/your-username/karpathy-digital-twin.git
cd karpathy-digital-twin

python3 -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows
```

### Step 2 — Install Dependencies

```bash
pip install streamlit google-genai chromadb requests beautifulsoup4 langchain-text-splitters python-dotenv
```

> ⚠️ **Important:** Use `google-genai` (the new SDK), **not** `google-generativeai`. If you have the old one installed, uninstall it first:
> ```bash
> pip uninstall google-generativeai google-genai -y
> pip install google-genai
> ```

### Step 3 — Configure API Key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_actual_google_genai_api_key_here
```

> 🔒 The `.gitignore` blocks this file from ever being committed. Never hardcode keys in source files.

### Step 4 — Build the Knowledge Base

```bash
python -m src.ingest_blogs
```

This scrapes Karpathy's blogs and GitHub READMEs, chunks the content into ~800-character segments, embeds them locally, and persists everything to `./chroma_db/`.

**Sources ingested:**
- `karpathy.github.io` — RNN Effectiveness, Recipe for Training NNs, State of Computer Vision, LeCun 1989, RL Pong, Breaking ConvNets, Feature Learning
- `github.com/karpathy` — nanoGPT README, micrograd README, minGPT README

> 🔁 To rebuild from scratch, delete `chroma_db/` and re-run this command.

### Step 5 — Launch the App

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

---

## 🚀 Features

### 🎨 Two-Page Frontend

**Landing Page** — A full dark-mode biography page featuring:
- Hero section with Karpathy's photo, key stats, and role description
- Vertical timeline of his career (1986 → 2023)
- Project showcase cards: nanoGPT, micrograd, Zero to Hero
- RAG trust banner showing which sources are active
- "Talk to Andrej" CTA button that transitions to the chat

**Chat Page** — A focused conversation interface with:
- Sticky header showing Karpathy's name and active status
- Sidebar with corpus status, turn counter, and clear button
- RAG expander showing exactly what was retrieved per message
- Avatar-tagged messages (`🧠` for Karpathy, `👤` for user)
- Back button to return to the landing page

### 🛡️ 503 Retry with Exponential Backoff

Gemini's free tier gets overloaded frequently. Instead of crashing, the app retries automatically:

```
Attempt 1 → wait 1s → Attempt 2 → wait 2s → Attempt 3 → wait 4s → Graceful error message
```

### 🧠 Multi-Turn Conversation Memory

Every request includes the full conversation history in the prompt, so Karpathy remembers what was discussed earlier in the session.

### 📄 RAG Source Transparency

Each response shows an expandable panel with the exact passages retrieved from ChromaDB — making it clear that answers are grounded in real writing, not hallucinated.

---

## 🧪 Core Code Reference

### Retriever (`src/retriever.py`)

```python
import chromadb

def get_relevant_context(query: str, n_results: int = 3) -> str:
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection("karpathy_corpus")

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if not results['documents'] or not results['documents'][0]:
        return ""

    return "\n\n---\n\n".join(results['documents'][0])
```

ChromaDB handles the embedding internally — no external API call needed for retrieval.

### Retry Helper (`app.py`)

```python
def call_gemini_with_retry(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if "503" in str(e) or "overloaded" in str(e).lower():
                wait = 2 ** attempt
                st.warning(f"Gemini overloaded. Retrying in {wait}s…")
                time.sleep(wait)
            else:
                return f"❌ API error: {e}"
    return "Gemini servers are too busy right now. Please try again in a minute."
```

---

## 🔐 Security Checklist

- [x] `.env` blocked from git via `.gitignore`
- [x] `chroma_db/` blocked from git (keeps repo clean)
- [x] No API keys hardcoded anywhere in source
- [x] All embedding computation runs locally (no data sent to external servers during retrieval)

---

## 📋 Evaluation Alignment

| Criterion | Implementation |
|---|---|
| **Persona consistency** | System prompt engineered with Karpathy's voice, vocabulary, and teaching patterns |
| **Technical accuracy** | RAG grounds every answer in actual blog content |
| **Memory quality** | Full conversation history injected into each prompt |
| **RAG quality** | Local ChromaDB with 10+ ingested sources; expander shows retrieved passages |
| **User experience** | Two-page Streamlit app with biography, timeline, and polished chat UI |

---

## 📜 License

Built for **AIMS DTU Summer Project 2026** under **CO101**. Scraping is limited to Karpathy's publicly available blog posts and GitHub READMEs, respecting the open-source intent of the original publications.

---

## 🙏 Acknowledgements

- [Andrej Karpathy](https://karpathy.ai/) for the extraordinary technical writing that makes this project possible
- [ChromaDB](https://www.trychroma.com/) for the simple, fast local vector store
- [Google GenAI / Gemini](https://ai.google.dev/) for the language model backend
- [LangChain](https://langchain.com/) for text splitting utilities
- [Streamlit](https://streamlit.io/) for the rapid UI framework
