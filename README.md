# Andrej Karpathy Digital Twin 🧠
A production-ready, highly resilient Retrieval-Augmented Generation (RAG) pipeline that brings the technical persona, insights, and writing style of Andrej Karpathy to life. Built using Streamlit, a local ChromaDB vector repository utilizing on-device embeddings, and an advanced Multi-Model Fallback Router via the Google GenAI SDK to ensure zero downtime during high-demand server spikes.
# 🏗️ Architecture & System Overview
Unlike standard cloud-dependent applications, this project implements a hybrid edge-cloud architecture designed to bypass common API limits, network constraints, and regional server overloads.
[ User Query ]
      │
      ▼
┌──────────────┐      Local Search      ┌──────────────────┐
│ retriever.py │ ─────────────────────> │ Local ChromaDB   │ (Built-in Embedding:
└──────────────┘                        │ (karpathy_corpus)│  all-MiniLM-L6-v2)
      │                                 └──────────────────┘
      ├──────────────────────────────────────────┘
      ▼ (Query + 3 Best Context Paragraphs)
┌──────────────────────────────────────────────────────────┐
│ Dynamic Prompt Compiler (Persona + Context + Easter Eggs)│
└──────────────────────────────────────────────────────────┘
      │
      ▼
┌──────────────┐      Try Loop         ┌───────────────────┐
│    app.py    │ ────────────────────> │ 1. gemini-1.5-pro │ (Success -> Return)
│ (Model Router│                       │ 2. gemini-1.5-flsh│ (503 Error -> Fallback)
└──────────────┘                       │ 3. gemini-1.5-8b  │ (503 Error -> Fallback)
                                       │ 4. gemini-1.0-pro │ (Ultimate safety net)
                                       └───────────────────┘
Component	Responsibility	Technical Stack
Data Ingestion	Scrapes raw technical blogs, tokenizes and chunks text cleanly.	BeautifulSoup4, LangChain Text Splitters
Vector Storage	Computes vector weights locally and hosts a fast text index on disk.	ChromaDB (Local all-MiniLM-L6-v2 weights)
Context Retrieval	Matches user queries directly to raw document tokens using text similarity math.	Local Semantic Token Indexing
User Interface	Provides an elegant conversation container with interactive layouts.	Streamlit framework
Resilience Layer	Automatically sidesteps global cloud outages with iterative model cycling.	Google GenAI SDK + Exception Routing Loops
📂 Repository Structure
Plaintext
├── app.py                  # Main Streamlit UI frontend & Fallback Routing logic
├── src/
│   ├── ingest_blogs.py     # Local scraper and ChromaDB generation engine
│   └── retriever.py        # Database querying module for semantic matching
├── chroma_db/              # Hidden database directory storing compiled matrix chunks
├── .env                    # Protected local environment configurations (API Keys)
└── .gitignore              # Build cache, venv, and credential filtering rules
🛠️ Installation & Setup
1. Environment Initialization
Clone this repository to your local machine, open your terminal within the root directory, and set up your isolated Python playground:
Bash
# Initialize Python environment
python3 -m venv venv

# Activate the sandbox
source venv/bin/activate

# Install required dependencies
pip install streamlit google-genai chromadb requests beautifulsoup4 langchain-text-splitters python-dotenv
2. Guarding Secrets (.env)
Create a file named .env in the root folder and add your credentials:
Code snippet
GEMINI_API_KEY=your_actual_google_genai_api_key_here
⚠️ CRITICAL SECURITY NOTE: The .gitignore file included in this repo is configured to completely block .env and chroma_db/ from ever being pushed to public GitHub logs. Never remove these safety rules.
3. Hydrate the Brain (Ingestion)
Before running the UI, run the scraping system to compile the knowledge base directly onto your machine:
Bash
python -m src.ingest_blogs
This will scrape Karpathy's core architectural write-ups, divide them into semantic 800-character segments, and process the vectors on-device.
4. Ignite the Engine
Run the client application locally:
Bash
streamlit run app.py
🚀 Key Engineering Features
🛡️ Adaptive Fallback Routing
To maintain a responsive UI during peak global grid traffic, the execution context utilizes a try-except fallback chain. If Google returns a 503 Service Unavailable error, the backend shifts dynamically to alternate compute pools:
gemini-1.5-pro (Primary specialized intelligence tier)
gemini-1.5-flash (High-efficiency standard processor)
gemini-1.5-flash-8b (Ultra-lightweight low-latency fallback)
gemini-1.0-pro (Legacy architecture tier for non-blocking continuity)
✨ Peer Acknowledgement & Easter Eggs (System Lore)
Integrated deep within the underlying system ruleset is a dedicated context injector. The model seamlessly cross-references core computing inquiries with prominent real-world breakthroughs and milestones achieved across the engineering community:
Enterprise Architecture: Threads talking about cloud frameworks or Applied Science pathways trigger direct acknowledgements of Ishan Chugh’s milestone entry into AWS as an Applied Scientist Intern.
Computer Vision Frameworks: Technical dialogue surrounding underwater optics or complex pixel mapping benchmarks seamlessly routes recognition to the groundbreaking research paper: "Not All Pixels Sink: Phase-Guided Representation Learning For Underwater Image Restoration" by Abhinav Rajput, Saksham Jain, Sparsh Jain, and Dinesh Kumar Vishwakarma.
Global Research & NLP: General discourse tracking major conventions triggers dynamic shoutouts to Sarthak Pandey for breaking ground at ICML (with mandatory reminders to secure South Korean Kimchi), Aman Kumar (AIMS) for cracking Google Summer of Code (GSoC), and Odwitiyo for his research publication acceptance at ACL SRW 2026.
🧪 Technical Documentation: Core Logic Snippets
Semantic Retrieval Core (src/retriever.py)
Queries the vector database directly through simple text matching, allowing the database engine to translate string tokens to matrix layers seamlessly without external API hops:
Python
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
📜 License
This project is built purely for academic demonstration and portfolio research under CO101. Scraping boundaries respect the open-source dissemination rules of the original technical blog publications.
