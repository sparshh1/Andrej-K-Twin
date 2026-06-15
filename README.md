# Andrej Karpathy Digital Twin

An ultra premium, brutalist, and high performance educational AI agent designed to replicate the technical depth, first principles reasoning philosophy, and distinct communication style of researcher Andrej Karpathy. The architecture leverages a decoupled **Dual-Engine / Hybrid-Cloud Blueprint**—combining a local knowledge retrieval base with an asynchronous intelligence layer.

---

## 🛠️ Project Architecture

```
                       +-----------------------------------+
                       |       app5.py (Streamlit UI)      |
                       +-----------------+-------+---------+
                                         |       ^
                User Input & UI Controls |       | SSE Token Stream
                                         v       |
                       +-----------------+-------+---------+
                       |      server.py (Flask Backend)    |
                       +--------+-----------------+--------+
                                |                 |
          Retrieve Top Chunks   |                 | Prompt + Memory Context
                                v                 v
        +-----------------------+-------+   +-----+------------------------+
        | src/retriever.py (Ensemble)   |   |   Gemini 2.5 Flash API       |
        +---+-----------------------+---+   +------------------------------+
            |                       |
            v (Semantic Search)     v (Sparse Match)
      [ChromaDB Index]         [BM25 Index]
  (all-MiniLM-L6-v2 Embeddings)

```

### 1. Ingestion & Preprocessing (`ingest.py`, `ingest_blogs.py`)

* **Multi-Modal Harvesting:** The data preprocessing pipeline automatically extracts unstructured text from two distinct public mediums: semantic HTML web scraping of Karpathy's core blog posts via `BeautifulSoup`, and raw textual subtitle extractions from his video lectures via the `YouTubeTranscriptApi`.
* **Recursive Chunking Strategy:** To feed the vector database safely, a custom chunking configuration breaks text into overlapping blocks utilizing a `RecursiveCharacterTextSplitter` configured to a strict **chunk size of 800 characters** and a **chunk overlap of 150 characters**. This guarantees that dense code blocks, mathematical expressions, and structural formatting don't get severed arbitrarily mid-thought, preventing context fragmentation.
* **Vector Indexing:** Text chunks are converted into numerical vector representations and stored in a persistent local instance of `ChromaDB`, allowing your knowledge retrieval layer to execute fully offline with sub-40ms CPU latency.

### 2. Intelligent Search Engine (`src/retriever.py`)

Instead of a basic vector database query, the system deploys a **Hybrid Ensemble Retrieval Pipeline**.

* **Semantic Search:** It instantiates a local HuggingFace embedding model (`all-MiniLM-L6-v2`) to perform semantic vector searches over the persistent database.
* **Sparse Match:** Concurrently, it runs a statistical keyword matcher via a sparse **BM25 algorithm**.
* **The Ensemble Merger:** By blending these two methods at an even **50/50 weight distribution**, the twin excels at broad conceptual inquiries (semantic alignment) while maintaining perfect precision for strict coding syntax, function names, and historical vocabulary like *micrograd* or *nanoGPT*.

### 3. Asynchronous Two-Tier Memory System

Cross session continuity is addressed without the massive overhead of an external relational database cluster by building an agile split memory pipeline running in parallel:

* **Short-Term Memory:** Tracks current active discussions within the session in real time via local transaction files mapped to a frontend-generated browser-side `uuid4` key string.
* **Long-Term Memory ("Self-Scrubbing Regex Engine"):** The server instructs the downstream LLM (Gemini 2.5 Flash) to analyze the chat turn and output discovered user facts inside structural tags. The backend uses a Python regular expression (`re.search`) to secretly scrape those facts into a permanent `global_memory.txt` ledger, stripping the metadata out before compiling the text stream for the UI.

### 4. Brutalist "Matrix" UX (`app5.py`)

* **Matrix Code Background:** Features an interactive canvas rendering a faint, animated stream of raw `Value` class backpropagation tensor math scrolling constantly in the background. It structurally integrates an explicit **amplitude scaling factor of 2.0** within the custom hardware normalization logic:

$$\text{self.data} = \text{self.data} \times 2.0$$


* **Dynamic Abstraction Toggle:** Includes a physical-style UI toggle layout switch shifting the persona instantly from accessible analogies ("ELI5") to heavy, underlying C/CUDA and matrix notation ("Under the Hood").
* **Technical Interface Elements:** Built-in dynamic text-scramble loading sequences, a contextual data sidebar showing real-time latency and token allocation metrics (capped at a 1M token context limit), and an interactive technical glossary that shows Karpathy’s specific definitions when hovering over complex deep learning terms.

---

## 🔬 Voice Synthesis Laboratory (Experimental Analysis)

The repository contains full architectural hooks for an integrated **Zero-Shot Voice Synthesis Pipeline** designed to provide real-time voice outputs synchronized with live text output:

* **The Layout:** An endpoint (`/api/audio/<chunk_id>`) maps incoming requests to an in-memory byte buffer storage object (`audio_store`) to coordinate wav binary playback via `io.BytesIO` without the latency of disk read/write cycles.
* **The Engineering Lessons:** The live audio components were bypassed at runtime due to three clear production barriers documented during empirical testing:
1. *Ngrok Tunnel Instability:* Persistent background socket terminations on free-tier compute instances killed the model process between test runs.
2. *Synthesis Latency:* Coqui XTTS v1 required ~25 seconds to generate speech on a standard T4 GPU, which brutally conflicted with the sub-100ms real-time token text stream of Gemini 2.5 Flash.
3. *Concurrency Conflict:* Streamlit's reactive rendering model (`st.rerun()`) created thread scheduling blocks when mixing raw binary media buffers with active text streams, resulting in session crashes.



---

## 📁 Repository Structure

```
├── .devcontainer/           # Development container configuration environments
├── memory/                  # JSON transaction histories and global profiles
│   └── [session_id].json    # Session-specific conversation contexts (e.g., fd626624...)
├── src/                     # Core backend Python pipeline logic
│   ├── ingest.py            # YouTube lecture transcript vectorizer
│   ├── ingest_blogs.py      # Blog element scraper and database builder
│   └── retriever.py         # Hybrid BM25 + Dense Vector Ensemble Engine
├── .env                     # Target Environment Keys (GEMINI_API_KEY)
├── .gitignore               # Git ignore rules for environment and DB protection
├── README.md                # Legacy project documentation
├── UPDATEDREADME.md         # Current project documentation master file
├── app.py                   # Legacy Streamlit UI interface
├── app5.py                  # Streamlit Brutalist User Interface Engine (Active)
├── requirements.txt         # System Python library packages
├── server.py                # Flask Server Sent Events API streaming core
└── tempCodeRunnerFile.py    # Temporary execution script cache
```

---

##  Quickstart Deployment Guide

### 1. Environmental Setup

Clone the repository, create a python virtual environment, and install the required library packages:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

Create a `.env` file in the root directory and append your access key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here

```

### 2. Ingest the Data Corpus (Build the Brain)

Run your ingestion scripts to build the local database index:

```bash
# Process and index the blog corpus
python3 ingest_blogs.py

# Process and index the video transcripts
python3 ingest.py

```

Verify that a `chroma_db` folder appears in your project root with your indexed vector data.

### 3. Initialize the Digital Twin

Open a terminal instance and start your Flask backend server:

```bash
python3 server.py

```

Ensure the log console outputs `[INFO] EnsembleRetriever loaded successfully` and listens on port `5000`.

In a separate parallel terminal pane, launch the brutalist interface:

```bash
streamlit run app5.py

```

Open your browser to the designated Streamlit port to interact with your personalized Andrej Karpathy Digital Twin!
