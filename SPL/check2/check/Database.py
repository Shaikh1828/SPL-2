# database.py
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="D:\\Git\\SPL-2\\SPL\\check2\\check copy\\users.db"):
        self.db_path = db_path
        # Initialize database connection
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.check_and_update_schema()
        self.init_app_database()
        
    def __del__(self):
        """Close database connection when object is destroyed"""
        if hasattr(self, 'connection'):
            self.connection.close()

    def check_and_update_schema(self):
        """Check existing schema and update if necessary"""
        try:
            # Check if users table exists
            self.cursor.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='users'
            """)
            
            if not self.cursor.fetchone():
                # Create new users table if it doesn't exist
                self.cursor.execute("""
                    CREATE TABLE users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE,
                        verified INTEGER DEFAULT 0,
                        verification_token TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                self.connection.commit()
                print("Users table created successfully.")
            else:
                # Check if needed columns exist and add them if they don't
                self.cursor.execute("PRAGMA table_info(users)")
                columns = [column[1] for column in self.cursor.fetchall()]
                
                if 'email' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN email TEXT UNIQUE")
                if 'verified' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0")
                if 'verification_token' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN verification_token TEXT")
                if 'created_at' not in columns:
                    self.cursor.execute("ALTER TABLE users ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                
                self.connection.commit()
                print("User table schema updated successfully.")
        except Exception as e:
            print(f"Error updating database schema: {e}")

    def init_app_database(self):
        """Initialize application database"""
        try:
            app_conn = sqlite3.connect("app_data.db")
            app_cursor = app_conn.cursor()

            app_cursor.execute("""
                CREATE TABLE IF NOT EXISTS App (
                    App_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Package_Name TEXT NOT NULL,
                    Name TEXT NOT NULL,
                    Version TEXT,
                    Status TEXT,
                    APK_File BLOB
                )
            """)

            app_cursor.execute("""
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
            # app_cursor.executemany(query, dataset_features)

            app_cursor.execute("""
                CREATE TABLE IF NOT EXISTS App_Features (
                    App_Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    App_ID INTEGER NOT NULL,
                    Feature_ID INTEGER NOT NULL,
                    FOREIGN KEY (App_ID) REFERENCES App(App_ID),
                    FOREIGN KEY (Feature_ID) REFERENCES Permissions_Intents(Feature_ID)
                )
            """)

            app_conn.commit()
            app_conn.close()
            print("App Database initialized successfully.")
        except Exception as e:
            print(f"Error initializing App database: {e}")

    # In the add_user method of Database.py, add:
    # Add these methods to your Database class

    def add_user(self, username, password, email, verification_token, user_type="personal"):
        """Add a new user to the database with verification token and user type"""
        try:
            # Check if username already exists
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone():
                return False
            
            # Check if email already exists
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone():
                return False
            
            # Add user to database (unverified)
            self.cursor.execute(
                "INSERT INTO users (username, password, email, verification_token, verified, user_type) VALUES (?, ?, ?, ?, ?, ?)",
                (username, password, email, verification_token, 0, user_type)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def get_user_type(self, username):
        """Get the user type for a specific username"""
        try:
            self.cursor.execute("SELECT user_type FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            if result:
                return result[0]
            return "personal"  # Default if not found
        except Exception as e:
            print(f"Error getting user type: {e}")
            return "personal"

    # Add to Database.py
    def get_user_email(self, username):
        """Get the email address for a given username"""
        try:
            query = "SELECT email FROM users WHERE username = ?"
            self.cursor.execute(query, (username,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error getting user email: {e}")
            return None

    def update_verification_token(self, email, jwt_token):
        """Update the verification token for a user"""
        try:
            query = "UPDATE users SET verification_token = ? WHERE email = ?"
            self.cursor.execute(query, (jwt_token, email))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error updating verification token: {e}")
            return False

    def mark_user_verified(self, email):
        """Mark user as verified after successful OTP validation"""
        try:
            query = "UPDATE users SET verified = 1 WHERE email = ?"
            self.cursor.execute(query, (email,))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error marking user as verified: {e}")
            return False

    def check_login(self, username, password):
        """Check login credentials and verification status"""
        try:
            query = """
                SELECT id, verified 
                FROM users 
                WHERE username = ? AND password = ?
            """
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()
            
            if result:
                user_id, is_verified = result
                if is_verified:
                    return True
                else:
                    return "unverified"
            return False
        except Exception as e:
            print(f"Error checking login: {e}")
            return False
        
    def get_verification_token(self, email):
        """Retrieve the JWT token for email verification"""
        try:
            query = "SELECT verification_token FROM users WHERE email = ?"
            self.cursor.execute(query, (email,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error retrieving verification token: {e}")
            return None
        
    def store_apk_in_db(apk_path, package_name):
        with open(apk_path, 'rb') as file:
            apk_data = file.read()
        db_path = "D:\\Git\\SPL-2\\SPL\\check2\\check copy\\app_data.db"
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO App (Package_Name,Name,Version,Status,APK_File) VALUES (?, ?,?,?,?)", (package_name,package_name,"2.1.0","Benign", apk_data))
        app_id = cursor.lastrowid
        conn.commit()
        conn.close()

        print(f"APK for {package_name} stored successfully in database.")
        return app_id