# pip3 install pyqt5
# pip3 install pillow
# pip3 install matpoltlib

# Imports
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit
)
from PyQt5.QtGui import QFont, QIcon, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt, QEvent

# App Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Droid Scanner")
main_window.resize(1000, 600)
main_window.setWindowFlags(Qt.FramelessWindowHint)  # Remove default title bar

# Custom Gradient Background
palette = QPalette()
gradient = QLinearGradient(0, 0, 900, 600)
gradient.setColorAt(0.0, QColor(86, 190, 228))  # Dark Slate Blue
gradient.setColorAt(0.5, QColor(10, 90, 170))  # Medium Slate Blue
palette.setBrush(QPalette.Window, QBrush(gradient))
main_window.setPalette(palette)

# Custom Title Bar
title_bar = QWidget()
title_bar.setStyleSheet("background-color: rgb(50, 50, 50); color: black;")
title_bar_layout = QHBoxLayout()
title_label = QLabel("Droid Scanner :")
title_label.setFont(QFont("Arial", 18, QFont.Bold))
title_label.setStyleSheet("color: #9BE5FF; padding: 5px;")

# Minimize and Close Buttons
minimize_button = QPushButton("-")
close_button = QPushButton("X")

for button in [minimize_button, close_button]:
    button.setFixedSize(30, 30)
    button.setStyleSheet("""
        QPushButton {
            background-color: rgb(70, 70, 70);
            color: black;
            border: none;
        }
        QPushButton:hover {
            background-color: rgb(100, 100, 100);
        }
    """)

minimize_button.clicked.connect(main_window.showMinimized)
close_button.clicked.connect(main_window.close)

# Add Widgets to Title Bar
title_bar_layout.addWidget(title_label)
title_bar_layout.addStretch()
title_bar_layout.addWidget(minimize_button)
title_bar_layout.addWidget(close_button)
title_bar.setLayout(title_bar_layout)

# File Upload Widgets
upload_label = QLabel("Upload Your File")
upload_label.setAlignment(Qt.AlignCenter)
upload_label.setFont(QFont("Arial", 16))
upload_label.setStyleSheet("color: #000; margin-top: 20px;")

file_path_label = QLabel("No file selected")
file_path_label.setAlignment(Qt.AlignCenter)
file_path_label.setStyleSheet("color:#FFF; font: 12pt Arial; font-style: italic;")

choose_button = QPushButton("Choose File")
choose_button.setStyleSheet("""
    QPushButton {
        background-color: rgb(107, 200, 180);
        color: black;
        font: bold 15pt Arial ;
        border-radius: 10px;
        padding: 8px;
    }
    QPushButton:hover {
        background-color: rgb(90, 180, 160);
    }
""")

upload_button = QPushButton("Upload")
upload_button.setStyleSheet("""
    QPushButton {
        background-color: rgb(255, 105, 135);
        color: black;
        font: bold 15pt Arial;
        border-radius: 10px;
        padding: 8px;
        margin-top: 20px
    }
    QPushButton:hover {
        background-color: rgb(235, 85, 115);
    }
""")

upload_file_label = QLabel("Upload to scan")
upload_file_label.setAlignment(Qt.AlignCenter)
upload_file_label.setStyleSheet("color:#FFF; font: 12pt Arial; font-style: italic;")

info_text = QTextEdit()
info_text.setReadOnly(True)
info_text.setText(
    "   Droid Scanner is a powerful and easy-to-use Android application designed to scan and analyze the apps "
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
info_text.setStyleSheet("""
    QTextEdit {
        background-color: rgba(240, 248, 255, 200);
        color: black;
        font: 11pt Courier;
        border-radius: 10px;
        padding: 10px;
    }
""")

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
left_layout.addWidget(upload_file_label)
left_layout.addStretch()

right_layout = QVBoxLayout()
right_layout.addWidget(info_text)

main_layout = QVBoxLayout()
main_layout.addWidget(title_bar)
content_layout = QHBoxLayout()
content_layout.addLayout(left_layout, 1)
content_layout.addLayout(right_layout, 2)

main_layout.addLayout(content_layout)

# Apply Layout
main_window.setLayout(main_layout)

# Event to allow window dragging
def mousePressEvent(event):
    main_window.drag_pos = event.globalPos()

def mouseMoveEvent(event):
    try:
        delta = event.globalPos() - main_window.drag_pos
        main_window.move(main_window.x() + delta.x(), main_window.y() + delta.y())
        main_window.drag_pos = event.globalPos()
    except AttributeError:
        pass

main_window.mousePressEvent = mousePressEvent
main_window.mouseMoveEvent = mouseMoveEvent

# Run Application
main_window.show()
app.exec_()