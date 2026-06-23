import uuid
from ollama_client import get_embedding, chat_with_model
from database import get_chroma_collection

def retrieve_memories(session_id, user_query, limit=2):
    """Searches ChromaDB globally for the most relevant past summaries."""
    collection = get_chroma_collection()
    query_vector = get_embedding(user_query)
    
    # The 'where' clause has been completely removed.
    # The AI will now search your entire ChromaDB vault across all sessions.
    results = collection.query(
        query_embeddings=[query_vector],
        n_results=limit
    )
    
    if results['documents'] and len(results['documents'][0]) > 0:
        return results['documents'][0]
    return []

def generate_and_save_summary(session_id, messages_chunk):
    """Compresses 15 messages into 1 summary and saves to Chroma."""
    formatted_chunk = "\n".join([f"{m['role']}: {m['content']}" for m in messages_chunk])
    
    prompt = [{
        "role": "system",
        "content": "You are a memory consolidation system. Summarize the key details from this chat segment into a concise 1-2 sentence statement. Focus ONLY on important facts."
    }, {
        "role": "user",
        "content": f"Chat Segment:\n{formatted_chunk}"
    }]
    
    summary_text = chat_with_model(prompt)
    embedding = get_embedding(summary_text)
    
    collection = get_chroma_collection()
    memory_id = f"mem_{uuid.uuid4().hex[:8]}"
    
    # We still save the session_id as metadata so you have a record of when 
    # and where this memory was originally created.
    collection.add(
        embeddings=[embedding],
        documents=[summary_text],
        metadatas=[{"session_id": session_id}], 
        ids=[memory_id]
    )
    
    print(f"\n[SYSTEM]: New Memory Saved to ChromaDB -> '{summary_text}'\n")