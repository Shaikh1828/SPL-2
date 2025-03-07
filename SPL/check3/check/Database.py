import sqlite3
from PyQt5.QtWidgets import QMessageBox
import hashlib
from datetime import datetime

class Database:
    def __init__(self, db_path="users.db"):
        self.db_path = db_path
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        self.init_user_database()
        self.init_AppDatabase()

    def __del__(self):
        """Close database connection"""
        if hasattr(self, 'connection'):
            self.connection.close()


    def init_user_database(self):
        """Initializes the database and ensures the users table is set up correctly."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create users table if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    verified INTEGER DEFAULT 0,
                    verification_token TEXT,
                    user_type TEXT DEFAULT 'personal',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
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
            print("User database initialized successfully.")
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
            
    
            # cursor.execute("""
            #     DELETE FROM App_Features
            #     WHERE App_ID in (51,52,53,54,55,56,57,58,59,60,61,62);

            # """)
            # cursor.execute("""
            #     DELETE FROM App
            #     WHERE App_ID in (51,52,53,54,55,56,57,58,59,60,61,62);
            # """)

            # cursor.execute("""
            #     VACUUM
            # """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS Permissions_Intents (
                    Feature_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    Feature_Name TEXT NOT NULL
                )
            """)
            query = """
            INSERT INTO Permissions_Intents (Feature_Name)
            SELECT ? WHERE NOT EXISTS (
                SELECT 1 FROM Permissions_Intents WHERE Feature_Name = ?
            )
            """



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

            cursor.executemany(query, [(feature[0], feature[0]) for feature in dataset_features])

            # query = "INSERT INTO Permissions_Intents (Feature_Name) VALUES (?)"
            # #cursor.executemany(query, dataset_features)
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


    def hash_password(self, password):
        """Hash the password before storing it"""
        return hashlib.sha256(password.encode()).hexdigest()

    def add_user(self, username, password, email, verification_token, user_type="personal"):
        """Add a new user to the database"""
        try:
            # Check if username already exists
            self.cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            if self.cursor.fetchone():
                print("Username already exists!")
                return False
            
            # Check if email already exists
            self.cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if self.cursor.fetchone():
                print("Email already exists!")
                return False

            # Hash password before storing
            hashed_password = self.hash_password(password)

            # Insert user into database
            self.cursor.execute(
                "INSERT INTO users (username, password, email, verification_token, verified, user_type) VALUES (?, ?, ?, ?, ?, ?)",
                (username, hashed_password, email, verification_token, 0, user_type)
            )
            self.connection.commit()
            print(f"User {username} added successfully.")
            return True
        except Exception as e:
            print(f"Error adding user: {e}")
            return False

    def check_login(self, username, password):
        """Check login credentials and verification status"""
        try:
            hashed_password = self.hash_password(password)
            query = "SELECT id, verified FROM users WHERE username = ? AND password = ?"
            self.cursor.execute(query, (username, hashed_password))
            result = self.cursor.fetchone()
            if result :
                if result[1]==1:
                    return result[0],True
                else: 
                    return 0,"unverified"     
            else: 
                return 0,"invalid"
        except Exception as e:
            print(f"Error checking login: {e}")
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

    def previously_scanned(self, package_name, version):
        """Check if the APK with the same package name and version exists in the database."""
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
        
        cursor.execute("SELECT App_ID FROM App WHERE Name = ? AND Version = ?", (package_name, version))
        existing_app = cursor.fetchone()
        
        conn.close()
        
        if existing_app:
            return True, existing_app[0]  # Return True and the App_ID if found
        return False, None
    
    def store_apk_in_db( self,apk_path, package_name,version):
        """Store APK file in database"""
        try:
            existing_app,app_id =self.previously_scanned(package_name,version)
            print("app id=",app_id)
            if (existing_app==False):
                with open(apk_path, 'rb') as file:
                    apk_data = file.read()
                conn = sqlite3.connect("app_data.db")
                cursor = conn.cursor()
                cursor.execute("INSERT INTO App (Package_Name, Name, Version, Status, APK_File) VALUES (?, ?, ?, ?, ?)",
                            (package_name, package_name, version, "Benign", apk_data))
                app_id=cursor.lastrowid
                conn.commit()
                conn.close()
            print(f"APK for {package_name} stored successfully.")
            return app_id    
        except Exception as e:
            print(f"Error storing APK in database: {e}")

    def get_user_email(self, username):
        """Get the email for a given username"""
        try:
            self.cursor.execute("SELECT id,email FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            return result[0],result[1] if result else None
        except Exception as e:
            print(f"Error getting user email: {e}")
            return None

    def get_user_type(self, username):
        """Get the user type for a specific username"""
        try:
            self.cursor.execute("SELECT user_type FROM users WHERE username = ?", (username,))
            result = self.cursor.fetchone()
            return result[0] if result else "personal"
        except Exception as e:
            print(f"Error getting user type: {e}")
            return "personal"

    

    def update_user_credentials(self, user_id, new_username, new_password):
        """Update user's username and password in the database"""
        try:
            # Check if new_username is already taken by another user
            self.cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (new_username, user_id))
            if self.cursor.fetchone():
                print("Username already exists!")
                return False

            hashed_password = self.hash_password(new_password)
            self.cursor.execute(
                "UPDATE users SET username = ?, password = ? WHERE id = ?",
                (new_username, hashed_password, user_id)
            )
            self.connection.commit()
            print("User credentials updated successfully.")
            return True
        except Exception as e:
            print(f"Error updating user credentials: {e}")
            return False
        
    def save_credentials(self):
        new_username = self.user_id_input.text().strip()
        new_password = self.password_input.text()
        
        # Basic validation
        if not new_username:
            QMessageBox.warning(self, "Input Error", "User ID cannot be empty.")
            return
            
        
        # Update credentials in the database
        if self.database:
            success = self.database.update_user_credentials(
                self.user_credentials["id"],  # Use the user's database ID
                new_username,
                new_password
            )
            if success:
                # Update local credentials and notify parent
                self.user_credentials["user_id"] = new_username
                self.user_credentials["password"] = new_password
                self.credentials_updated.emit(self.user_credentials)
                QMessageBox.information(self, "Success", "Credentials updated successfully.")
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Username already taken.")
        else:
            QMessageBox.warning(self, "Error", "Database connection not available.")

    def log_scan(self,user_id, app_id):
        conn_scan = sqlite3.connect("users.db")
        cursor_scan = conn_scan.cursor()

        cursor_scan.execute("""
            INSERT INTO Scans(User_ID, App_ID)
            VALUES (?, ?)
        """, (user_id, app_id))

        conn_scan.commit()
        conn_scan.close()

    def get_permission_intent_status(app_id):
        conn = sqlite3.connect("app_data.db")
        cursor = conn.cursor()
                
        query = """SELECT pi.Feature_Name 
               FROM App_Features af
               JOIN Permissions_Intents pi ON af.Feature_ID = pi.Feature_ID
               WHERE af.App_ID = ?;"""
    
        cursor.execute(query, (app_id,))
        features = [row[0] for row in cursor.fetchall()]
        query = "SELECT Status FROM App WHERE App_ID = ?;"
        cursor.execute(query, (app_id,))
        status = cursor.fetchone()
          # Extract feature names
        cursor.commit()
        cursor.close()

        return features,status
