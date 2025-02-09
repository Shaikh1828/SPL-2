import sqlite3
import AuthWindow

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)


# Initialize Database
# def init_database():
#     try:
#         conn = sqlite3.connect("users.db")
#         cursor = conn.cursor()
#         cursor.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 username TEXT UNIQUE NOT NULL,
#                 password TEXT NOT NULL
#             )
#         """)
#         conn.commit()
#         conn.close()
#         print("Database initialized successfully.")
#     except Exception as e:
#         print(f"Error initializing database: {e}")


# # Initialize Database
# init_database()

# Run Application
app = QApplication([])
auth_window = AuthWindow.AuthWindows()
auth_window.show()
app.exec_()
