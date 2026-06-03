import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH  = os.path.join(BASE_DIR, "tourist.db")

conn   = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Drop old tables so they get recreated with correct schema
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS likes")
cursor.execute("DROP TABLE IF EXISTS ratings")

conn.commit()
conn.close()

print("Old tables dropped.")