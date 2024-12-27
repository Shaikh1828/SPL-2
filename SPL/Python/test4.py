# Imports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QLineEdit, QMessageBox
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QEvent

# Application
app = QApplication([])

# ---------- Login/Registration Window ----------
class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login/Register")
        self.resize(500, 300)
        self.setStyleSheet("background-color: #E2F6FD;")
        self.init_ui()
    
    def init_ui(self):
        # Title
        self.title_label = QLabel("Welcome to Droid Scanner")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #1E90FF; margin-bottom: 20px;")

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
        self.password_input.setStyleSheet("background-color: #FFF; padding: 5px; border-radius: 5px;")

        # Buttons
        self.submit_button = QPushButton("Login")
        self.submit_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.submit_button.setStyleSheet("background-color: #00BFFF; color: white; padding: 8px; border-radius: 5px;")
        self.submit_button.clicked.connect(self.validate_user)

        self.toggle_button = QPushButton("Switch to Register")
        self.toggle_button.setFlat(True)
        self.toggle_button.setStyleSheet("color: #1E90FF; text-decoration: underline;")
        self.toggle_button.clicked.connect(self.toggle_mode)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.toggle_button)
        self.layout.addStretch()

        self.setLayout(self.layout)
        self.mode = "login"

    def validate_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and Password cannot be empty.")
            return

        if self.mode == "login":
            # Dummy validation (replace with actual backend logic)
            if username == "1" and password == "1":
                QMessageBox.information(self, "Success", "Login Successful!")
                self.open_main_window()
            else:
                QMessageBox.warning(self, "Error", "Invalid credentials.")
        elif self.mode == "register":
            QMessageBox.information(self, "Success", "Registration Successful! You can now log in.")
            self.toggle_mode()

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

    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

# ---------- Main Application Window ----------
# ---------- Main Application Window ----------
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Droid Scanner")
        self.resize(1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui()
        self.drag_pos = None  # To track dragging position
    
    def init_ui(self):
        # Gradient Background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 900, 600)
        gradient.setColorAt(0.0, QColor(86, 190, 228))
        gradient.setColorAt(0.5, QColor(10, 90, 170))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Custom Title Bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
        title_bar_layout = QHBoxLayout()
        title_label = QLabel("Droid Scanner")
        title_label.setFont(QFont("Arial", 18, QFont.Bold))
        title_label.setStyleSheet("color: #9BE5FF; padding: 5px;")

        minimize_button = QPushButton("-")
        close_button = QPushButton("X")
        for button in [minimize_button, close_button]:
            button.setFixedSize(30, 30)
            button.setStyleSheet("""
                QPushButton {
                    background-color: rgb(70, 70, 70);
                    color: white;
                    border: none;
                }
                QPushButton:hover {
                    background-color: rgb(100, 100, 100);
                }
            """)
        minimize_button.clicked.connect(self.showMinimized)
        close_button.clicked.connect(self.close)

        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(minimize_button)
        title_bar_layout.addWidget(close_button)
        title_bar.setLayout(title_bar_layout)

        # Enable dragging for the title bar
        title_bar.mousePressEvent = self.mousePressEvent
        title_bar.mouseMoveEvent = self.mouseMoveEvent

        # File Upload Section
        upload_label = QLabel("Upload Your File")
        upload_label.setFont(QFont("Arial", 16))
        upload_label.setAlignment(Qt.AlignCenter)
        upload_label.setStyleSheet("font: bold; color: white; margin-top: 20px;")

        choose_button = QPushButton("Choose File")
        choose_button.clicked.connect(self.choose_file)
        choose_button.setStyleSheet("""
            QPushButton {
                background-color: #6BC8B4;
                color: black;
                font: bold 15pt Arial;
                border-radius: 10px;
                padding: 8px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: rgb(90, 180, 160);
            }
        """)

        self.file_path_label = QLabel("No file selected")
        self.file_path_label.setAlignment(Qt.AlignCenter)
        self.file_path_label.setStyleSheet("color: white; font-style: italic;")

        upload_button = QPushButton("Upload")
        upload_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 105, 135);
                color: black;
                font: bold 15pt Arial;
                border-radius: 10px;
                padding: 8px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: rgb(235, 85, 115);
            }
        """)

        # Information Panel
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setText(
            "   Droid Scanner is a powerful and easy-to-use Android application designed to scan and analyze "
            "the apps on your device for security, privacy, and performance.\n\n"
            "Key Features:\n"
            "   - Comprehensive App Scan: Detect malicious software, adware, and any apps that could compromise your security.\n"
            "   - Permission Analysis: Review and manage app permissions to protect your privacy.\n"
            "   - Performance Monitoring: Identify apps consuming excessive resources like battery, storage, or RAM.\n\n"
            "App Insights:\n"
            "   - Detailed reports on app origin, updates, and security.\n"
            "   - Real-Time Protection for new installations.\n"
            "   - Uninstallation Recommendations to free up space."
        )
        info_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(240, 248, 255, 200);
                color: black;
                font: 11pt Courier;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(upload_label)
        left_layout.addWidget(choose_button)
        left_layout.addWidget(self.file_path_label)
        left_layout.addWidget(upload_button)
        left_layout.addStretch()

        right_layout = QVBoxLayout()
        right_layout.addWidget(info_text)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        content_layout = QHBoxLayout()
        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 2)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.file_path_label.setText(file_path)

    # Mouse Event Handlers for Window Dragging
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()


# ---------- Run Application ----------
auth_window = AuthWindow()
auth_window.show()
app.exec_()
