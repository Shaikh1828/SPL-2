from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QTableWidget, QStackedWidget,
    QLineEdit, QMessageBox, QGridLayout, QFrame, QTableWidgetItem, QComboBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, pyqtSignal
from Database import Database
import sqlite3,hashlib


class Dashboard(QWidget):
    credentials_updated = pyqtSignal(dict)
    u_id = 0 
    def __init__(self, parent=None, user_credentials=None, database=None ):
        super().__init__(parent)
        self.setWindowTitle("User Dashboard")
        self.resize(800, 800)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        print("User ID passed to Dashboard:", parent.u_id)  # Debugging
        self.u_id = parent.u_id
        
        
        # User credentials
        self.user_credentials = user_credentials 
        # self.loadScanData(u_id)
        self.init_ui()
        self.drag_pos = None
        
    def init_ui(self):
        # Title Bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
        title_bar_layout = QHBoxLayout()
        title_label = QLabel("User Dashboard")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
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
        
        # Section Buttons
        section_layout = QHBoxLayout()
        section_buttons = [
            ("Profile", self.show_credentials_section),
            ("History", self.show_history_section),
            ("AppList", self.show_applist_section)
        ]
        
        self.section_button_group = []
        for label, method in section_buttons:
            btn = QPushButton(label)
            btn.clicked.connect(method)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6BC8B4;
                    color: white;
                    border: none;
                    padding: 10px;
                    margin: 5px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: rgb(90, 180, 160);
                }
            """)
            section_layout.addWidget(btn)
            self.section_button_group.append(btn)
        
        # Stacked Widget for Sections
        self.stacked_widget = QStackedWidget()
        
        # Credentials Section
        credentials_section = QWidget()
        credentials_layout = QVBoxLayout()
        
        form_frame = QFrame()
        form_frame.setStyleSheet("""
            QFrame {
                background-color: rgba(240, 248, 255, 200);
                border-radius: 10px;
                padding: 10px;
            }
        """)
        
        form_layout = QGridLayout()
        
        user_id_label = QLabel("User Name:")
        user_id_label.setFont(QFont("Arial", 12))
        user_id_label.setStyleSheet("color: #333; font-weight: bold;")
        
        self.user_id_input = QLineEdit(self.user_credentials.get("user_name"))
        
        password_label = QLabel("Add New Password:")
        password_label.setFont(QFont("Arial", 12))
        password_label.setStyleSheet("color: #333; font-weight: bold;")
        
        self.password_input = QLineEdit(self.user_credentials.get("password", ""))
        self.password_input.setEchoMode(QLineEdit.Password)
        
        self.toggle_password_btn = QPushButton("Show")
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        
        form_layout.addWidget(user_id_label, 0, 0)
        form_layout.addWidget(self.user_id_input, 0, 1)
        form_layout.addWidget(password_label, 1, 0)
        form_layout.addWidget(self.password_input, 1, 1)
        form_layout.addWidget(self.toggle_password_btn, 1, 2)
        
        form_frame.setLayout(form_layout)
        
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_credentials)
        
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.close)
        
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        credentials_layout.addWidget(form_frame)
        credentials_layout.addLayout(button_layout)
        credentials_section.setLayout(credentials_layout)

        
        # history Section
        history_section = QWidget()
        history_layout = QVBoxLayout()
        # hbox = QHBoxLayout()
        self.tableWidget = QTableWidget()
        # Set up table columns
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels([
            "Scan ID", "User ID", "App Name", "Status", "Scan Timestamp"
        ])
         # Add table to HBox layout
        # hbox.addWidget(self.tableWidget)
        history_layout.addWidget(self.tableWidget)
        # history_layout.addWidget(refresh_button)
        history_section.setLayout(history_layout)



         # Applist
        applist_section = QWidget()
        applist_layout = QVBoxLayout()
        appbox = QHBoxLayout()
        self.appTable = QTableWidget()
        # Set up table columns
        self.appTable.setColumnCount(3)
        self.appTable.setHorizontalHeaderLabels([
            "Scan ID", "User ID", "App Name", "Status", "Scan Timestamp"
        ])
         # Add table to HBox layout
        appbox.addWidget(self.appTable)        
        applist_layout.addWidget(self.appTable)
        # history_layout.addWidget(refresh_button)
        applist_section.setLayout(applist_layout)
        ##

         # Feature selection label
        label = QLabel('Select Feature:')
        applist_layout.addWidget(label)
        
        # Create dropdown (combo box)
        self.feature_combo = QComboBox()
        self.feature_combo.addItem('-- Select a feature --')  # Default placeholder
        self.feature_combo.currentIndexChanged.connect(self.on_feature_selected)
        applist_layout.addWidget(self.feature_combo)

        
        # Add Sections to Stacked Widget
        self.stacked_widget.addWidget(credentials_section)
        self.stacked_widget.addWidget(history_section)
        self.stacked_widget.addWidget(applist_section)
        
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        main_layout.addLayout(section_layout)
        main_layout.addWidget(self.stacked_widget)
        
        self.setLayout(main_layout)
        
        # Default to Credentials Section
        self.show_credentials_section()
    
    # def get_username_by_user_id(self, u_id):
    #     """
    #     Retrieve username from the users.db database based on user_id
        
    #     Parameters:
    #     user_id (str): The unique ID of the user to look up
        
    #     Returns:
    #     str or None: The username if found, None otherwise
    #     """
    #     try:
    #         import sqlite3
            
    #         # Connect to the users.db database
    #         conn = sqlite3.connect('users.db')
    #         cursor = conn.cursor()
            
    #         # Query the database for the username
    #         cursor.execute("SELECT username FROM users WHERE id = ?", (u_id,))
    #         result = cursor.fetchone()
            
    #         # Close the connection
    #         conn.close()
            
    #         # Return the username if found, otherwise None
    #         return result[0] if result else None
            
    #     except sqlite3.Error as e:
    #         print(f"Database error: {e}")
    #         return None


    def show_credentials_section(self):
        self.stacked_widget.setCurrentIndex(0)
    
    def show_history_section(self):
        self.loadScanData()
        self.stacked_widget.setCurrentIndex(1)

    def show_applist_section(self):
        self.ShowApplist()
        self.load_features()
        self.stacked_widget.setCurrentIndex(2)

    
    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("Hide")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("Show")

    def loadScanData(self):
        try:
            # Connect to user.db for scans
            user_conn = sqlite3.connect('users.db')
            user_cursor = user_conn.cursor()
            
            # Get all scan data from user.db
            user_cursor.execute('''
                SELECT Scan_ID, User_ID, App_ID, Scan_Timestamp
                FROM Scans WHERE User_ID = ?
            ''', (self.u_id,))
            scan_results = user_cursor.fetchall()
            
            # Connect to app_data.db for app details
            app_conn = sqlite3.connect('app_data.db')
            app_cursor = app_conn.cursor()
            
            # Get all app data
            app_cursor.execute('''
                SELECT App_ID, Name, Status
                FROM App
            ''')
            
            # Convert app data to a dictionary for easier lookup
            app_dict = {}
            for app_id, name, status in app_cursor.fetchall():
                app_dict[app_id] = (name, status)
            
            # Prepare the combined data
            combined_results = []
            for scan_id, user_id, app_id, timestamp in scan_results:
                if app_id in app_dict:
                    app_name, status = app_dict[app_id]
                    combined_results.append((scan_id, user_id, app_name, status, timestamp))
                else:
                    # Handle case where App_ID doesn't have a match
                    combined_results.append((scan_id, user_id, "Unknown", "Unknown", timestamp))
            
            # Set the number of rows in the table
            self.tableWidget.setRowCount(len(combined_results))
            
            # Populate the table
            for row, (scan_id, user_id, app_name, status, timestamp) in enumerate(combined_results):
                self.tableWidget.setItem(row, 0, QTableWidgetItem(str(scan_id)))
                self.tableWidget.setItem(row, 1, QTableWidgetItem(str(user_id)))
                self.tableWidget.setItem(row, 2, QTableWidgetItem(app_name))
                self.tableWidget.setItem(row, 3, QTableWidgetItem(status))
                self.tableWidget.setItem(row, 4, QTableWidgetItem(str(timestamp)))
            
            # Resize columns to content
            self.tableWidget.resizeColumnsToContents()
            
            # Close the database connections
            user_conn.close()
            app_conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in loadScanData: {e}")
    
    def save_credentials(self, u_id ):
        user_name = self.user_id_input.text().strip()
        password = self.password_input.text()
        

        if not user_name:
            QMessageBox.warning(self, "Input Error", "User Name cannot be empty.")
            return
        
        # if len(password) < 8:
        #     QMessageBox.warning(self, "Input Error", "Password must be at least 8 characters long.")
        #     return
        
        # If user is logged in and has an ID, use database update
        if self.user_credentials.get("id") and (user_name!=self.user_credentials["user_name"] or password):
            success = self.update_user_in_database(self.user_credentials["id"],user_name,password)
            if success:
                self.user_credentials["user_name"] = user_name
                self.user_credentials["password"] = password
                self.credentials_updated.emit(self.user_credentials)
                QMessageBox.information(self, "Success", "Credentials updated successfully.")
                #self.close()
            else:
                QMessageBox.warning(self, "Error", "Username already taken or update failed.")
        else:
            # If not logged in, just update local credentials
            self.user_credentials = {"id":self.u_id,"user_name": user_name, "password": password}
            self.credentials_updated.emit(self.user_credentials)
            QMessageBox.information(self, "Success", "Your credentials have been updated successfully.")
            #self.close()


    def update_user_in_database(self, u_id, new_username=None, new_password=None):
        """
        Update user credentials in the users.db database
        
        Parameters:
        user_id (str): The unique ID of the user to update
        new_username (str): The new username
        new_password (str): The new password
        
        Returns:
        bool: True if update succeeded, False otherwise
        """
        try:
            import sqlite3
            
            # Connect to the users.db database
            conn = sqlite3.connect('users.db')
            cursor = conn.cursor()
            
            # Check if the new username already exists for a different user
            if new_username:
                cursor.execute("SELECT id FROM users WHERE username = ? AND id != ?", (new_username, u_id))
                if cursor.fetchone():
                    conn.close()
                    return False  # Username already taken
                
            # Update the user with the new credentials
                # Handle updates based on which fields are provided
            if new_username and new_password:
                print("both")
                # Both username and password are provided
                cursor.execute(
                    "UPDATE users SET username = ?, password = ? WHERE id = ?", 
                    (new_username, self.hash_password(new_password), u_id)
                )
            elif new_username:
                print("only name")
                # Only username is provided
                cursor.execute(
                    "UPDATE users SET username = ? WHERE id = ?", 
                    (new_username, u_id)
                )
            elif new_password:
                print("only pass")
                # Only password is provided
                cursor.execute(
                    "UPDATE users SET password = ? WHERE id = ?", 
                    (self.hash_password(new_password), u_id)
                )
            
            # Commit changes and close connection
            conn.commit()
            conn.close()
            
            # Return True if at least one row was affected
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False
    
    def hash_password(self, password):
        """Hash the password before storing it"""
        return hashlib.sha256(password.encode()).hexdigest()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def ShowApplist(self):
        try:
            # Connect to user.db for scans
            user_conn = sqlite3.connect('users.db')
            user_cursor = user_conn.cursor()
            
            # Get unique App_IDs for this user
            user_cursor.execute('''
                SELECT DISTINCT App_ID
                FROM Scans 
                WHERE User_ID = ?
            ''', (self.u_id,))
            unique_app_ids = [row[0] for row in user_cursor.fetchall()]
            
            # Connect to app_data.db for app details
            app_conn = sqlite3.connect('app_data.db')
            app_cursor = app_conn.cursor()
            
            # Create a dictionary to store app information by name
            app_dict = {}
            
            # Get app information for each unique App_ID
            placeholders = ','.join(['?' for _ in unique_app_ids])
            if unique_app_ids:  # Only execute if there are app IDs
                app_cursor.execute(f'''
                    SELECT App_ID, Name, Status
                    FROM App
                    WHERE App_ID IN ({placeholders})
                ''', unique_app_ids)
                
                for app_id, name, status in app_cursor.fetchall():
                    # Store the app info by name (will overwrite if same name appears multiple times)
                    app_dict[name] = (app_id, status)
            
            # Get the unique app names (sorted)
            unique_app_names = sorted(app_dict.keys())
            
            # Set the number of rows in the table
            self.appTable.setRowCount(len(unique_app_names))
            
            # Populate the table
            for row, app_name in enumerate(unique_app_names):
                app_id, status = app_dict[app_name]
                self.appTable.setItem(row, 0, QTableWidgetItem(app_name))
                self.appTable.setItem(row, 1, QTableWidgetItem(str(app_id)))
                self.appTable.setItem(row, 2, QTableWidgetItem(status))
            
            # Resize columns to content
            self.appTable.resizeColumnsToContents()
            
            # Close the database connections
            user_conn.close()
            app_conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in loadScanData: {e}")

    def load_features(self):
        """Load feature names from the database"""
        try:
            # Save current selection if any
            current_selection = self.feature_combo.currentText()
            if current_selection == '-- Select a feature --':
                current_selection = None
                
            # Clear the combo box but keep the placeholder
            self.feature_combo.clear()
            self.feature_combo.addItem('-- Select a feature --')
            
            # Connect to SQLite database
            conn = sqlite3.connect('app_data.db')
            cursor = conn.cursor()
            
            # Query to get distinct feature names
            cursor.execute('SELECT DISTINCT feature_name FROM Permissions_Intents ORDER BY feature_name')
            features = cursor.fetchall()
            
            # Add features to the combo box
            for feature in features:
                self.feature_combo.addItem(feature[0])
                
            # Restore previous selection if it exists
            if current_selection and current_selection != '-- Select a feature --':
                index = self.feature_combo.findText(current_selection)
                if index >= 0:
                    self.feature_combo.setCurrentIndex(index)
            
            # Close connection
            conn.close()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error', 
                                f'Failed to load features from database: {str(e)}')
    
    def on_feature_selected(self):
        """Handle the feature selection change"""
        selected = self.feature_combo.currentText()
        print(selected)
        self.ShowApplistbyfeature()

    def ShowApplistbyfeature(self):
        selected_feature = self.feature_combo.currentText()
        try:
            # Connect to user.db for scans
            user_conn = sqlite3.connect('users.db')
            user_cursor = user_conn.cursor()
            
            # Get unique App_IDs for this user
            user_cursor.execute('''
                SELECT DISTINCT App_ID
                FROM Scans 
                WHERE User_ID = ?
            ''', (self.u_id,))
            unique_app_ids = [row[0] for row in user_cursor.fetchall()]
            
            # Connect to app_data.db for app details
            app_conn = sqlite3.connect('app_data.db')
            app_cursor = app_conn.cursor()
            
            # First, get the Feature_ID for the selected feature
            app_cursor.execute('''
                SELECT Feature_ID
                FROM Permissions_Intents
                WHERE Feature_Name = ?
            ''', (selected_feature,))
            feature_id_result = app_cursor.fetchone()
            
            if not feature_id_result:
                # No such feature found
                self.appTable.setRowCount(0)
                app_conn.close()
                user_conn.close()
                return
                
            feature_id = feature_id_result[0]
            
            # Get App_IDs that have this feature
            placeholders = ','.join(['?' for _ in unique_app_ids])
            if unique_app_ids:  # Only execute if there are app IDs
                app_cursor.execute(f'''
                    SELECT DISTINCT App_ID
                    FROM App_Features
                    WHERE App_ID IN ({placeholders}) AND Feature_ID = ?
                ''', unique_app_ids + [feature_id])
                
                filtered_app_ids = [row[0] for row in app_cursor.fetchall()]
                
                # Get app information for each filtered App_ID
                app_dict = {}
                if filtered_app_ids:
                    placeholders = ','.join(['?' for _ in filtered_app_ids])
                    app_cursor.execute(f'''
                        SELECT App_ID, Name, Status
                        FROM App
                        WHERE App_ID IN ({placeholders})
                    ''', filtered_app_ids)
                    
                    for app_id, name, status in app_cursor.fetchall():
                        # Store the app info by name
                        app_dict[name] = (app_id, status)
            
            # Get the unique app names (sorted)
            unique_app_names = sorted(app_dict.keys())
            
            # Set the number of rows in the table
            self.appTable.setRowCount(len(unique_app_names))
            
            # Populate the table
            for row, app_name in enumerate(unique_app_names):
                app_id, status = app_dict[app_name]
                self.appTable.setItem(row, 0, QTableWidgetItem(app_name))
                self.appTable.setItem(row, 1, QTableWidgetItem(str(app_id)))
                self.appTable.setItem(row, 2, QTableWidgetItem(status))
            
            # Resize columns to content
            self.appTable.resizeColumnsToContents()
            
            # Close the database connections
            user_conn.close()
            app_conn.close()
        except sqlite3.Error as e:
            print(f"Database error: {e}")
        except Exception as e:
            print(f"Exception in ShowApplist: {e}")