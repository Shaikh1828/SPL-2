import sqlite3
from PyQt5.QtWidgets import QMessageBox, QWidget

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.newpath="app_features.db"
        self.init_Userdatabase() 
        self.init_Appdatabase()
    def init_Userdatabase(self):
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
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Database initialization error: {e}")


    def init_Appdatabase(self):
        try:
            conn = sqlite3.connect(self.newpath)
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
                    BATTERY_LOW BOOLEAN DEFAULT FALSE,
                    ACTION_POWER_CONNECTED BOOLEAN DEFAULT FALSE
                )
            """)
            conn.commit()
            conn.close()
            print("Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing database: {e}")
