from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor
from PyQt5.QtCore import Qt
from Dashboard import Dashboard

from scan import Scan
from MLmodel import MLModel  

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Droid Scanner")
        self.resize(1400, 900)
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.init_ui()
        self.drag_pos = None  
    
    def init_ui(self):
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
        # upload_button.clicked.connect()
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

        scan_button = QPushButton("Scan Devices")
        scan_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(90, 180, 160);
                color: black;
                font: bold 15pt Arial;
                border-radius: 10px;
                padding: 8px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: rgb(110, 190, 170);
            }
        """)
        scan_button.clicked.connect(self.open_scan_window)

        # Dashboard
        self.dashboard_button = QPushButton("User Dashboard")
        self.dashboard_button.clicked.connect(self.open_dashboard)
        self.dashboard_button.setStyleSheet("""
            QPushButton {
                background-color: #6BC8B4;
                color: black;
                font: bold 15pt Arial;
                border-radius: 10px;
                padding: 8px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: rgb(90, 180, 160);
            }
        """)

        # Train Model Button
        self.train_button = QPushButton("Model Accuracy")
        self.train_button.clicked.connect(self.train_model)
        self.train_button.setStyleSheet("""
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
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setVisible(True)
        self.info_text.setText(
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

        self.info_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(240, 248, 255, 200);
                color: black;
                font: 11pt Courier;
                border-radius: 10px;
                padding: 10px;
            }
        """)

        # Results Display
        self.results_text = QTextEdit()
        self.results_text.setStyleSheet("""
            QTextEdit {
                background-color: rgba(240, 248, 255, 200);
                color: black;
                font: 11pt Courier;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        self.results_text.setReadOnly(True)
        self.results_text.setVisible(False)

        # Layouts
        left_layout = QVBoxLayout()
        left_layout.addWidget(upload_label)
        left_layout.addWidget(choose_button)
        left_layout.addWidget(self.file_path_label)
        left_layout.addWidget(upload_button)
        left_layout.addWidget(scan_button)
        left_layout.addStretch()
        left_layout.addWidget(self.dashboard_button)

        left_layout.addWidget(self.train_button)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.info_text)
        right_layout.addWidget(self.results_text)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title_bar)
        content_layout = QHBoxLayout()
        content_layout.addLayout(left_layout, 1)
        content_layout.addLayout(right_layout, 2)

        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)

        # Initialize MLModel with the CSV file path
        self.ml_model = MLModel('processed_output.csv')

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

    def open_scan_window(self):
        self.scan_window = Scan(self)
        self.scan_window.scan_completed.connect(self.update_scan_results)
        self.scan_window.show()

    def update_scan_results(self, scan_result):
        """Update the main window with scan results"""
        self.info_text.setVisible(False)
        self.results_text.setVisible(True)
        
        # Format the report with HTML for better presentation
        classification_color = "#FF3333" if scan_result["classification"] == "Malicious" else "#33AA33"
        
        report = f"""
        <h2>App Scan Report</h2>
        <p><b>Package Name:</b> {scan_result["package_name"]}</p>
        <p><b>Version:</b> {scan_result["app_version"]}</p>
        <p><b>Classification:</b> <span style="color: {classification_color}; font-weight: bold;">{scan_result["classification"]}</span></p>
        
        <h3>Security Analysis</h3>
        <p><b>Total Permissions:</b> {len(scan_result["permissions"])}</p>
        <p><b>Suspicious Permissions:</b> {len(scan_result["suspicious_permissions"])}</p>
        <p><b>Total Intents:</b> {len(scan_result["intents"])}</p>
        <p><b>Suspicious Intents:</b> {len(scan_result["suspicious_intents"])}</p>
        """
        
        # Add suspicious permissions details if any exist
        if scan_result["suspicious_permissions"]:
            report += """
            <h3>Suspicious Permissions</h3>
            <ul style="color: #DD4444;">
            """
            for perm in scan_result["suspicious_permissions"]:
                # Add human-readable descriptions for common permissions
                description = self.get_permission_description(perm)
                report += f"<li><b>{perm}</b> - {description}</li>"
            report += "</ul>"
        
        # Add suspicious intents details if any exist
        if scan_result["suspicious_intents"]:
            report += """
            <h3>Suspicious Intents</h3>
            <ul style="color: #DD4444;">
            """
            for intent in scan_result["suspicious_intents"]:
                # Add human-readable descriptions for common intents
                description = self.get_intent_description(intent)
                report += f"<li><b>{intent}</b> - {description}</li>"
            report += "</ul>"
        
        # Add all permissions
        report += """
        <h3>All Permissions</h3>
        <ul style="color: #555555;">
        """
        for perm in scan_result["permissions"]:
            report += f"<li>{perm}</li>"
        report += "</ul>"
        
        # Add security recommendations based on classification
        report += """
        <h3>Security Recommendations</h3>
        """
        
        if scan_result["classification"] == "Malicious":
            report += """
            <p style="color: #FF3333; font-weight: bold;">This app appears to be potentially harmful. Consider the following actions:</p>
            <ul>
                <li>Uninstall this application immediately</li>
                <li>Check your device for other suspicious apps</li>
                <li>Run a full system scan with an antivirus</li>
                <li>Monitor for unusual behavior or excessive battery/data usage</li>
            </ul>
            """
        else:
            report += """
            <p style="color: #33AA33;">This app appears to be safe, but always be cautious with app permissions:</p>
            <ul>
                <li>Review permissions regularly</li>
                <li>Consider revoking unnecessary permissions</li>
                <li>Keep the app updated to the latest version</li>
                <li>Only download apps from trusted sources</li>
            </ul>
            """
            
        # Set the formatted report to the results text area
        self.results_text.setHtml(report)

    def get_permission_description(self, permission):
        """Return a human-readable description of common Android permissions"""
        descriptions = {
            "android.permission.READ_CONTACTS": "Can read your contacts",
            "android.permission.WRITE_CONTACTS": "Can modify your contacts",
            "android.permission.ACCESS_FINE_LOCATION": "Can track your precise location",
            "android.permission.READ_CALL_LOG": "Can read your call history",
            "android.permission.READ_SMS": "Can read your text messages",
            "android.permission.SEND_SMS": "Can send text messages (potentially at cost)",
            "android.permission.RECORD_AUDIO": "Can record audio using the microphone",
            "android.permission.CAMERA": "Can take pictures and videos",
            "android.permission.READ_PHONE_STATE": "Can read phone status and identity",
        }
        return descriptions.get(permission, "May impact your privacy or security")

    def get_intent_description(self, intent):
        """Return a human-readable description of common Android intents"""
        descriptions = {
            "android.intent.action.BOOT_COMPLETED": "App starts automatically when device boots",
            "android.intent.action.NEW_OUTGOING_CALL": "App can monitor outgoing calls",
            "android.intent.action.SMS_RECEIVED": "App can monitor incoming text messages",
        }
        return descriptions.get(intent, "May impact your privacy or security")
    
    # Add these as new methods to your MainWindow class
    def open_dashboard(self):
        self.dashboard = Dashboard(self, self.get_user_credentials())
        self.dashboard.credentials_updated.connect(self.update_user_credentials)
        self.dashboard.show()

    def get_user_credentials(self):
        # In a real application, you would retrieve this from a database or config file
        # For now, we'll use hardcoded values or empty strings
        return {
            "user_id": "user123", 
            "password": "password123"
        }

    def update_user_credentials(self, credentials):
        # In a real application, you would save these to a database or config file
        print(f"Updated credentials: User ID: {credentials['user_id']}")
        # Don't print the password in a real application

    def train_model(self):
        try:
            # Call the MLModel's train_model method
            accuracy, cm = self.ml_model.train_model()
            self.info_text.setVisible(False)
            self.results_text.setVisible(True)

            # Display the results in the text box
            results = f"Model trained successfully!\n\n"
            results += f"Accuracy: {accuracy * 100:.2f}%\n\n"
            results += f"Confusion Matrix:\n{cm}"
            self.results_text.setText(results)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to train the model: {e}")