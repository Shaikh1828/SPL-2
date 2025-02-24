# import sqlite3
# import Database
# from PyQt5.QtWidgets import QMessageBox

# class Authentication:
#     def __init__(self, db_path="users.db"):
#         self.db_path = db_path

#         Database.Database()



#     def validate_user(self, username, password, mode, parent):
#         """Validates user credentials for login or registration."""
#         if not username or not password:
#             QMessageBox.warning(parent, "Input Error", "Username and Password cannot be empty.")
#             return

#         try:
#             conn = sqlite3.connect(self.db_path)
#             cursor = conn.cursor()

#             if mode == "login": 
#                 # Check if the user exists
#                 cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
#                 user = cursor.fetchone()
#                 conn.close()
#                 if user:
#                     QMessageBox.information(parent, "Success", "Login Successful!")
#                     return True  # Return success to open the main window
#                 else:
#                     QMessageBox.warning(parent, "Error", "Invalid credentials.")
#             elif mode == "register":
#                 # Add the user to the database
#                 cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#                 conn.commit()
#                 conn.close()
#                 QMessageBox.information(parent, "Success", "Registration Successful! You can now log in.")
#                 return True  # Return success to switch back to login mode
#         except sqlite3.IntegrityError:
#             QMessageBox.warning(parent, "Error", "Username already exists.")
#         except Exception as e:
#             QMessageBox.critical(parent, "Database Error", f"An error occurred: {e}")

#         return False  # Return failure for invalid credentials or errors


# authentication.py
from PyQt5.QtWidgets import QMessageBox
from Database import Database
import random
import string

class Authentication:
    def __init__(self, db_path="users.db"):
        self.db = Database(db_path)

    def generate_verification_code(self):
        """Generate a 6-character verification code"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    def validate_user(self, username, password, email, mode, parent):
        """Handle user login and registration with email verification"""
        if not username or not password:
            QMessageBox.warning(parent, "Input Error", "Username and Password cannot be empty.")
            return False

        try:
            if mode == "login":
                # Use the enhanced check_login method which now uses 'verified' column
                login_result = self.db.check_login(username, password)
                
                if login_result == True:
                    QMessageBox.information(parent, "Success", "Login Successful!")
                    return True
                elif login_result == "unverified":
                    QMessageBox.warning(parent, "Unverified Account", 
                        "Please verify your email before logging in.")
                    return False
                else:
                    QMessageBox.warning(parent, "Error", "Invalid credentials.")
                    return False

            elif mode == "register":
                if not email:
                    QMessageBox.warning(parent, "Input Error", "Email is required for registration.")
                    return False

                verification_code = self.generate_verification_code()
                
                # Add user with verification code
                if self.db.add_user(username, password, email, verification_code):
                    # For now, we'll simulate email sending with a message box
                    QMessageBox.information(
                        parent,
                        "Verification Required",
                        f"Your verification code is: {verification_code}\nPlease enter this code to verify your account."
                    )
                    return "verify"
                else:
                    QMessageBox.warning(
                        parent,
                        "Registration Error",
                        "Username or email already exists."
                    )
                return False

        except Exception as e:
            QMessageBox.critical(parent, "Error", f"An error occurred: {e}")
            return False

    def verify_email(self, email, verification_code):
        """Verify user's email with the provided code"""
        return self.db.verify_user(email, verification_code)