from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QMessageBox, QGridLayout, QFrame
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt, pyqtSignal

class Dashboard(QWidget):
    # Signal to notify main window of credential changes
    credentials_updated = pyqtSignal(dict)
    
    def __init__(self, parent=None, user_credentials=None):
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle("User Dashboard")
        self.resize(600, 400)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        # Default credentials if none provided
        self.user_credentials = user_credentials or {"user_id": "", "password": ""}
        
        self.init_ui()
        self.drag_pos = None
        
    def init_ui(self):
        # Title Bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
        title_bar_layout = QHBoxLayout()
        title_label = QLabel("User Dashboard")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
        title_label.setStyleSheet("color: #9BE5FF; padding: 5px;")

        minimize_button = QPushButton("-")
        close_button = QPushButton("X")
        for button in [minimize_button, close_button]:
            button.setFixedSize(30, 30)
            button.setStyleSheet("background-color: rgb(70, 70, 70); color: white; border: none;")
        minimize_button.clicked.connect(self.showMinimized)
        close_button.clicked.connect(self.close)

        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(minimize_button)
        title_bar_layout.addWidget(close_button)
        title_bar.setLayout(title_bar_layout)
        
        # Form Layout
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(240, 248, 255, 200);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        form_layout = QGridLayout()
        
        # User ID Section
        user_id_label = QLabel("User ID:")
        user_id_label.setFont(QFont("Arial", 12))
        user_id_label.setStyleSheet("color: #333; font-weight: bold;")
        
        self.user_id_input = QLineEdit(self.user_credentials["user_id"])
        self.user_id_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #6BC8B4;
                border-radius: 5px;
                padding: 8px;
                font: 12pt Arial;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #FF6987;
            }
        """)
        
        # Password Section
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 12))
        password_label.setStyleSheet("color: #333; font-weight: bold;")
        
        self.password_input = QLineEdit(self.user_credentials["password"])
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #6BC8B4;
                border-radius: 5px;
                padding: 8px;
                font: 12pt Arial;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #FF6987;
            }
        """)
        
        # Show/Hide Password Button
        self.toggle_password_btn = QPushButton("Show")
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #6BC8B4;
                color: black;
                font: bold 10pt Arial;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: rgb(90, 180, 160);
            }
        """)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        # Add to form layout
        form_layout.addWidget(user_id_label, 0, 0)
        form_layout.addWidget(self.user_id_input, 0, 1)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)
        form_layout.addWidget(self.toggle_password_btn, 1, 2)
        
        form_frame.setLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Changes")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #6BC8B4;
                color: black;
                font: bold 12pt Arial;
                border-radius: 10px;
                padding: 8px 16px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: rgb(90, 180, 160);
            }
        """)
        save_button.clicked.connect(self.save_credentials)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 105, 135);
                color: black;
                font: bold 12pt Arial;
                border-radius: 10px;
                padding: 8px 16px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: rgb(235, 85, 115);
            }
        """)
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        # Info section
        info_label = QLabel("Manage your account credentials securely. Your password should be at least 8 characters long and include numbers and special characters.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #555; font-style: italic; padding: 10px;")
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        main_layout.addSpacing(20)
        main_layout.addWidget(form_frame)
        main_layout.addWidget(info_label)
        main_layout.addLayout(button_layout)
        main_layout.addStretch()
        
        self.setLayout(main_layout)
        
        # Apply styles to the entire window
        self.setStyleSheet("""
            QWidget {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:1, 
                                                stop:0 rgba(86, 190, 228, 255), 
                                                stop:1 rgba(10, 90, 170, 255));
            }
        """)
    
    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("Show")
    
    def save_credentials(self):
        user_id = self.user_id_input.text().strip()
        password = self.password_input.text()
        
        # Basic validation
        if not user_id:
            QMessageBox.warning(self, "Input Error", "User ID cannot be empty.")
            return
            
        if len(password) < 8:
            QMessageBox.warning(self, "Input Error", "Password must be at least 8 characters long.")
            return
        
        # Update credentials
        self.user_credentials = {
            "user_id": user_id,
            "password": password
        }
        
        # Emit signal with new credentials
        self.credentials_updated.emit(self.user_credentials)
        
        QMessageBox.information(self, "Success", "Your credentials have been updated successfully.")
        self.close()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()