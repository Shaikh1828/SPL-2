import sqlite3
from PyQt5.QtWidgets import QApplication
import AuthWindow
import MainWindow  # Ensure MainWindow contains your MainWindow class.

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


# ---------- Main Application Flow ----------
if __name__ == "__main__":
    # Initialize Database
    init_database()

    # Run Application
    app = QApplication([])

    # Launch Authentication Window
    auth_window = AuthWindow.AuthWindows()
    
    # Handle successful login to show Main Window
    def on_login_success():
        auth_window.close()
        main_window = MainWindow.MainWindow()  # Load MainWindow
        main_window.show()

    # Connect login success signal to on_login_success
    # auth_window.login_success.connect(on_login_success)  # Ensure `login_success` is defined in AuthWindows

    auth_window.show()
    app.exec_()
