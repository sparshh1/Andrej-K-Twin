import os
import chromadb
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from google import genai
from dotenv import load_dotenv
import warnings

warnings.filterwarnings("ignore")
load_dotenv()


client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

karpathy_videos = ["kCc8FmEb1nY", "zduSFxRajkE", "ojepHUd1xhI"]

def fetch_and_embed():
    print("Initializing ChromaDB...")
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_or_create_collection("karpathy_corpus")
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    
    all_ids, all_embeddings, all_documents = [], [], []
    yt_api = YouTubeTranscriptApi()
    
    for vid_id in karpathy_videos:
        print(f"Downloading transcript for {vid_id}...")
        try:
            transcript = yt_api.fetch(vid_id)
            full_text = " ".join([snippet.text for snippet in transcript])
            
            chunks = splitter.split_text(full_text)
            
            for i, chunk in enumerate(chunks):
                doc_id = f"yt_{vid_id}_{i}"
                
        
                response = client.models.embed_content(
                    model="models/embedding-001",
                    content=chunk
                )
                embedding = response.embedding
                
                all_ids.append(doc_id)
                all_embeddings.append(embedding)
                all_documents.append(chunk)
                
            print(f"Processed {len(chunks)} chunks for {vid_id}")
        except Exception as e:
            print(f"Skipping {vid_id}: {e}")
            
    if all_documents:
        collection.upsert(ids=all_ids, embeddings=all_embeddings, documents=all_documents)
        print("\nSUCCESS: Data successfully ingested into ChromaDB! The Twin has a brain.")

if __name__ == "__main__":
    fetch_and_embed()