import os
import requests
from bs4 import BeautifulSoup
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import warnings

warnings.filterwarnings("ignore")

karpathy_blogs = [
    "https://karpathy.github.io/2015/05/21/rnn-effectiveness/",
    "https://karpathy.github.io/2019/04/25/recipe/",
    "https://karpathy.github.io/2012/10/22/state-of-computer-vision/"
]

def fetch_and_embed_blogs():
    print("Initializing ChromaDB (Using local embeddings, bypassing Google!)...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    
    collection = chroma_client.get_or_create_collection("karpathy_corpus")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    all_ids, all_documents = [], []
    
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)'}
    
    for url in karpathy_blogs:
        print(f"Scraping blog: {url}...")
        try:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            text_elements = soup.find_all(['p', 'h1', 'h2', 'h3', 'li'])
            full_text = " ".join([elem.get_text(strip=True) for elem in text_elements])
            
            chunks = splitter.split_text(full_text)
            
            for i, chunk in enumerate(chunks):
                doc_id = f"blog_{url.split('/')[-2]}_{i}"
                all_ids.append(doc_id)
                all_documents.append(chunk)
                
            print(f"Processed {len(chunks)} chunks from this post.")
        except Exception as e:
            print(f"Skipping {url}: {e}")
            
    if all_documents:
        print("Embedding and saving to local database... (This takes a few seconds)")
       
        collection.upsert(ids=all_ids, documents=all_documents)
        print("\nSUCCESS: Written data successfully ingested into ChromaDB! The Twin has a brain.")

if __name__ == "__main__":
    fetch_and_embed_blogs()