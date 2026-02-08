import sqlite3
from datetime import datetime

DB_PATH = "memory.db"


class Memory:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

        
    def get_all_prefs(self):
        cur = self.conn.cursor()
        cur.execute("SELECT key, value FROM preferences")
        return cur.fetchall()


    def create_tables(self):
        cur = self.conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            prompt TEXT,
            command TEXT,
            output TEXT,
            timestamp TEXT
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        self.conn.commit()

    # -------- Conversation storage --------
    def save_conversation(self, prompt, command, output):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT INTO conversations (prompt, command, output, timestamp) VALUES (?, ?, ?, ?)",
            (prompt, command, output, datetime.now().isoformat())
        )
        self.conn.commit()

    def get_recent_conversations(self, limit=5):
        cur = self.conn.cursor()
        cur.execute(
            "SELECT prompt, command, output, timestamp FROM conversations ORDER BY id DESC LIMIT ?",
            (limit,)
        )
        return cur.fetchall()

    # -------- Preferences --------
    def set_pref(self, key, value):
        cur = self.conn.cursor()
        cur.execute(
            "INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)",
            (key, value)
        )
        self.conn.commit()

    def get_pref(self, key, default=None):
        cur = self.conn.cursor()
        cur.execute("SELECT value FROM preferences WHERE key=?", (key,))
        row = cur.fetchone()
        return row[0] if row else default
