import sqlite3
import Database
from PyQt5.QtWidgets import QMessageBox

class Authentication:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path

        Database.Database.init_database(self)



    def validate_user(self, username, password, mode, parent):
        """Validates user credentials for login or registration."""
        if not username or not password:
            QMessageBox.warning(parent, "Input Error", "Username and Password cannot be empty.")
            return

        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            if mode == "login": 
                # Check if the user exists
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = cursor.fetchone()
                conn.close()
                if user:
                    QMessageBox.information(parent, "Success", "Login Successful!")
                    return True  # Return success to open the main window
                else:
                    QMessageBox.warning(parent, "Error", "Invalid credentials.")
            elif mode == "register":
                # Add the user to the database
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                conn.close()
                QMessageBox.information(parent, "Success", "Registration Successful! You can now log in.")
                return True  # Return success to switch back to login mode
        except sqlite3.IntegrityError:
            QMessageBox.warning(parent, "Error", "Username already exists.")
        except Exception as e:
            QMessageBox.critical(parent, "Database Error", f"An error occurred: {e}")

        return False  # Return failure for invalid credentials or errors
