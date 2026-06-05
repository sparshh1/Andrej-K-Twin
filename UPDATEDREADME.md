# ANDREJ KARPATHY / DIGITAL TWIN 

[![Live App](https://img.shields.io/badge/Live_Application-Streamlit_Cloud-FF4B4B?style=for-the-badge&logo=streamlit)](https://andrej-k-twin-awm8rzhs7m2rgde4xtlxvk.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com/)

A premium, strictly monochromatic interactive web application acting as a "Digital Twin" for AI researcher Andrej Karpathy. This dual-stack architecture combines a highly customized, brutalist Streamlit frontend with a streaming Flask backend powered by LangChain, Hugging Face, and ChromaDB.

🌐 **Live Interface:** [andrej-k-twin-awm8rzhs7m2rgde4xtlxvk.streamlit.app](https://andrej-k-twin-awm8rzhs7m2rgde4xtlxvk.streamlit.app/) (Backend Might not work because of the cloud space limit)

---

## 🏗️ System Architecture

This project is decoupled into two separate services to optimize UI rendering and heavy AI matrix computations.

### 1. The Frontend (Streamlit Cloud)
*   **Framework:** Streamlit (Python) heavily overridden with custom CSS injections.
*   **Aesthetic:** Academic brutalism, pitch black (`#000000`) and pure white (`#ffffff`).
*   **Views:** 
    *   `Legacy Archive:` A chronological masonry grid detailing his core history (Stanford, OpenAI, Tesla, Education).
    *   `Neural Interface:` A terminal-styled chat room featuring active system status metrics, simulated token generation, and an "Abstraction Layer" toggle (ELI5 vs. Under the Hood).

### 2. The Backend (Flask + LangChain)
*   **Framework:** Flask web server with Server-Sent Events (SSE) for token streaming.
*   **RAG Pipeline:** Uses LangChain and `langchain-chroma` to retrieve context regarding Andrej's work (micrograd, transformers, nanoGPT).
*   **Model Provider:** Hugging Face Hub (Requires `HF_TOKEN` for unthrottled inference).

---

## 🚀 Local Development Setup

To run this application on your local machine, you need to spin up the backend API first, followed by the frontend interface.

### Prerequisites
*   Python 3.10+
*   Hugging Face Account (for API Token)

### Step 1: Clone the Repository
```bash
git clone [https://github.com/yourusername/andrej-k-twin.git](https://github.com/yourusername/andrej-k-twin.git)
cd andrej-k-twin
