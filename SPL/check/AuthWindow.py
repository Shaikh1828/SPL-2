import sqlite3
import MainWindow
from Authentication import Authentication  # Import the Authentication class
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt

class AuthWindows(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Register")
        self.resize(500, 300)
        self.setStyleSheet("background-color: #E2F6FD;")
        self.auth = Authentication()  # Initialize the Authentication class
        self.init_ui()
    
    def init_ui(self):
        # Title
        self.title_label = QLabel("Welcome to Droid Scanner")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #1E90FF; ")

        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setFont(QFont("Arial", 12))
        self.username_input.setStyleSheet("background-color: #FFF; padding: 5px; border-radius: 5px;")

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setFont(QFont("Arial", 12))
        self.password_input.setStyleSheet("background-color: #FFF; padding: 5px; border-radius: 5px; margin-bottom:10px")

        # Buttons
        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.validate_user)
        self.submit_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

        self.toggle_button = QPushButton("Switch to Register")
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.toggle_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

        self.show_data_button = QPushButton("Show Database Data")
        self.show_data_button.clicked.connect(self.show_data)
        self.show_data_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.show_data_button)
        self.setLayout(self.layout)
        self.mode = "login"

    def validate_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.auth.validate_user(username, password, self.mode, self):
            if self.mode == "login":
                self.open_main_window()  # Open the main window if login succeeds
            else:
                self.toggle_mode()  # Switch to login mode after registration

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.submit_button.setText("Register")
            self.toggle_button.setText("Switch to Login")
            self.title_label.setText("Register for Droid Scanner")
        else:
            self.mode = "login"
            self.submit_button.setText("Login")
            self.toggle_button.setText("Switch to Register")
            self.title_label.setText("Welcome to Droid Scanner")

    def show_data(self):
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password FROM users")  # Fetching password
            data = cursor.fetchall()
            conn.close()

            # Create a new window for the table
            self.data_window = QWidget()
            self.data_window.setWindowTitle("User Data")
            self.data_window.resize(600, 400)

            # Create a table widget
            self.table = QTableWidget(len(data), 3)  # Number of rows and columns
            self.table.setHorizontalHeaderLabels(["ID", "Username", "Password"])
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only

            # Populate the table with data
            for row_idx, (id_, username, password) in enumerate(data):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(id_)))
                self.table.setItem(row_idx, 1, QTableWidgetItem(username))
                self.table.setItem(row_idx, 2, QTableWidgetItem(password))

            # Layout for the table
            layout = QVBoxLayout()
            layout.addWidget(self.table)
            self.data_window.setLayout(layout)
            self.data_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

    def open_main_window(self):
        self.main_window = MainWindow.MainWindow()
        self.main_window.show()
        self.close()
