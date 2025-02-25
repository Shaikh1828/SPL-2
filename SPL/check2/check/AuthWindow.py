# import sqlite3
# import MainWindow
# from Authentication import Authentication  # Import the Authentication class
# from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem
# from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor
# from PyQt5.QtCore import Qt

# class AuthWindows(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Login/Register")
#         self.resize(500, 300)
#         self.setStyleSheet("background-color: #E2F6FD;")
#         self.auth = Authentication()  # Initialize the Authentication class
#         self.init_ui()
    
#     def init_ui(self):
#         # Title
#         self.title_label = QLabel("Welcome to Droid Scanner")
#         self.title_label.setAlignment(Qt.AlignCenter)
#         self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
#         self.title_label.setStyleSheet("color: #1E90FF; ")

#         # Username Input
#         self.username_input = QLineEdit()
#         self.username_input.setPlaceholderText("Enter Username")
#         self.username_input.setFont(QFont("Arial", 12))
#         self.username_input.setStyleSheet("background-color: #FFF; padding: 5px; border-radius: 5px;")

#         # Password Input
#         self.password_input = QLineEdit()
#         self.password_input.setPlaceholderText("Enter Password")
#         self.password_input.setEchoMode(QLineEdit.Password)
#         self.password_input.setFont(QFont("Arial", 12))
#         self.password_input.setStyleSheet("background-color: #FFF; padding: 5px; border-radius: 5px; margin-bottom:10px")

#         # Buttons
#         self.submit_button = QPushButton("Login")
#         self.submit_button.clicked.connect(self.validate_user)
#         self.submit_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

#         self.toggle_button = QPushButton("Switch to Register")
#         self.toggle_button.clicked.connect(self.toggle_mode)
#         self.toggle_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

#         self.show_data_button = QPushButton("Show Database Data")
#         self.show_data_button.clicked.connect(self.show_data)
#         self.show_data_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

#         # Layout
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.title_label)
#         self.layout.addWidget(self.username_input)
#         self.layout.addWidget(self.password_input)
#         self.layout.addWidget(self.submit_button)
#         self.layout.addWidget(self.toggle_button)
#         self.layout.addWidget(self.show_data_button)
#         self.setLayout(self.layout)
#         self.mode = "login"

#     def validate_user(self):
#         username = self.username_input.text()
#         password = self.password_input.text()

#         if self.auth.validate_user(username, password, self.mode, self):
#             if self.mode == "login":
#                 self.open_main_window()  # Open the main window if login succeeds
#             else:
#                 self.toggle_mode()  # Switch to login mode after registration

#     def toggle_mode(self):
#         if self.mode == "login":
#             self.mode = "register"
#             self.submit_button.setText("Register")
#             self.toggle_button.setText("Switch to Login")
#             self.title_label.setText("Register for Droid Scanner")
#         else:
#             self.mode = "login"
#             self.submit_button.setText("Login")
#             self.toggle_button.setText("Switch to Register")
#             self.title_label.setText("Welcome to Droid Scanner")

#     def show_data(self):
#         try:
#             conn = sqlite3.connect("users.db")
#             cursor = conn.cursor()
#             cursor.execute("SELECT id, username, password FROM users")  # Fetching password
#             data = cursor.fetchall()
#             conn.close()

#             # Create a new window for the table
#             self.data_window = QWidget()
#             self.data_window.setWindowTitle("User Data")
#             self.data_window.resize(600, 400)

#             # Create a table widget
#             self.table = QTableWidget(len(data), 3)  # Number of rows and columns
#             self.table.setHorizontalHeaderLabels(["ID", "Username", "Password"])
#             self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only

#             # Populate the table with data
#             for row_idx, (id_, username, password) in enumerate(data):
#                 self.table.setItem(row_idx, 0, QTableWidgetItem(str(id_)))
#                 self.table.setItem(row_idx, 1, QTableWidgetItem(username))
#                 self.table.setItem(row_idx, 2, QTableWidgetItem(password))

#             # Layout for the table
#             layout = QVBoxLayout()
#             layout.addWidget(self.table)
#             self.data_window.setLayout(layout)
#             self.data_window.show()
#         except Exception as e:
#             QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

#     def open_main_window(self):
#         self.main_window = MainWindow.MainWindow()
#         self.main_window.show()
#         self.close()




# auth_windows.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, 
    QMessageBox, QDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Authentication import Authentication
from Database import Database

class VerificationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Email Verification")
        self.setFixedWidth(300)
        
        layout = QVBoxLayout()
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter verification code")
        
        verify_button = QPushButton("Verify")
        verify_button.clicked.connect(self.accept)
        
        layout.addWidget(QLabel("Please enter the verification code sent to your email:"))
        layout.addWidget(self.code_input)
        layout.addWidget(verify_button)
        
        self.setLayout(layout)

    def get_code(self):
        return self.code_input.text()

class AuthWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Register")
        self.resize(500, 300)
        self.setStyleSheet("background-color: #E2F6FD;")
        Database()
        self.auth = Authentication()
        self.init_ui()
    
    def init_ui(self):
        # Title
        self.title_label = QLabel("Welcome to Droid Scanner")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #1E90FF;")

        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px;"
        )

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px;"
        )

        # Email Input (initially hidden)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email")
        self.email_input.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px;"
        )
        self.email_input.hide()

        # Buttons
        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.validate_user)
        self.submit_button.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px;"
        )

        self.toggle_button = QPushButton("Switch to Register")
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.toggle_button.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px;"
        )

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.toggle_button)
        self.setLayout(self.layout)
        
        self.mode = "login"
        self.current_email = None

    def validate_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text() if self.mode == "register" else None

        result = self.auth.validate_user(username, password, email, self.mode, self)
        
        if result == "verify":
            self.current_email = email
            dialog = VerificationDialog(self)
            if dialog.exec_() == QDialog.Accepted:
                verification_code = dialog.get_code()
                if self.auth.verify_email(email, verification_code):
                    QMessageBox.information(
                        self,
                        "Success",
                        "Email verified successfully! You can now login."
                    )
                    self.toggle_mode()  # Switch back to login
                else:
                    QMessageBox.warning(
                        self,
                        "Error",
                        "Invalid or expired verification code."
                    )
        elif result:
            if self.mode == "login":
                self.open_main_window()

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.submit_button.setText("Register")
            self.toggle_button.setText("Switch to Login")
            self.title_label.setText("Register for Droid Scanner")
            self.email_input.show()
        else:
            self.mode = "login"
            self.submit_button.setText("Login")
            self.toggle_button.setText("Switch to Register")
            self.title_label.setText("Welcome to Droid Scanner")
            self.email_input.hide()

    def open_main_window(self):
        from MainWindow import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()