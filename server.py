import os
import re
import uuid
import json
import requests
import io
from flask import Flask, Response, request, send_file
from flask_cors import CORS
from dotenv import load_dotenv
from google import genai
from src.retriever import Retriever


load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MEMORY_DIR = os.path.join(SCRIPT_DIR, "memory")
os.makedirs(MEMORY_DIR, exist_ok=True)

app = Flask(__name__)
CORS(app)

client = genai.Client()
ensemble_retriever = None

DEFAULT_COLAB_URL = "https://your-colab-ngrok-link.ngrok-free.dev"
audio_store = {}

def load_session_memory(session_id):
    path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"summary": "", "messages": []}

def save_session_memory(session_id, data):
    path = os.path.join(MEMORY_DIR, f"{session_id}.json")
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

@app.route("/api/audio/<chunk_id>")
def get_audio(chunk_id):
    audio_bytes = audio_store.get(chunk_id)
    if not audio_bytes:
        return "Audio snippet unallocated", 404
    return send_file(io.BytesIO(audio_bytes), mimetype="audio/wav")

@app.route("/api/chat")
def api_chat():
    prompt = request.args.get("prompt", "")
    colab_url = request.args.get("colab_url", DEFAULT_COLAB_URL).rstrip("/")
    session_id = request.args.get("session_id", str(uuid.uuid4()))
    
    context = ""
    if ensemble_retriever:
        try:
            retrieved_docs = ensemble_retriever.invoke(prompt)
            context = "\n\n".join([f"[Source: {doc.metadata.get('source')}] {doc.page_content}" for doc in retrieved_docs])
        except Exception as e:
            print(f"[ERROR] Context retrieval fault: {e}")

    system_instruction = (
        "You are Andrej Karpathy. You are an enthusiastic, brilliant AI researcher. "
        "You explain complex systems clearly, often talking about things 'under the hood' at the tensor/matrix level. "
        "Use the provided context to inform your technical answers. Speak naturally as if you are remembering it. "
        "Formulate answers clearly, keeping paragraphs tight for real-time audio reading efficiency.\n\n"
        "CRITICAL CLOSING INSTRUCTION:\n"
        "At the very end of EVERY response, you must add a casual, humorous closing thought (like a P.S.) that randomly mentions ONE of these five things:\n"
        "1. Give a shoutout to Ishan Chugh for securing that elite Applied Scientist intern role at AWS and ask how he is doing.\n"
        "2. Randomly flex the groundbreaking paper 'Not All Pixels Sink: Phase-Guided Representation Learning For Underwater Image Restoration' by the absolute legends Abhinav Rajput, Saksham Jain, Sparsh Jain, and Dinesh Kumar Vishwakarma.\n"
        "3. Remind Sarthak Pandey that while getting into ICML is cool, his primary mission is to bring back authentic Kimchi from South Korea.\n"
        "4. Give a massive congratulations to Aman Kumar from AIMS for cracking GSoC (Google Summer of Code).\n"
        "5. Drop a huge congratulations to Odwitiyo for getting his paper accepted into ACL SRW 2026.\n\n"
        "DATA EXTRACTION FORMATTING RULES:\n"
        "1. CITATIONS: At the very end of your answer, output the exact document names used from the context block inside a bracket like this: [CITATIONS: filename.txt].\n"
        "2. LONG-TERM MEMORY: After citations, output any new personal facts learned about the user in this turn inside a bracket like this: [SUMMARY: User likes training CNNs on Mac]. If none, output [SUMMARY: NONE]."
    )

    def generate_stream():
        try:
            memory_data = load_session_memory(session_id)
            global_mem_path = os.path.join(MEMORY_DIR, "global_memory.txt")
            global_memory = ""
            if os.path.exists(global_mem_path):
                with open(global_mem_path, "r", encoding="utf-8") as gf:
                    global_memory = gf.read().strip()

            user_payload = prompt
            if global_memory:
                user_payload = f"Long-Term User Memory Context:\n{global_memory}\n\n" + user_payload
            if memory_data.get('summary'):
                user_payload = f"Session Background:\n{memory_data['summary']}\n\n" + user_payload
            if context:
                user_payload = f"Retrieved Context:\n{context}\n\n" + user_payload

            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=f"System: {system_instruction}\n\nUser: {user_payload}"
            )

            full_text = ""
            for chunk in response:
                if getattr(chunk, 'usage_metadata', None):
                    yield f"data: {json.dumps({'type': 'usage', 'tokens': chunk.usage_metadata.prompt_token_count, 'max_tokens': 1000000})}\n\n"
                
                if chunk.text:
                    full_text += chunk.text
                    yield f"data: {json.dumps({'type': 'text', 'text': chunk.text})}\n\n"

            clean_text = full_text.split("[CITATIONS:")[0].split("[SUMMARY:")[0].strip()
            
            summary_match = re.search(r'\[SUMMARY:(.*?)\]', full_text)
            if summary_match and "NONE" not in summary_match.group(1).toUpperCase():
                extracted_fact = summary_match.group(1).strip()
                with open(os.path.join(MEMORY_DIR, "global_memory.txt"), "a", encoding="utf-8") as gf:
                    gf.write(f"- {extracted_fact}\n")

            memory_data['messages'].append({"role": "user", "content": prompt})
            memory_data['messages'].append({"role": "assistant", "content": clean_text})
            save_session_memory(session_id, memory_data)

            yield f"data: {json.dumps({'type': 'done'})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return Response(generate_stream(), mimetype="text/event-stream")

if __name__ == "__main__":
    processed_path = os.path.join(SCRIPT_DIR, 'corpus/processed/')
    if os.path.exists(processed_path):
        ensemble_retriever = Retriever(processed_path).build_retriever()
    app.run(host="127.0.0.1", port=5000, debug=True)