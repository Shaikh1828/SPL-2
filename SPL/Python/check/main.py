import sqlite3
import MainWindow

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt

# Initialize Database
def init_database():
    try:
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")

# ---------- Login/Registration Window ----------


# ---------- Main Application Window ----------

# Initialize Database
init_database()

# Run Application
app = QApplication([])
auth_window = AuthWindow()
auth_window.show()
app.exec_()
