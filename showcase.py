import sqlite3
from database import get_chroma_collection

def run_showcase():
    print("\n" + "="*70)
    print(" [ AI HYBRID MEMORY BACKEND SHOWCASE ] ")
    print("="*70)
    
    # --- Part 1: SQLite (Short-Term Chat Log) ---
    print("\n[ DATABASE 1: SQLite (chat_history.db) ]")
    print("Purpose: Stores the exact, chronological conversation history.")
    
    try:
        conn = sqlite3.connect("chat_history.db")
        cursor = conn.cursor()
        
        # Count total raw messages
        cursor.execute("SELECT COUNT(*) FROM chat_history")
        total_msgs = cursor.fetchone()[0]
        print(f" -> Total Raw Messages Logged: {total_msgs}")
        
        # Show a preview of the latest messages
        print(" -> Last 3 Messages in the DB:")
        cursor.execute("SELECT session_id, role, content FROM chat_history ORDER BY id DESC LIMIT 3")
        for row in reversed(cursor.fetchall()):
            # Truncate long messages for a clean display
            content = row[2][:70] + "..." if len(row[2]) > 70 else row[2]
            print(f"    [{row[0]}] {row[1].upper()}: {content}")
            
        conn.close()
    except Exception as e:
        print(" -> [!] Could not load SQLite database.")

    # --- Part 2: ChromaDB (Long-Term Vector Vault) ---
    print("\n" + "-"*70)
    print("\n[ DATABASE 2: ChromaDB (chroma_data folder) ]")
    print("Purpose: Stores mathematical embeddings and distilled fact summaries.")
    
    try:
        collection = get_chroma_collection()
        results = collection.get()
        
        if not results['documents']:
            print(" -> No episodic memories saved yet.")
        else:
            total_mems = len(results['documents'])
            print(f" -> Total Episodic Memories Extracted: {total_mems}")
            print(" -> Global Memory Vault Contents:")
            
            # Print out every memory and where it came from
            for i in range(total_mems):
                session = results['metadatas'][i].get('session_id', 'Unknown')
                text = results['documents'][i]
                print(f"    * [Source: {session}] {text}")
                
    except Exception as e:
        print(" -> [!] Could not load ChromaDB.")

    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    run_showcase()