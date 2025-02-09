# Imports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# App Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Droid Scanner")
main_window.resize(800, 500)
main_window.setStyleSheet("QWidget { background-color: rgb(166, 220, 219); }")

# Widgets
title_label = QLabel("Droid Scanner")
title_label.setAlignment(Qt.AlignCenter)
title_label.setFont(QFont("Arial", 20, QFont.Bold))

upload_label = QLabel("Upload Your File")
upload_label.setAlignment(Qt.AlignCenter)
upload_label.setFont(QFont("Arial", 15))

file_path_label = QLabel("No file selected")
file_path_label.setAlignment(Qt.AlignCenter)
file_path_label.setStyleSheet("QLabel { color: rgb(50, 50, 50); font: 12pt Arial; }")

choose_button = QPushButton("Choose File")
choose_button.setStyleSheet("QPushButton { background-color: rgb(107, 200, 180); font: 12pt Arial; padding: 8px; }")

upload_button = QPushButton("Upload")
upload_button.setStyleSheet("QPushButton { background-color: rgb(255, 105, 135); font: 12pt Arial; padding: 8px; }")

max_file_label = QLabel("Max file size: 50MB")
max_file_label.setAlignment(Qt.AlignCenter)
max_file_label.setStyleSheet("QLabel { font: 10pt Arial; color: rgb(100, 100, 100); }")

info_text = QTextEdit()
info_text.setReadOnly(True)
info_text.setText(
    "Droid Scanner is a powerful and easy-to-use Android application designed to scan and analyze the apps "
    "on your device for security, privacy, and performance.\n\n"
    "Key Features:\n"
    "   - Comprehensive App Scan: Detect malicious software, adware, and any apps that could compromise your security.\n"
    "   - Permission Analysis: Review and manage app permissions to protect your privacy.\n"
    "   - Performance Monitoring: Identify apps consuming excessive resources like battery, storage, or RAM.\n\n"
    "App Insights:\n"
    "   - Detailed reports on app origin, updates, and security.\n"
    "   - Real-Time Protection for new installations.\n"
    "   - Uninstallation Recommendations to free up space."
)
info_text.setStyleSheet("QTextEdit { background-color: rgb(240, 248, 255); color: black; font: 11pt Courier; }")

# File Selection Logic
def choose_file():
    file_path, _ = QFileDialog.getOpenFileName(main_window, "Select File", "", "All Files (*)")
    if file_path:
        file_path_label.setText(file_path)

choose_button.clicked.connect(choose_file)

# Layouts
left_layout = QVBoxLayout()
left_layout.addWidget(upload_label)
left_layout.addWidget(choose_button)
left_layout.addWidget(file_path_label)
left_layout.addWidget(upload_button)
left_layout.addWidget(max_file_label)
left_layout.addStretch()

right_layout = QVBoxLayout()
right_layout.addWidget(info_text)

main_layout = QHBoxLayout()
main_layout.addLayout(left_layout, 1)
main_layout.addLayout(right_layout, 2)

# Apply Layout
main_window.setLayout(main_layout)

# Run Application
main_window.show()
app.exec_()
