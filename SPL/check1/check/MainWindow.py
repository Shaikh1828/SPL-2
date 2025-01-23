from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt
import MLmodel
from scan import Scan

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Droid Scanner")
        self.resize(1000, 600)
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.init_ui()
        self.drag_pos = None  
    
    def init_ui(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 900, 600)
        gradient.setColorAt(0.0, QColor(86, 190, 228))
        gradient.setColorAt(0.5, QColor(10, 90, 170))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Title Bar
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
            button.setStyleSheet("background-color: rgb(70, 70, 70); color: white; border: none;")
        minimize_button.clicked.connect(self.showMinimized)
        close_button.clicked.connect(self.close)

        title_bar_layout.addWidget(title_label)
        title_bar_layout.addStretch()
        title_bar_layout.addWidget(minimize_button)
        title_bar_layout.addWidget(close_button)
        title_bar.setLayout(title_bar_layout)

        # File Upload Section
        upload_label = QLabel("Upload Your File")
        upload_label.setFont(QFont("Arial", 16))
        upload_label.setAlignment(Qt.AlignCenter)
        upload_label.setStyleSheet("font: bold;  margin-top: 20px;")

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

        scan_button = QPushButton("Scan Devices")
        scan_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(90, 180, 160);
                color: black;
                font: bold 15pt Arial;
                border-radius: 10px;
                padding: 8px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: rgb(110, 190, 170);
            }
        """)
        scan_button.clicked.connect(self.open_scan_window)


        # Info Panel
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
        left_layout.addWidget(scan_button)
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

        

    def train_model(self):
        try:
            # Call the MLModel's train_model method
            accuracy, cm = self.ml_model.train_model()

            # Display the results in the text box
            results = f"Model trained successfully!\n\n"
            results += f"Accuracy: {accuracy * 100:.2f}%\n\n"
            results += f"Confusion Matrix:\n{cm}"
            self.results_text.setText(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to train the model: {e}")

    def choose_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*)")
        if file_path:
            self.file_path_label.setText(file_path)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def open_scan_window(self):
        self.scan_window = Scan()
        self.scan_window.show()
