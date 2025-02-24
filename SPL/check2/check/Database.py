# import sqlite3
# from PyQt5.QtWidgets import QMessageBox, QWidget

# class Database:
#     def __init__(self, db_path="users.db"):
#         self.db_path = db_path
#         self.init_AppDatabase()
#         self.init_UserDatabase()

#     def init_UserDatabase(self):
#         """Initializes the database and creates the `users` table if it doesn't exist."""
#         try:
#             conn = sqlite3.connect(self.db_path)
#             cursor = conn.cursor()
#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS users (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     username TEXT UNIQUE NOT NULL,
#                     password TEXT NOT NULL
#                 )
#             """)
#             conn.commit()
#             conn.close()
#         except Exception as e:
#             print(f"User Database initialization error: {e}")

#     def init_AppDatabase(self):
#         try:
#             conn = sqlite3.connect("app_data.db")
#             cursor = conn.cursor()

#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS App (
#                     App_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                     Package_Name TEXT NOT NULL,
#                     Name TEXT NOT NULL,
#                     Version TEXT,
#                     Status TEXT,
#                     APK_File BLOB
#                 )
#             """)

#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS Permissions_Intents (
#                     Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                     Feature_Name TEXT NOT NULL
#                 )
#             """)

#             cursor.execute("""
#                 CREATE TABLE IF NOT EXISTS App_Features (
#                     App_Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
#                     App_ID INTEGER NOT NULL,
#                     Feature_ID INTEGER NOT NULL,
#                     FOREIGN KEY (App_ID) REFERENCES App(App_ID),
#                     FOREIGN KEY (Feature_ID) REFERENCES Permissions_Intents(Feature_ID)
#                 )
#             """)

#             conn.commit()
#             conn.close()
#             print("APP Database initialized successfully.")
#         except Exception as e:
#             print(f"Error initializing database: {e}")






# database.py
import sqlite3
from datetime import datetime
from PyQt5.QtWidgets import QMessageBox

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.check_and_update_schema()
        self.init_AppDatabase()

    def check_and_update_schema(self):
        """Check existing schema and update if necessary"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check if users table exists
            cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='users12'
            """)
            
            if cursor.fetchone() is None:
                # Create new users table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE,
                        verified INTEGER DEFAULT 0,
                        verification_code TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            else:
                # Check if needed columns exist and add them if they don't
                cursor.execute("PRAGMA table_info(users)")
                columns = [column[1] for column in cursor.fetchall()]
                
                if 'email' not in columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN email TEXT UNIQUE")
                if 'verified' not in columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0")
                if 'verification_code' not in columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN verification_code TEXT")
                if 'created_at' not in columns:
                    cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

            conn.commit()
            conn.close()
            print("User database schema updated successfully.")
        except Exception as e:
            print(f"Error updating database schema: {e}")

    def init_AppDatabase(self):
        """Initialize application database"""
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS App (
                    App_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Package_Name TEXT NOT NULL,
                    Name TEXT NOT NULL,
                    Version TEXT,
                    Status TEXT,
                    APK_File BLOB
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Permissions_Intents (
                    Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Feature_Name TEXT NOT NULL
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS App_Features (
                    App_Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    App_ID INTEGER NOT NULL,
                    Feature_ID INTEGER NOT NULL,
                    FOREIGN KEY (App_ID) REFERENCES App(App_ID),
                    FOREIGN KEY (Feature_ID) REFERENCES Permissions_Intents(Feature_ID)
                )
            """)

            conn.commit()
            conn.close()
            print("App Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing App database: {e}")

    def add_user(self, username, password, email, verification_code):
        """Add a new user with email verification"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO users (username, password, email, verification_code, verified)
                VALUES (?, ?, ?, ?, 0)
            """, (username, password, email, verification_code))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def verify_user(self, email, verification_code):
        """Verify user's email"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE users 
                SET verified = 1, verification_code = NULL 
                WHERE email = ? AND verification_code = ?
            """, (email, verification_code))
            
            success = cursor.rowcount > 0
            conn.commit()
            conn.close()
            return success
        except Exception as e:
            print(f"Error verifying user: {e}")
            return False

    def check_login(self, username, password):
        """Check login credentials"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, verified 
                FROM users 
                WHERE username = ? AND password = ?
            """, (username, password))
            
            result = cursor.fetchone()
            
            if result:
                user_id, is_verified = result
                if is_verified:
                    conn.close()
                    return True
                else:
                    conn.close()
                    return "unverified"
            conn.close()
            return False
        except Exception as e:
            print(f"Error checking login: {e}")
            return False