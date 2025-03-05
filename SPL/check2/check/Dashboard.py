from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QStackedWidget,
    QLineEdit, QMessageBox, QGridLayout, QFrame, QTableWidgetItem
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from Database import Database


class Dashboard(QWidget):
    credentials_updated = pyqtSignal(dict)
    
    def __init__(self, parent=None, user_credentials=None, database=None):
        super().__init__(parent)
        self.setWindowTitle("User Dashboard")
        self.resize(800, 600)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        
        # Database connection
        self.database = database or Database()
        
        # User credentials
        self.user_credentials = user_credentials or {"id": None, "user_id": "", "password": ""}
        
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
        
        # Section Buttons
        section_layout = QHBoxLayout()
        section_buttons = [
            ("Credentials", self.show_credentials_section),
            ("Analytics", self.show_analytics_section)
        ]
        
        self.section_button_group = []
        for label, method in section_buttons:
            btn = QPushButton(label)
            btn.clicked.connect(method)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
            """)
            section_layout.addWidget(btn)
            self.section_button_group.append(btn)
        
        # Stacked Widget for Sections
        self.stacked_widget = QStackedWidget()
        
        # Credentials Section
        credentials_section = QWidget()
        credentials_layout = QVBoxLayout()
        
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(240, 248, 255, 200);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        form_layout = QGridLayout()
        
        user_id_label = QLabel("User ID:")
        user_id_label.setFont(QFont("Arial", 12))
        user_id_label.setStyleSheet("color: #333; font-weight: bold;")
        
        self.user_id_input = QLineEdit(self.user_credentials.get("user_id", ""))
        
        password_label = QLabel("Password:")
        password_label.setFont(QFont("Arial", 12))
        password_label.setStyleSheet("color: #333; font-weight: bold;")
        
        self.password_input = QLineEdit(self.user_credentials.get("password", ""))
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.toggle_password_btn = QPushButton("Show")
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        form_layout.addWidget(user_id_label, 0, 0)
        form_layout.addWidget(self.user_id_input, 0, 1)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)
        form_layout.addWidget(self.toggle_password_btn, 1, 2)
        
        form_frame.setLayout(form_layout)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_credentials)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        
        update_button = QPushButton("Update Credentials")
        update_button.clicked.connect(self.update_credentials)
        
        history_button = QPushButton("Show History")
        history_button.clicked.connect(self.show_history)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(update_button)
        button_layout.addWidget(history_button)
        button_layout.addWidget(cancel_button)
        
        credentials_layout.addWidget(form_frame)
        credentials_layout.addLayout(button_layout)
        credentials_section.setLayout(credentials_layout)
        
        # Analytics Section
        analytics_section = QWidget()
        analytics_layout = QVBoxLayout()
        
        # Analytics Table
        self.analytics_table = QTableWidget()
        self.analytics_table.setColumnCount(4)
        self.analytics_table.setHorizontalHeaderLabels(["Date", "Action", "Result", "Details"])
        
        refresh_button = QPushButton("Refresh Analytics")
        refresh_button.clicked.connect(self.refresh_analytics)
        
        analytics_layout.addWidget(self.analytics_table)
        analytics_layout.addWidget(refresh_button)
        analytics_section.setLayout(analytics_layout)
        
        # Add Sections to Stacked Widget
        self.stacked_widget.addWidget(credentials_section)
        self.stacked_widget.addWidget(analytics_section)
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        main_layout.addLayout(section_layout)
        main_layout.addWidget(self.stacked_widget)
        
        self.setLayout(main_layout)
        
        # Default to Credentials Section
        self.show_credentials_section()
    
    def show_credentials_section(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def show_analytics_section(self):
        self.stacked_widget.setCurrentIndex(1)
    
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
        
        if not user_id:
            QMessageBox.warning(self, "Input Error", "User ID cannot be empty.")
            return
        
        if len(password) < 8:
            QMessageBox.warning(self, "Input Error", "Password must be at least 8 characters long.")
            return
        
        # If user is logged in and has an ID, use database update
        if self.user_credentials.get("id"):
            success = self.database.update_user_credentials(
                self.user_credentials["id"],
                user_id,
                password
            )
            if success:
                self.user_credentials["user_id"] = user_id
                self.user_credentials["password"] = password
                self.credentials_updated.emit(self.user_credentials)
                QMessageBox.information(self, "Success", "Credentials updated successfully.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Username already taken or update failed.")
        else:
            # If not logged in, just update local credentials
            self.user_credentials = {"user_id": user_id, "password": password}
            self.credentials_updated.emit(self.user_credentials)
            QMessageBox.information(self, "Success", "Your credentials have been updated successfully.")
            self.close()
    
    def update_credentials(self):
        QMessageBox.information(self, "Update", "Updating credentials...")
    
    def show_history(self):
        QMessageBox.information(self, "History", "Displaying history...")
    
    def refresh_analytics(self):
        try:
            # Clear existing table
            self.analytics_table.setRowCount(0)
            
            # Placeholder for actual user-specific analytics
            sample_data = [
                ["2024-03-01", "Login", "Success", "Web Access"],
                ["2024-03-02", "Password Change", "Success", "Security Update"],
                ["2024-03-03", "Failed Login", "Failed", "Incorrect Password"]
            ]
            
            self.analytics_table.setRowCount(len(sample_data))
            for row, data in enumerate(sample_data):
                for col, value in enumerate(data):
                    self.analytics_table.setItem(row, col, QTableWidgetItem(value))
        except Exception as e:
            print(f"Error refreshing analytics: {e}")
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()