# database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        # Initialize database connection
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.check_and_update_schema()
        self.init_app_database()
        
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'connection'):
            self.connection.close()

    def check_and_update_schema(self):
        """Check existing schema and update if necessary"""
        try:
            # Check if users table exists
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='users'
            """)
            
            if not self.cursor.fetchone():
                # Create new users table if it doesn't exist
                self.cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE,
                        verified INTEGER DEFAULT 0,
                        verification_token TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.connection.commit()
                print("Users table created successfully.")
            else:
                # Check if needed columns exist and add them if they don't
                self.cursor.execute("PRAGMA table_info(users)")
                columns = [column[1] for column in self.cursor.fetchall()]
                
                if 'email' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN email TEXT UNIQUE")
                if 'verified' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0")
                if 'verification_token' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN verification_token TEXT")
                if 'created_at' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                
                self.connection.commit()
                print("User table schema updated successfully.")
        except Exception as e:
            print(f"Error updating database schema: {e}")

    def init_app_database(self):
        """Initialize application database"""
        try:
            app_conn = sqlite3.connect("app_data.db")
            app_cursor = app_conn.cursor()

            app_cursor.execute("""
                CREATE TABLE IF NOT EXISTS App (
                    App_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Package_Name TEXT NOT NULL,
                    Name TEXT NOT NULL,
                    Version TEXT,
                    Status TEXT,
                    APK_File BLOB
                )
            """)

            app_cursor.execute("""
                CREATE TABLE IF NOT EXISTS Permissions_Intents (
                    Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Feature_Name TEXT NOT NULL
                )
            """)

            app_cursor.execute("""
                CREATE TABLE IF NOT EXISTS App_Features (
                    App_Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    App_ID INTEGER NOT NULL,
                    Feature_ID INTEGER NOT NULL,
                    FOREIGN KEY (App_ID) REFERENCES App(App_ID),
                    FOREIGN KEY (Feature_ID) REFERENCES Permissions_Intents(Feature_ID)
                )
            """)

            app_conn.commit()
            app_conn.close()
            print("App Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing App database: {e}")

    # In the add_user method of Database.py, add:
    def add_user(self, username, password, email, jwt_token):
        """Store new user with JWT token for verification"""
        try:
            query = """
                INSERT INTO users 
                (username, password, email, verified, verification_token) 
                VALUES (?, ?, ?, 0, ?)
            """
            self.cursor.execute(query, (username, password, email, jwt_token))
            self.connection.commit()
            
            # Verify token was saved
            self.cursor.execute("SELECT verification_token FROM users WHERE email = ?", (email,))
            saved_token = self.cursor.fetchone()
            print(f"Saved token for {email}: {saved_token}")
            
            return True
        except sqlite3.IntegrityError as e:
            print(f"Integrity error adding user: {e}")
            return False
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    # Add to Database.py
    def get_user_email(self, username):
        """Get the email address for a given username"""
        try:
            query = "SELECT email FROM users WHERE username = ?"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting user email: {e}")
            return None

    def update_verification_token(self, email, jwt_token):
        """Update the verification token for a user"""
        try:
            query = "UPDATE users SET verification_token = ? WHERE email = ?"
            self.cursor.execute(query, (jwt_token, email))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating verification token: {e}")
            return False

    def mark_user_verified(self, email):
        """Mark user as verified after successful OTP validation"""
        try:
            query = "UPDATE users SET verified = 1 WHERE email = ?"
            self.cursor.execute(query, (email,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error marking user as verified: {e}")
            return False

    def check_login(self, username, password):
        """Check login credentials and verification status"""
        try:
            query = """
                SELECT id, verified 
                FROM users 
                WHERE username = ? AND password = ?
            """
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            
            if result:
                user_id, is_verified = result
                if is_verified:
                    return True
                else:
                    return "unverified"
            return False
        except Exception as e:
            print(f"Error checking login: {e}")
            return False
        
    def get_verification_token(self, email):
        """Retrieve the JWT token for email verification"""
        try:
            query = "SELECT verification_token FROM users WHERE email = ?"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving verification token: {e}")
            return None