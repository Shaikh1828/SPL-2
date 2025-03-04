import sqlite3
from PyQt5.QtWidgets import QMessageBox
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_path="D:\\Git\\SPL-2\\SPL\\check2\\check\\users.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.check_and_update_schema()

    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'connection'):
            self.connection.close()

    def check_and_update_schema(self):
        """Check and update database schema"""
        try:
            # Check if users table exists
            self.cursor.execute("""
                SELECT name FROM sqlite_master WHERE type='table' AND name='users'
            """)
            if not self.cursor.fetchone():
                # Create users table if not exists
                self.cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        verified INTEGER DEFAULT 0,
                        verification_token TEXT,
                        user_type TEXT DEFAULT 'personal',
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.connection.commit()
                print("Users table created successfully.")
            else:
                # Ensure required columns exist
                self.cursor.execute("PRAGMA table_info(users)")
                columns = [column[1] for column in self.cursor.fetchall()]
                
                if 'user_type' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN user_type TEXT DEFAULT 'personal'")
                
                self.connection.commit()
                print("User table schema updated successfully.")
        except Exception as e:
            print(f"Error updating database schema: {e}")

    def hash_password(self, password):
        """Hash the password before storing it"""
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, email, verification_token, user_type="personal"):
        """Add a new user to the database"""
        try:
            # Check if username already exists
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone():
                print("Username already exists!")
                return False
            
            # Check if email already exists
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone():
                print("Email already exists!")
                return False

            # Hash password before storing
            hashed_password = self.hash_password(password)

            # Insert user into database
            self.cursor.execute(
                "INSERT INTO users (username, password, email, verification_token, verified, user_type) VALUES (?, ?, ?, ?, ?, ?)",
                (username, hashed_password, email, verification_token, 0, user_type)
            )
            self.connection.commit()
            print(f"User {username} added successfully.")
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def check_login(self, username, password):
        """Check login credentials and verification status"""
        try:
            hashed_password = self.hash_password(password)
            query = "SELECT id, verified FROM users WHERE username = ? AND password = ?"
            self.cursor.execute(query, (username, hashed_password))
            result = self.cursor.fetchone()
            
            if result:
                user_id, is_verified = result
                return True if is_verified else "unverified"
            return False
        except Exception as e:
            print(f"Error checking login: {e}")
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

    def store_apk_in_db( apk_path, package_name):
        """Store APK file in database"""
        try:
            with open(apk_path, 'rb') as file:
                apk_data = file.read()

            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO App (Package_Name, Name, Version, Status, APK_File) VALUES (?, ?, ?, ?, ?)",
                           (package_name, package_name, "2.1.0", "Benign", apk_data))
            app_id=cursor.lastrowid
            conn.commit()
            conn.close()
            print(f"APK for {package_name} stored successfully.")
            return app_id
        except Exception as e:
            print(f"Error storing APK in database: {e}")

    def get_user_email(self, username):
        """Get the email for a given username"""
        try:
            self.cursor.execute("SELECT email FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting user email: {e}")
            return None

    def get_user_type(self, username):
        """Get the user type for a specific username"""
        try:
            self.cursor.execute("SELECT user_type FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            return result[0] if result else "personal"
        except Exception as e:
            print(f"Error getting user type: {e}")
            return "personal"

    def update_user_credentials(self, user_id, new_username, new_password):
        """Update user's username and password in the database"""
        try:
            # Check if new_username is already taken by another user
            self.cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (new_username, user_id))
            if self.cursor.fetchone():
                print("Username already exists!")
                return False

            hashed_password = self.hash_password(new_password)
            self.cursor.execute(
                "UPDATE users SET username = ?, password = ? WHERE id = ?",
                (new_username, hashed_password, user_id)
            )
            self.connection.commit()
            print("User credentials updated successfully.")
            return True
        except Exception as e:
            print(f"Error updating user credentials: {e}")
            return False
        
    def save_credentials(self):
        new_username = self.user_id_input.text().strip()
        new_password = self.password_input.text()
        
        # Basic validation
        if not new_username:
            QMessageBox.warning(self, "Input Error", "User ID cannot be empty.")
            return
            
        
        # Update credentials in the database
        if self.database:
            success = self.database.update_user_credentials(
                self.user_credentials["id"],  # Use the user's database ID
                new_username,
                new_password
            )
            if success:
                # Update local credentials and notify parent
                self.user_credentials["user_id"] = new_username
                self.user_credentials["password"] = new_password
                self.credentials_updated.emit(self.user_credentials)
                QMessageBox.information(self, "Success", "Credentials updated successfully.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Username already taken.")
        else:
            QMessageBox.warning(self, "Error", "Database connection not available.")