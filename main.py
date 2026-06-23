import sqlite3
from database import init_chat_db
from ollama_client import chat_with_model
from memory_engine import retrieve_memories, generate_and_save_summary

def main():
    init_chat_db()
    
    print("--- AI Episodic Memory Engine ---")
    session_id = input("Enter a Session ID to load or create a new one: ")
    print(f"\nSession '{session_id}' Active. Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
            
        conn = sqlite3.connect("chat_history.db")
        cursor = conn.cursor()
        
        # 1. Save User Message
        cursor.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?, 'user', ?)", (session_id, user_input))
        conn.commit()
        
        # 2. Retrieve Relevant Long-Term Memory
        relevant_memories = retrieve_memories(session_id, user_input, limit=2)
        memory_context = " ".join(relevant_memories) if relevant_memories else "None."
        
        # 3. Pull Short-Term History (Last 5 messages)
        cursor.execute("SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY id DESC LIMIT 5", (session_id,))
        recent_history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()][::-1]
        
        # 4. Build Prompt
        system_prompt = {
            "role": "system",
            "content": f"You are a helpful assistant. Relevant recalled memories: [{memory_context}]. Use them if applicable."
        }
        final_prompt = [system_prompt] + recent_history
        
        # 5. Get AI Response
        reply = chat_with_model(final_prompt)
        print(f"AI: {reply}\n")
        
        # 6. Save AI Response
        cursor.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?, 'assistant', ?)", (session_id, reply))
        conn.commit()
        
        # 7. Check Message Count & Trigger Summary
        cursor.execute("SELECT COUNT(*) FROM chat_history WHERE session_id = ?", (session_id,))
        msg_count = cursor.fetchone()[0]
        
        if msg_count > 0 and msg_count % 15 == 0:
            cursor.execute("SELECT role, content FROM chat_history WHERE session_id = ? ORDER BY id DESC LIMIT 15", (session_id,))
            chunk = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()][::-1]
            generate_and_save_summary(session_id, chunk)
            
        conn.close()

if __name__ == "__main__":
    main()