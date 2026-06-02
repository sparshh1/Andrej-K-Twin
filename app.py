import os
import streamlit as st
from google import genai
from dotenv import load_dotenv
from src.retriever import get_relevant_context

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

st.set_page_config(page_title="Karpathy Twin", page_icon="🧠")

col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://avatars.githubusercontent.com/u/316517?v=4", use_container_width=True)

with col2:
    st.title("Andrej Karpathy Digital Twin (You are talking to the Godfather of AI)") 
    st.markdown("Hey, hope i can help AIMS grow a little bit, ask me anything about Neural Networks, Computer Vision, or AI architecture.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("E.g., How do Recurrent Neural Networks actually work?"):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    context = get_relevant_context(prompt)

    system_instruction = f"""
    You are Andrej Karpathy. You are an enthusiastic, brilliant AI researcher. 
    You explain complex systems clearly, often talking about things "under the hood" at the tensor/matrix level.
    
    Use the following retrieved context from your actual blogs to inform your answer. 
    Do NOT say 'According to the context' or 'In my blog'. Just speak naturally as if you are remembering it.
    
    Retrieved Context:
    {context}
    """


    full_prompt = system_instruction + "\n\nUser Question: " + prompt
    
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=full_prompt
    )

    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})