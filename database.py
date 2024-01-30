import sqlite3

db_file = 'emails.db'

conn = sqlite3.connect(db_file)

cursor = conn.cursor()

create_table_query = '''
CREATE TABLE IF NOT EXISTS emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    sender TEXT,
    sender_address TEXT,
    timestamp TEXT,
    content TEXT,
    evaluation TEXT
)
'''

cursor.execute(create_table_query)

conn.commit()
conn.close()

print("Database and table created successfully.")