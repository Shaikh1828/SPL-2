import sqlite3
from PyQt5.QtWidgets import QMessageBox, QWidget

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path

        self.init_database(self) 

    def init_database(self):
        """Initializes the database and creates the `users` table if it doesn't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database initialization error: {e}")
