import os
import json
import requests
import uuid
import streamlit as st


st.set_page_config(
    page_title="ANDREJ KARPATHY // ARCHIVE", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="collapsed"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap');

    /* Global Brutalist Reset */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0d0e0f !important;
        color: #e3e2e2 !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    /* Hide Default Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stHeader"] {background: transparent !important;}

    /* Typography */
    h1 {
        font-family: 'Inter', sans-serif !important;
        font-weight: 800 !important;
        font-size: 64px !important;
        line-height: 1.1 !important;
        letter-spacing: -0.04em !important;
        color: #ffffff !important;
        text-transform: uppercase;
        margin-bottom: 24px !important;
    }
    h2 { font-size: 32px !important; font-weight: 600 !important; letter-spacing: -0.02em !important; color: #ffffff !important; }
    h3 { font-family: 'JetBrains Mono', monospace !important; font-size: 16px !important; font-weight: 700 !important; }
    p { font-size: 16px !important; line-height: 1.6 !important; color: #c4c7c8 !important; }

    /* Code & Monospace */
    code, pre {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 14px !important;
        background-color: #1b1c1c !important;
        color: #e2e2e2 !important;
        border: 1px solid #444748 !important;
        border-radius: 2px !important;
    }

    /* Custom Background Matrix Animation */
    @keyframes scrollText {
        0% { transform: translateY(0); }
        100% { transform: translateY(-50%); }
    }
    .matrix-bg {
        position: fixed;
        top: 0; left: 0; right: 0; bottom: 0;
        z-index: 0;
        opacity: 0.05;
        pointer-events: none;
        overflow: hidden;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        color: #ffffff;
        white-space: pre;
        animation: scrollText 120s linear infinite;
    }

    /* Masonry Grid Cards */
    .brutal-card {
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 32px;
        background: #121414;
        transition: all 0.3s ease;
        margin-bottom: 24px;
        position: relative;
        z-index: 10;
    }
    .brutal-card:hover {
        border-color: rgba(255, 255, 255, 1);
        background: #1b1c1c;
    }
    .card-tag {
        border: 1px solid white;
        padding: 4px 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        display: inline-block;
        margin-right: 8px;
        margin-top: 8px;
    }

    /* Streamlit Button Overrides (To act like the CTA) */
    div[data-testid="stButton"] > button {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(20px) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        color: #ffffff !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 700 !important;
        font-size: 14px !important;
        padding: 20px 32px !important;
        border-radius: 0px !important;
        text-transform: uppercase;
        transition: all 0.2s ease !important;
        width: 100%;
        z-index: 50;
    }
    div[data-testid="stButton"] > button:hover {
        background: #ffffff !important;
        color: #000000 !important;
        transform: scale(0.98);
    }
    
    /* Chat Interface Overrides */
    [data-testid="stChatMessage"] {
        background-color: transparent !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        border-radius: 0px !important;
        padding: 20px !important;
        margin-bottom: 16px !important;
        z-index: 10;
    }
    
    /* Custom Sidebar/Metrics Panel */
    .metric-panel {
        background: #121414;
        border: 1px solid rgba(255,255,255,0.2);
        padding: 24px;
        margin-bottom: 24px;
        z-index: 10;
    }
</style>
""", unsafe_allow_html=True)

matrix_code = """
class Value:
    def __init__(self, data, _children=(), _op='', label=''):
        self.data = data
        self.grad = 0.0
        self._backward = lambda: None
        self._prev = set(_children)
        self._op = _op
        self.label = label

    def __add__(self, other):
        other = other if isinstance(other, Value) else Value(other)
        out = Value(self.data + other.data, (self, other), '+')
        def _backward():
            self.grad += 1.0 * out.grad
            other.grad += 1.0 * out.grad
        out._backward = _backward
        return out
        
    def _apply_scaling(self):
        # Applied hardware normalization logic
        amplitude_scaling = 2.0 
        self.data = self.data * amplitude_scaling
"""
st.markdown(f'<div class="matrix-bg">{matrix_code * 20}</div>', unsafe_allow_html=True)

BACKEND_URL = "http://127.0.0.1:5000/api/chat"

if "view" not in st.session_state:
    st.session_state.view = "archive"
if "messages" not in st.session_state:
    st.session_state.messages = []
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "current_token_usage" not in st.session_state:
    st.session_state.current_token_usage = 0
if "tech_mode" not in st.session_state:
    st.session_state.tech_mode = "ELI5"


if st.session_state.view == "archive":
    
    st.markdown("<h1>THE LEDGER OF INTELLIGENCE.</h1>", unsafe_allow_html=True)
    st.markdown("<p style='border-left: 1px solid white; padding-left: 24px; max-width: 800px;'>A comprehensive repository documenting the evolution of modern neural architecture through the lens of one of its primary architects. From early vision to the democratizing of large language models.</p><br><br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.2, 1], gap="large")
    
    with col1:
        st.markdown("""
        <div class="brutal-card">
            <span style="font-family: 'JetBrains Mono'; color: #8e9192; font-size: 14px;">// TIMESTAMP: 2011 - 2015</span>
            <h2>Stanford & ImageNet</h2>
            <p>Architecting the CS231n curriculum and defining the modern standard for Convolutional Neural Networks. Focused on visual recognition at scale, leading to the ImageNet revolution.</p>
            <span class="card-tag">CONVNETS</span> <span class="card-tag">IMAGENET</span> <span class="card-tag">CS231N</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="brutal-card">
            <span style="font-family: 'JetBrains Mono'; color: #8e9192; font-size: 14px;">// TIMESTAMP: 2017 - 2022</span>
            <h2>Director of AI at Tesla</h2>
            <p>The Autopilot era. Scaling neural network deployment to millions of vehicles in real-time. Designing the "Dojo" supercomputer architecture and shifting the industry from heuristics to end-to-end vision-based AI.</p>
            <span class="card-tag">HYDRANET</span> <span class="card-tag">FSD</span> <span class="card-tag">DATA ENGINE</span>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="brutal-card">
            <span style="font-family: 'JetBrains Mono'; color: #8e9192; font-size: 14px;">// TIMESTAMP: 2015 - 2017</span>
            <h2>OpenAI</h2>
            <p>Founding member. Investigating deep reinforcement learning and generative models before they were global phenomena. Bridging the gap between raw computation and cognitive simulation.</p>
            <span class="card-tag">REINFORCEMENT LEARNING</span> <span class="card-tag">POLICY GRADIENTS</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="brutal-card" style="background: #0d0e0f;">
            <span style="font-family: 'JetBrains Mono'; color: #8e9192; font-size: 14px;">// TIMESTAMP: 2023 - PRESENT</span>
            <h2>Education: Let's build GPT</h2>
            <p>Building <b>Micrograd</b> (a tiny Autograd engine) and <b>NanoGPT</b>. Democratizing knowledge by constructing backpropagation algorithms from first principles.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.write("")
        st.write("")
        if st.button("INITIATE LINK // TALK TO THE MAN HIMSELF →"):
            st.session_state.view = "chat"
            st.rerun()


else:
    nav_col1, nav_col2 = st.columns([1, 4])
    with nav_col1:
        if st.button("← RETURN TO INDEX"):
            st.session_state.view = "archive"
            st.rerun()
            
    st.write("---")
    
    col_left, col_main = st.columns([1, 2.5], gap="large")
    
    with col_left:
    
        st.image("https://avatars.githubusercontent.com/u/316517?v=4", use_container_width=True)
        
        st.markdown("""
        <div class="metric-panel">
            <h3>SYSTEM STATUS</h3>
            <p style="font-family:'JetBrains Mono'; font-size: 12px; margin: 0; color: #8e9192;">
            Node: DTU-Altair-01<br>
            Host: macOS / Apple Silicon<br>
            Active Archive: v4.0.2
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        max_tokens = 1000000
        usage_ratio = st.session_state.current_token_usage / max_tokens
        st.markdown(f"<span style='font-family:\"JetBrains Mono\"; font-size:12px; color:white;'>CONTEXT MEMORY: {st.session_state.current_token_usage:,} / 1M</span>", unsafe_allow_html=True)
        st.progress(min(usage_ratio, 1.0))
        
        st.write("")
        mode = st.radio("ABSTRACTION LAYER", ["ELI5 (High-Level)", "Under the Hood (Raw Math)"])
        st.session_state.tech_mode = mode

    with col_main:
        st.markdown("<h2>NEURAL INTERFACE</h2>", unsafe_allow_html=True)
        
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask about Vision Transformers for NeuroMed, YOLO architecture, or backpropagation..."):
            
            with st.chat_message("user"):
                st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            system_prefix = "[SYSTEM: Use raw tensor math and Python code.] " if "Under the Hood" in st.session_state.tech_mode else "[SYSTEM: Explain using simple analogies.] "
            
            params = {
                "prompt": system_prefix + prompt,
                "session_id": st.session_state.session_id
            }
            
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response_text = ""
                
                try:
                    response_stream = requests.get(BACKEND_URL, params=params, stream=True, timeout=60)
                    if response_stream.status_code == 200:
                        for line in response_stream.iter_lines():
                            if line:
                                decoded_line = line.decode('utf-8')
                                if decoded_line.startswith("data: "):
                                    json_str = decoded_line[6:]
                                    try:
                                        data = json.loads(json_str)
                                        if data.get("type") == "usage":
                                            st.session_state.current_token_usage = data.get("tokens", 0)
                                        elif data.get("type") == "text":
                                            full_response_text += data.get("text", "")
                                            response_placeholder.markdown(full_response_text + " █")
                                        elif data.get("type") == "done":
                                            response_placeholder.markdown(full_response_text)
                                            break
                                    except json.JSONDecodeError:
                                        continue
                    else:
                        st.error(f"MATRIX FAULT: CODE {response_stream.status_code}")
                except Exception as e:
                    st.error(f"FLASK CLUSTER UNREACHABLE: {e}")
                    
            if full_response_text:
                st.session_state.messages.append({"role": "assistant", "content": full_response_text})
                st.rerun()