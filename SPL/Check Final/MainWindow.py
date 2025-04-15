from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor,QTextDocument
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter
from Dashboard import Dashboard
import sqlite3
import scan, os, datetime
from MLmodel import MLModel  
from Report import Report
class MainWindow(QWidget):
    u_id = 0
    user_name=""
    result=""
    pdf_data=""
    def __init__(self, u_id):
        super().__init__()
        self.setWindowTitle("Droid Scanner")
        self.resize(1200, 800)
        self.setWindowFlags(Qt.FramelessWindowHint) 
        self.init_ui()
        self.drag_pos = None  
        self.u_id = u_id
        self.user_name = self.get_user_name(self.u_id)
        self.Report=Report()

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
        title_label.setFont(QFont("Calibri", 18, QFont.Bold))
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
        upload_label.setFont(QFont("Calibri", 16))
        upload_label.setAlignment(Qt.AlignCenter)
        upload_label.setStyleSheet("font: bold;  margin-top: 20px;")
    
        choose_button = QPushButton("Choose File")
        choose_button.clicked.connect(self.choose_file)
        choose_button.setStyleSheet("""
            QPushButton {
                background-color: #6BC8B4;
                color: black;
                font: bold 15pt Calibri;
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

        scan_button = QPushButton("Scan Devices")
        scan_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 105, 135);
                color: black;
                font: bold 15pt Calibri;
                border-radius: 10px;
                padding: 8px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: rgb(235, 85, 115);
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
                font: bold 15pt Calibri;
                border-radius: 10px;
                padding: 8px;
                margin-top: 10px;
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
                font: bold 15pt Calibri;
                border-radius: 10px;
                padding: 8px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: rgb(235, 85, 115);
            }
        """)
        
        self.download_button = QPushButton("Download Report")
        self.download_button.clicked.connect(lambda:self.Report.download_report())
        self.download_button.setStyleSheet("""
            QPushButton {
                background-color: #6BC8B4;
                color: black;
                font: bold 15pt Calibri;
                border-radius: 10px;
                padding: 8px;
                margin-top: 10px;
            }
            QPushButton:hover {
                background-color: rgb(90, 180, 160);
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
        # left_layout.addWidget(upload_button)
        left_layout.addWidget(scan_button)
        left_layout.addStretch()
        left_layout.addWidget(self.dashboard_button)
        
        left_layout.addWidget(self.train_button)
        left_layout.addWidget(self.download_button)
        
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
            scan_instance=scan.Scan(self.u_id)
            self.file_path_label.setText(file_path)
            
            manifest_path,app_id,scan_id=scan_instance.extract_manifest(file_path,os.path.basename(file_path))

            permissions,intents=scan_instance.extract_features(manifest_path)
            scan_instance.update_database(app_id,permissions+intents)
            status=scan_instance.classify_last_apk(app_id)
            # print(status)

            if status=='Malicious':
                scan_instance.update_status(app_id)
            scan_instance.generateReport(os.path.basename(file_path),permissions,intents,status,"2.1.0" )
            scan_instance.scan_completed.connect(self.update_scan_results)
            
            classification_color = "#FF3333" if status == "Malicious" else "#33AA33"
            result=self.generate_result(os.path.basename(file_path),classification_color,status,len(permissions),len(intents))
            self.result=result
            scan_result = {
                        "package_name": os.path.basename(file_path),
                        "app_version": "2.1.0",
                        "classification": status,
                        "permissions": permissions,
                        "intents": intents,
                        "scan_id":scan_id
                    }
            html_content=self.Report.generate_report(scan_result,self.user_name)
            
            # self.results_text.setHtml(result)
            self.show_report(result)
    
    def generate_result(self,package_name,classification_color,status,permission_length,intents_length):
        result =  f"""
            <h2>Apk Scan Report</h2>
            <p><b>Package Name:</b> {package_name}</p>
            <p><b>Version:</b> {"2.1.0"}</p>
            <p><b>Classification:</b> <span style="color: {classification_color}; font-weight: bold;">{status}</span></p>
            <p><b>Total Permissions:</b> {permission_length}</p>
            <p><b>Total Intents:</b> {intents_length}</p>
            """
        if status == "Malicious":
                result += """
                <p style="color: #FF3333; font-weight: bold;font-family: Calibri, sans-serif;">This app appears to be potentially harmful. Consider the following actions:</p>
                <ul>
                    <li>Uninstall this application immediately</li>
                    <li>Check your device for other suspicious apps</li>
                    <li>Run a full system scan with an antivirus</li>
                    <li>Monitor for unusual behavior or excessive battery/data usage</li>
                </ul>
                """
        else:
                result += """
                <p style="color: #33AA33; font-family: Calibri, sans-serif;">This app appears to be safe, but always be cautious with app permissions:</p>
                <ul>
                    <li>Review permissions regularly</li>
                    <li>Consider revoking unnecessary permissions</li>
                    <li>Keep the app updated to the latest version</li>
                    <li>Only download apps from trusted sources</li>
                </ul>
                """
        return result        
        

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()

    def open_scan_window(self):
        self.scan_window = scan.Scan(self.u_id)
        self.scan_window.scan_result_type1.connect(self.update_scan_results)
        self.scan_window.scan_result_type2.connect(self.show_report)
        self.scan_window.show()
        


    def update_scan_results(self, scan_result):
        """Update the main window with scan results."""
        self.info_text.setVisible(False)
        self.results_text.setVisible(True)
        # Generate the HTML content using the helper function
        report_content = self.Report.generate_report_content(scan_result)
        # self.result=report
        # Set the formatted report to the results text area
        self.results_text.setHtml(report_content)
        self.pdf_data =self.Report.generate_report(scan_result,self.user_name)
        # print("report saved")
        self.show_report(report_content)

    # Add these as new methods to your MainWindow class
    def open_dashboard(self):
        self.dashboard = Dashboard(self, self.get_user_credentials(),self.u_id)
        self.dashboard.credentials_updated.connect(self.update_user_credentials)
        self.dashboard.show()

    def get_user_credentials(self):
        # In a real application, you would retrieve this from a database or config file
        # For now, we'll use hardcoded values or empty strings
        return {
            "id":self.u_id,
            "user_name": self.user_name, 
            "password": ""
        }

    def update_user_credentials(self, credentials):
        # In a real application, you would save these to a database or config file
        print(f"Updated credentials: User Name: {credentials['user_name']}")
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

    def show_report(self, report):
        try:
            # print(report)
            self.info_text.setVisible(False)
            self.results_text.setText(report)
            self.results_text.setVisible(True)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to Show the report: {e}")

    def get_user_name(self,u_id):
        try:
            conn = sqlite3.connect("users.db")
            cursor = conn.cursor()
            # print("connected")
            cursor.execute("SELECT username FROM users WHERE id = ?", (u_id,))
            result = cursor.fetchone()
            return result[0] if result else "Unknown User"
        except Exception as e:
            print(f"Error getting user name: {e}")
            return None
        
