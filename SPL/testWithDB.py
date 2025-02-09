import sqlite3
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


def init_database1():
    try:
        conn = sqlite3.connect("app_features.db")
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AppFeatures (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_name TEXT UNIQUE NOT NULL,

                -- Permissions
                SEND_SMS BOOLEAN DEFAULT FALSE,
                READ_PHONE_STATE BOOLEAN DEFAULT FALSE,
                GET_ACCOUNTS BOOLEAN DEFAULT FALSE,
                RECEIVE_SMS BOOLEAN DEFAULT FALSE,
                READ_SMS BOOLEAN DEFAULT FALSE,
                USE_CREDENTIALS BOOLEAN DEFAULT FALSE,
                MANAGE_ACCOUNTS BOOLEAN DEFAULT FALSE,
                WRITE_SMS BOOLEAN DEFAULT FALSE,
                READ_SYNC_SETTINGS BOOLEAN DEFAULT FALSE,
                AUTHENTICATE_ACCOUNTS BOOLEAN DEFAULT FALSE,
                WRITE_HISTORY_BOOKMARKS BOOLEAN DEFAULT FALSE,
                INSTALL_PACKAGES BOOLEAN DEFAULT FALSE,
                CAMERA BOOLEAN DEFAULT FALSE,
                WRITE_SYNC_SETTINGS BOOLEAN DEFAULT FALSE,
                READ_HISTORY_BOOKMARKS BOOLEAN DEFAULT FALSE,
                INTERNET BOOLEAN DEFAULT FALSE,
                RECORD_AUDIO BOOLEAN DEFAULT FALSE,
                NFC BOOLEAN DEFAULT FALSE,
                ACCESS_LOCATION_EXTRA_COMMANDS BOOLEAN DEFAULT FALSE,
                WRITE_APN_SETTINGS BOOLEAN DEFAULT FALSE,
                BIND_REMOTEVIEWS BOOLEAN DEFAULT FALSE,
                READ_PROFILE BOOLEAN DEFAULT FALSE,
                MODIFY_AUDIO_SETTINGS BOOLEAN DEFAULT FALSE,
                READ_SYNC_STATS BOOLEAN DEFAULT FALSE,
                BROADCAST_STICKY BOOLEAN DEFAULT FALSE,
                WAKE_LOCK BOOLEAN DEFAULT FALSE,
                RECEIVE_BOOT_COMPLETED BOOLEAN DEFAULT FALSE,
                RESTART_PACKAGES BOOLEAN DEFAULT FALSE,
                BLUETOOTH BOOLEAN DEFAULT FALSE,
                READ_CALENDAR BOOLEAN DEFAULT FALSE,
                READ_CALL_LOG BOOLEAN DEFAULT FALSE,
                SUBSCRIBED_FEEDS_WRITE BOOLEAN DEFAULT FALSE,
                READ_EXTERNAL_STORAGE BOOLEAN DEFAULT FALSE,
                VIBRATE BOOLEAN DEFAULT FALSE,
                ACCESS_NETWORK_STATE BOOLEAN DEFAULT FALSE,
                SUBSCRIBED_FEEDS_READ BOOLEAN DEFAULT FALSE,
                CHANGE_WIFI_MULTICAST_STATE BOOLEAN DEFAULT FALSE,
                WRITE_CALENDAR BOOLEAN DEFAULT FALSE,
                MASTER_CLEAR BOOLEAN DEFAULT FALSE,
                UPDATE_DEVICE_STATS BOOLEAN DEFAULT FALSE,
                WRITE_CALL_LOG BOOLEAN DEFAULT FALSE,
                DELETE_PACKAGES BOOLEAN DEFAULT FALSE,
                GET_TASKS BOOLEAN DEFAULT FALSE,
                GLOBAL_SEARCH BOOLEAN DEFAULT FALSE,
                DELETE_CACHE_FILES BOOLEAN DEFAULT FALSE,
                WRITE_USER_DICTIONARY BOOLEAN DEFAULT FALSE,
                REORDER_TASKS BOOLEAN DEFAULT FALSE,
                WRITE_PROFILE BOOLEAN DEFAULT FALSE,
                SET_WALLPAPER BOOLEAN DEFAULT FALSE,
                BIND_INPUT_METHOD BOOLEAN DEFAULT FALSE,
                READ_SOCIAL_STREAM BOOLEAN DEFAULT FALSE,
                READ_USER_DICTIONARY BOOLEAN DEFAULT FALSE,
                PROCESS_OUTGOING_CALLS BOOLEAN DEFAULT FALSE,
                CALL_PRIVILEGED BOOLEAN DEFAULT FALSE,
                BIND_WALLPAPER BOOLEAN DEFAULT FALSE,
                RECEIVE_WAP_PUSH BOOLEAN DEFAULT FALSE,
                DUMP BOOLEAN DEFAULT FALSE,
                BATTERY_STATS BOOLEAN DEFAULT FALSE,
                ACCESS_COARSE_LOCATION BOOLEAN DEFAULT FALSE,
                SET_TIME BOOLEAN DEFAULT FALSE,
                WRITE_SOCIAL_STREAM BOOLEAN DEFAULT FALSE,
                WRITE_SETTINGS BOOLEAN DEFAULT FALSE,
                REBOOT BOOLEAN DEFAULT FALSE,
                BLUETOOTH_ADMIN BOOLEAN DEFAULT FALSE,
                BIND_DEVICE_ADMIN BOOLEAN DEFAULT FALSE,
                WRITE_GSERVICES BOOLEAN DEFAULT FALSE,
                KILL_BACKGROUND_PROCESSES BOOLEAN DEFAULT FALSE,
                STATUS_BAR BOOLEAN DEFAULT FALSE,
                PERSISTENT_ACTIVITY BOOLEAN DEFAULT FALSE,
                CHANGE_NETWORK_STATE BOOLEAN DEFAULT FALSE,
                RECEIVE_MMS BOOLEAN DEFAULT FALSE,
                SET_TIME_ZONE BOOLEAN DEFAULT FALSE,
                CONTROL_LOCATION_UPDATES BOOLEAN DEFAULT FALSE,
                BROADCAST_WAP_PUSH BOOLEAN DEFAULT FALSE,
                BIND_ACCESSIBILITY_SERVICE BOOLEAN DEFAULT FALSE,
                ADD_VOICEMAIL BOOLEAN DEFAULT FALSE,
                CALL_PHONE BOOLEAN DEFAULT FALSE,
                BIND_APPWIDGET BOOLEAN DEFAULT FALSE,
                FLASHLIGHT BOOLEAN DEFAULT FALSE,
                READ_LOGS BOOLEAN DEFAULT FALSE,
                SET_PROCESS_LIMIT BOOLEAN DEFAULT FALSE,
                MOUNT_UNMOUNT_FILESYSTEMS BOOLEAN DEFAULT FALSE,
                BIND_TEXT_SERVICE BOOLEAN DEFAULT FALSE,
                INSTALL_LOCATION_PROVIDER BOOLEAN DEFAULT FALSE,
                SYSTEM_ALERT_WINDOW BOOLEAN DEFAULT FALSE,
                MOUNT_FORMAT_FILESYSTEMS BOOLEAN DEFAULT FALSE,
                CHANGE_CONFIGURATION BOOLEAN DEFAULT FALSE,
                CLEAR_APP_USER_DATA BOOLEAN DEFAULT FALSE,
                CHANGE_WIFI_STATE BOOLEAN DEFAULT FALSE,
                READ_FRAME_BUFFER BOOLEAN DEFAULT FALSE,
                ACCESS_SURFACE_FLINGER BOOLEAN DEFAULT FALSE,
                BROADCAST_SMS BOOLEAN DEFAULT FALSE,
                EXPAND_STATUS_BAR BOOLEAN DEFAULT FALSE,
                INTERNAL_SYSTEM_WINDOW BOOLEAN DEFAULT FALSE,
                SET_ACTIVITY_WATCHER BOOLEAN DEFAULT FALSE,
                WRITE_CONTACTS BOOLEAN DEFAULT FALSE,
                BIND_VPN_SERVICE BOOLEAN DEFAULT FALSE,
                DISABLE_KEYGUARD BOOLEAN DEFAULT FALSE,
                ACCESS_MOCK_LOCATION BOOLEAN DEFAULT FALSE,
                GET_PACKAGE_SIZE BOOLEAN DEFAULT FALSE,
                MODIFY_PHONE_STATE BOOLEAN DEFAULT FALSE,
                CHANGE_COMPONENT_ENABLED_STATE BOOLEAN DEFAULT FALSE,
                CLEAR_APP_CACHE BOOLEAN DEFAULT FALSE,
                SET_ORIENTATION BOOLEAN DEFAULT FALSE,
                READ_CONTACTS BOOLEAN DEFAULT FALSE,
                DEVICE_POWER BOOLEAN DEFAULT FALSE,
                HARDWARE_TEST BOOLEAN DEFAULT FALSE,
                ACCESS_WIFI_STATE BOOLEAN DEFAULT FALSE,
                WRITE_EXTERNAL_STORAGE BOOLEAN DEFAULT FALSE,
                ACCESS_FINE_LOCATION BOOLEAN DEFAULT FALSE,
                SET_WALLPAPER_HINTS BOOLEAN DEFAULT FALSE,
                SET_PREFERRED_APPLICATIONS BOOLEAN DEFAULT FALSE,
                WRITE_SECURE_SETTINGS BOOLEAN DEFAULT FALSE,

                -- Intents
                BOOT_COMPLETED BOOLEAN DEFAULT FALSE,
                PACKAGE_REPLACED BOOLEAN DEFAULT FALSE,
                SEND_MULTIPLE BOOLEAN DEFAULT FALSE,
                TIME_SET BOOLEAN DEFAULT FALSE,
                PACKAGE_REMOVED BOOLEAN DEFAULT FALSE,
                TIMEZONE_CHANGED BOOLEAN DEFAULT FALSE,
                ACTION_POWER_DISCONNECTED BOOLEAN DEFAULT FALSE,
                PACKAGE_ADDED BOOLEAN DEFAULT FALSE,
                ACTION_SHUTDOWN BOOLEAN DEFAULT FALSE,
                PACKAGE_DATA_CLEARED BOOLEAN DEFAULT FALSE,
                PACKAGE_CHANGED BOOLEAN DEFAULT FALSE,
                NEW_OUTGOING_CALL BOOLEAN DEFAULT FALSE,
                SENDTO BOOLEAN DEFAULT FALSE,
                CALL BOOLEAN DEFAULT FALSE,
                SCREEN_ON BOOLEAN DEFAULT FALSE,
                BATTERY_OKAY BOOLEAN DEFAULT FALSE,
                PACKAGE_RESTARTED BOOLEAN DEFAULT FALSE,
                CALL_BUTTON BOOLEAN DEFAULT FALSE,
                SCREEN_OFF BOOLEAN DEFAULT FALSE,
                RUN BOOLEAN DEFAULT FALSE,
                SET_WALLPAPER BOOLEAN DEFAULT FALSE,
                BATTERY_LOW BOOLEAN DEFAULT FALSE,
                ACTION_POWER_CONNECTED BOOLEAN DEFAULT FALSE
            )
        """)
        conn.commit()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing database: {e}")
 

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
        self.title_label.setStyleSheet("color: #1E90FF; ")


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
        self.password_input.setStyleSheet("background-color: #FFF; padding: 5px; border-radius: 5px; margin-bottom:10px")

        # Buttons
        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.validate_user)
        self.submit_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

        self.toggle_button = QPushButton("Switch to Register")
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.toggle_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

        self.show_data_button = QPushButton("Show Database Data")
        self.show_data_button.clicked.connect(self.show_data)
        self.show_data_button.setStyleSheet("background-color: #FFF; font:16px; padding: 5px; border-radius: 5px;")

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.toggle_button)
        self.layout.addWidget(self.show_data_button)
        self.setLayout(self.layout)
        self.mode = "login"

    def validate_user(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if not username or not password:
            QMessageBox.warning(self, "Input Error", "Username and Password cannot be empty.")
            return

        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()

            if self.mode == "login":
                cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
                user = cursor.fetchone()
                conn.close()
                if user:
                    QMessageBox.information(self, "Success", "Login Successful!")
                    self.open_main_window()
                else:
                    QMessageBox.warning(self, "Error", "Invalid credentials.")
            elif self.mode == "register":
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                conn.commit()
                conn.close()
                QMessageBox.information(self, "Success", "Registration Successful! You can now log in.")
                self.toggle_mode()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")

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

    def show_data(self):
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            cursor.execute("SELECT id, username, password FROM users")  # Fetching password
            data = cursor.fetchall()
            conn.close()

            # Create a new window for the table
            self.data_window = QWidget()
            self.data_window.setWindowTitle("User Data")
            self.data_window.resize(600, 400)

            # Create a table widget
            self.table = QTableWidget(len(data), 3)  # Number of rows and columns
            self.table.setHorizontalHeaderLabels(["ID", "Username", "Password"])
            self.table.setEditTriggers(QTableWidget.NoEditTriggers)  # Make table read-only

            # Populate the table with data
            for row_idx, (id_, username, password) in enumerate(data):
                self.table.setItem(row_idx, 0, QTableWidgetItem(str(id_)))
                self.table.setItem(row_idx, 1, QTableWidgetItem(username))
                self.table.setItem(row_idx, 2, QTableWidgetItem(password))

            # Layout for the table
            layout = QVBoxLayout()
            layout.addWidget(self.table)
            self.data_window.setLayout(layout)
            self.data_window.show()
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"An error occurred: {e}")


    def open_main_window(self):
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

# Initialize Database
init_database()
init_database1()

# Run Application
app = QApplication([])
auth_window = AuthWindow()
auth_window.show()
app.exec_()
