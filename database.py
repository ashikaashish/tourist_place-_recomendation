import sqlite3

conn = sqlite3.connect("tourist.db")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
age INTEGER,
budget TEXT,
climate TEXT
)
""")

# Likes Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS likes(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
place TEXT
)
""")

# Ratings Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS ratings(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
place TEXT,
rating INTEGER
)
""")

conn.commit()
conn.close()

print("Database Created Successfully")