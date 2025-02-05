import sqlite3
import Database
from PyQt5.QtWidgets import QMessageBox

class Authentication:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path

        Database.Database()



    def validate_user(self, username, password, mode, parent):
        """Validates user credentials for login or registration."""
        if not username or not password:
            QMessageBox.warning(parent, "Input Error", "Username and Password cannot be empty.")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if mode == "login":
                if self.login_user(username, password, parent, cursor, conn):
                    return True
            elif mode == "register":
                if self.register_user(username, password, parent, cursor, conn):
                    return True
                
        except sqlite3.IntegrityError:
            QMessageBox.warning(parent, "Error", "Username already exists.")
        except Exception as e:
            QMessageBox.critical(parent, "Database Error", f"An error occurred: {e}")

        return False  

    def login_user(self, username, password, parent, cursor, conn):
        """Handles the login functionality."""
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            QMessageBox.information(parent, "Success", "Login Successful!")
            return True  # Indicate success to proceed to the main window
        else:
            QMessageBox.warning(parent, "Error", "Invalid credentials.")
            return False  # Indicate failure to prevent navigation

    def register_user(self, username, password, parent, cursor, conn):
    
        try:
            # Add the user to the database
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            conn.close()
            QMessageBox.information(parent, "Success", "Registration Successful! You can now log in.")
            return True  # Indicate success to switch to login mode
        except Exception as e:
            conn.close()
            QMessageBox.warning(parent, "Error", f"Registration failed: {e}")
            return False  # Indicate failure if registration fails
