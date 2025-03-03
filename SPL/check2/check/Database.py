import sqlite3
from PyQt5.QtWidgets import QMessageBox, QWidget

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.init_AppDatabase()
        self.init_UserDatabase()

    def init_UserDatabase(self):
        """Initializes the database and creates the `users` table if it doesn't exist."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            cursor.execute("ATTACH DATABASE 'app_data.db' AS app_db;")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Scans (
                    Scan_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    User_ID INTEGER,
                    App_ID INTEGER,
                    Scan_Timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (User_ID) REFERENCES users(id)
                )
            """)
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"User Database initialization error: {e}")

    def init_AppDatabase(self):
        try:
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS App (
                    App_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Package_Name TEXT NOT NULL,
                    Name TEXT NOT NULL,
                    Version TEXT,
                    Status TEXT,
                    APK_File BLOB
                )
            """)
        
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Permissions_Intents (
                    Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Feature_Name TEXT NOT NULL
                )
            """)
            dataset_features = [
                ("SYSTEM_ALERT_WINDOW",), ("CHANGE_WIFI_STATE",), ("BIND_ACCESSIBILITY_SERVICE",), ("CALL",), ("UPDATE_DEVICE_STATS",),
                ("ACCESS_WIFI_STATE",), ("BROADCAST_SMS",), ("READ_SOCIAL_STREAM",), ("CHANGE_CONFIGURATION",), ("SEND_MULTIPLE",),
                ("READ_PROFILE",), ("BOOT_COMPLETED",), ("KILL_BACKGROUND_PROCESSES",), ("WRITE_APN_SETTINGS",), ("STATUS_BAR",), ("RUN",),
                ("CLEAR_APP_CACHE",), ("ADD_VOICEMAIL",), ("TIME_SET",), ("SUBSCRIBED_FEEDS_WRITE",), ("GET_ACCOUNTS",), ("WRITE_USER_DICTIONARY",),
                ("INSTALL_PACKAGES",), ("SCREEN_ON",), ("RECORD_AUDIO",), ("RESTART_PACKAGES",), ("DISABLE_KEYGUARD",), ("READ_SYNC_SETTINGS",),
                ("WRITE_GSERVICES",), ("RECEIVE_WAP_PUSH",), ("CALL_PRIVILEGED",), ("SET_PROCESS_LIMIT",), ("ACCESS_NETWORK_STATE",),
                ("BIND_VPN_SERVICE",), ("ACTION_POWER_CONNECTED",), ("BROADCAST_WAP_PUSH",), ("CONTROL_LOCATION_UPDATES",), ("WRITE_PROFILE",),
                ("WRITE_SECURE_SETTINGS",), ("CALL_BUTTON",), ("WRITE_EXTERNAL_STORAGE",), ("REORDER_TASKS",), ("SCREEN_OFF",),
                ("ACTION_POWER_DISCONNECTED",), ("BLUETOOTH_ADMIN",), ("ACCESS_FINE_LOCATION",), ("FLASHLIGHT",), ("WRITE_SYNC_SETTINGS",),
                ("PACKAGE_REPLACED",), ("SET_WALLPAPER",), ("PACKAGE_DATA_CLEARED",), ("SET_WALLPAPER_HINTS",), ("CAMERA",), ("BIND_WALLPAPER",),
                ("BROADCAST_STICKY",), ("WRITE_SOCIAL_STREAM",), ("READ_EXTERNAL_STORAGE",), ("READ_SYNC_STATS",), ("READ_CALL_LOG",),
                ("PERSISTENT_ACTIVITY",), ("WRITE_CALL_LOG",), ("EXPAND_STATUS_BAR",), ("SET_TIME_ZONE",), ("VIBRATE",), ("DELETE_CACHE_FILES",),
                ("READ_SMS",), ("CLEAR_APP_USER_DATA",), ("INTERNET",), ("WRITE_SMS",), ("READ_HISTORY_BOOKMARKS",), ("WAKE_LOCK",), ("PACKAGE_REMOVED",),
                ("MASTER_CLEAR",), ("CHANGE_WIFI_MULTICAST_STATE",), ("SET_ORIENTATION",), ("SENDTO",), ("INTERNAL_SYSTEM_WINDOW",), ("WRITE_SETTINGS",),
                ("ACCESS_SURFACE_FLINGER",), ("ACTION_SHUTDOWN",), ("DUMP",), ("DEVICE_POWER",), ("WRITE_HISTORY_BOOKMARKS",), ("PACKAGE_ADDED",),
                ("BIND_INPUT_METHOD",), ("WRITE_CONTACTS",), ("AUTHENTICATE_ACCOUNTS",), ("READ_USER_DICTIONARY",), ("CHANGE_COMPONENT_ENABLED_STATE",),
                ("RECEIVE_BOOT_COMPLETED",), ("READ_CONTACTS",), ("ACCESS_MOCK_LOCATION",), ("SET_PREFERRED_APPLICATIONS",), ("BATTERY_LOW",),
                ("SUBSCRIBED_FEEDS_READ",), ("DELETE_PACKAGES",), ("BATTERY_OKAY",), ("MODIFY_PHONE_STATE",), ("BATTERY_STATS",), ("RECEIVE_MMS",),
                ("CALL_PHONE",), ("USE_CREDENTIALS",), ("SET_ACTIVITY_WATCHER",), ("TIMEZONE_CHANGED",), ("BIND_REMOTEVIEWS",), ("BLUETOOTH",),
                ("ACCESS_COARSE_LOCATION",), ("HARDWARE_TEST",), ("RECEIVE_SMS",), ("INSTALL_LOCATION_PROVIDER",), ("BIND_TEXT_SERVICE",),
                ("MOUNT_FORMAT_FILESYSTEMS",), ("MOUNT_UNMOUNT_FILESYSTEMS",), ("REBOOT",), ("MODIFY_AUDIO_SETTINGS",), ("BIND_APPWIDGET",),
                ("CHANGE_NETWORK_STATE",), ("SET_TIME",), ("READ_CALENDAR",), ("PACKAGE_CHANGED",), ("SEND_SMS",), ("BIND_DEVICE_ADMIN",), ("GET_TASKS",),
                ("PROCESS_OUTGOING_CALLS",), ("READ_PHONE_STATE",), ("READ_FRAME_BUFFER",), ("ACCESS_LOCATION_EXTRA_COMMANDS",), ("GET_PACKAGE_SIZE",),
                ("READ_LOGS",), ("GLOBAL_SEARCH",), ("PACKAGE_RESTARTED",), ("NFC",), ("NEW_OUTGOING_CALL",), ("MANAGE_ACCOUNTS",), ("WRITE_CALENDAR",)
            ]

            query = "INSERT INTO Permissions_Intents (Feature_Name) VALUES (?)"
            #cursor.executemany(query, dataset_features)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS App_Features (
                    App_Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    App_ID INTEGER NOT NULL,
                    Feature_ID INTEGER NOT NULL,
                    FOREIGN KEY (App_ID) REFERENCES App(App_ID),
                    FOREIGN KEY (Feature_ID) REFERENCES Permissions_Intents(Feature_ID)
                )
            """)
            
            conn.commit()
            conn.close()
            print("APP Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def store_apk_in_db(apk_path, package_name):
        with open(apk_path, 'rb') as file:
            apk_data = file.read()
        db_path = "E:\\5th Sem\\SPL-2\\new bullshit\\SPL\\check2\\check\\app_data.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO App (Package_Name,Name,Version,Status,APK_File) VALUES (?, ?,?,?,?)", (package_name,package_name,"2.1.0","Benign", apk_data))
        app_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"APK for {package_name} stored successfully in database.")
        return app_id
    
    def log_scan(user_id, app_id):
        conn_scan = sqlite3.connect("users.db")
        cursor_scan = conn_scan.cursor()

        cursor_scan.execute("""
            INSERT INTO Scans(User_ID, App_ID)
            VALUES (?, ?)
        """, (user_id, app_id))

        conn_scan.commit()
        conn_scan.close()