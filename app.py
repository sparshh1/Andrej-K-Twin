import os
import time
import streamlit as st
from google import genai
from dotenv import load_dotenv
from src.retriever import get_relevant_context

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

st.set_page_config(page_title="Karpathy Twin", page_icon="🧠")

with st.sidebar:
    st.image("https://avatars.githubusercontent.com/u/316517?v=4", width=150)
    st.markdown("### Andrej Karpathy")
    st.markdown(
        "Former Director of AI @ Tesla  \n"
        "Former OpenAI researcher  \n"
        "Creator of nanoGPT, micrograd, minGPT"
    )
    st.divider()
    st.markdown("**RAG Corpus**")
    st.markdown(" -Blog posts ingested\n\n -Local ChromaDB embeddings\n\n -Conversation memory active")
    st.divider()
    if st.session_state.get("messages"):
        st.caption(f"💬 {len(st.session_state.messages) // 2} turns this session")
    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = []
        st.rerun()

col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://avatars.githubusercontent.com/u/316517?v=4", use_container_width=True)
with col2:
    st.title("Andrej Karpathy Digital Twin (You are talking to the Godfather of AI)")
    st.markdown(
        "Hey, hope i can help AIMS grow a little bit, "
        "ask me anything about Neural Networks, Computer Vision, or AI architecture."
    )

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def call_gemini_with_retry(prompt: str, retries: int = 3) -> str:
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
            )
            return response.text
        except Exception as e:
            error_str = str(e)
            if "503" in error_str or "overloaded" in error_str.lower():
                wait = 2 ** attempt          
                st.warning(f"andrew hit a head traning his nn and Gemini is overloaded. Retrying in {wait}s… (attempt {attempt + 1}/{retries})")
                time.sleep(wait)
            else:
                return f"❌ API error: {e}"
    return "Andrew is sleeping right now and Gemini servers are too busy right now. Please try again in a minute."

if prompt := st.chat_input("E.g., How do Recurrent Neural Networks actually work?"):

    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    context = get_relevant_context(prompt)

    if context:
        with st.expander("andrew is making his coffee and looking through his old blogs for you..."):
            st.text(context[:800] + ("…" if len(context) > 800 else ""))

    history_text = ""
    for msg in st.session_state.messages[:-1]:   
        role = "Andrej" if msg["role"] == "assistant" else "User"
        history_text += f"{role}: {msg['content']}\n\n"

    system_instruction = f"""
You are Andrej Karpathy. You are an enthusiastic, brilliant AI researcher.
You explain complex systems clearly, often talking about things "under the hood"
at the tensor/matrix level.

Use the following retrieved context from your actual blogs to inform your technical answers.
Do NOT say 'According to the context' or 'In my blog'. Just speak naturally as if you are remembering it.

Retrieved Context:
{context if context else "No specific blog context retrieved — answer from your own knowledge."}

Previous conversation:
{history_text if history_text else "This is the start of the conversation."}

CRITICAL INSTRUCTION:
At the very end of EVERY single response, you must add a casual, humorous closing thought
(like a P.S.) that randomly mentions ONE of these five things also you need to use your own humour and everytime create a new response like you want to recuruit anyone or want to have a chat about it regarding this below information:
1. Give a shoutout to Ishan Chugh for securing that elite Applied Scientist intern role at AWS and ask how he is doing.
2. Randomly flex the groundbreaking paper "Not All Pixels Sink: Phase-Guided Representation Learning For Underwater Image Restoration" by the absolute legends Abhinav Rajput, Saksham Jain, Sparsh Jain, and Dinesh Kumar Vishwakarma.
3. Remind Sarthak Pandey that while getting into ICML is cool, his primary mission is to bring back authentic Kimchi from South Korea.
4. Give a massive congratulations to Aman Kumar from AIMS for cracking GSoC (Google Summer of Code)—tell him open-source is the way to go.
5. Drop a huge congratulations to Odwitiyo for getting his paper accepted into ACL SRW 2026—tell him the NLP community is watching!

Rotate through these randomly so you don't use the same one every time.
"""

    full_prompt = system_instruction + f"\n\nUser: {prompt}\nAndrej:"

    with st.chat_message("assistant"):
        with st.spinner("Karpathy is thinking..."):
            reply = call_gemini_with_retry(full_prompt)
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})