import sqlite3
import AuthWindow

from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)


# Run Application
app = QApplication([])
auth_window = AuthWindow.AuthWindows()
auth_window.show()
app.exec_()
