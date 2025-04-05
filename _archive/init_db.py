# init_db.py

import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect("conversation_history.db")
cursor = conn.cursor()

# Create the conversation_history table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS conversation_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT NOT NULL,
        prediction INTEGER NOT NULL,
        description TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print("✅ Table created successfully!")