import os
import chromadb
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
import warnings

warnings.filterwarnings("ignore")


karpathy_videos = {
    "kCc8FmEb1nY": "Let's Build GPT from Scratch",
    "zduSFxRajkE": "Let's Build the GPT Tokenizer",
    "VMj-3S1tku0": "Building micrograd / Backpropagation",
}


def fetch_and_embed():
    print("=" * 60)
    print("KARPATHY YOUTUBE TRANSCRIPT INGESTION")
    print("Using local ChromaDB embeddings (all-MiniLM-L6-v2)")
    print("=" * 60)

    chroma_client = chromadb.PersistentClient(path="./chroma_db")

    collection = chroma_client.get_or_create_collection("karpathy_corpus")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    yt_api = YouTubeTranscriptApi()

    total_chunks = 0
    all_ids, all_documents = [], []

    for vid_id, title in karpathy_videos.items():
        print(f"\n[→] Fetching transcript: {title}")
        print(f"    Video ID: {vid_id}")

        try:
            transcript = yt_api.fetch(vid_id)
            full_text = " ".join([snippet.text for snippet in transcript])

            word_count = len(full_text.split())
            print(f"    Transcript length: {word_count:,} words")

            chunks = splitter.split_text(full_text)
            print(f"    Split into {len(chunks)} chunks (800 chars, 150 overlap)")

            for i, chunk in enumerate(chunks):
                doc_id = f"yt_{vid_id}_{i}"
                all_ids.append(doc_id)
                all_documents.append(chunk)

            total_chunks += len(chunks)
            print(f"    [✓] {len(chunks)} chunks queued")

        except Exception as e:
            print(f"    [✗] Skipping {vid_id}: {e}")

    if all_documents:
        print(f"\n[→] Embedding and saving {len(all_documents)} chunks to ChromaDB...")
        print("    (ChromaDB runs all-MiniLM-L6-v2 locally — no API calls needed)")
        collection.upsert(ids=all_ids, documents=all_documents)

        # Verify what's now in the collection
        count = collection.count()
        print(f"\n{'=' * 60}")
        print(f"SUCCESS — YouTube transcripts ingested.")
        print(f"Total chunks in karpathy_corpus: {count}")
        print(f"{'=' * 60}")
    else:
        print("\n[!] No documents to ingest. Check video IDs or network connection.")


if __name__ == "__main__":
    fetch_and_embed()
