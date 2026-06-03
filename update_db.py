import sqlite3

conn = sqlite3.connect("tourist.db")
cursor = conn.cursor()

cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")

conn.commit()
conn.close()

print("Password column added!")