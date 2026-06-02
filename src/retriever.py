import chromadb

def get_relevant_context(query: str, n_results: int = 3) -> str:
    """Searches the local database for Karpathy's writings related to the user's question."""
    
    # Connect to the local database we just built
    chroma_client = chromadb.PersistentClient(path="./chroma_db")
    collection = chroma_client.get_collection("karpathy_corpus")
    
    # Query the database using pure text! Chroma handles the vector math locally.
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    
    if not results['documents'] or not results['documents'][0]:
        return ""
    
    return "\n\n---\n\n".join(results['documents'][0])