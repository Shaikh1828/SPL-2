from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QTextEdit
from PyQt5.QtCore import pyqtSignal
import Database
import subprocess
import sqlite3
import numpy as np
import joblib, os, shutil, uuid, parsing
import pandas as pd
import MainWindow
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QTextEdit
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPalette, QLinearGradient, QColor, QBrush

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define paths to Apktool and ADB
APKTOOL_PATH = os.path.join(BASE_DIR, "apktool_2.10.0.jar")
ADB_PATH = os.path.join(BASE_DIR, "adb.exe")

class Scan(QWidget):
    scan_completed = pyqtSignal()
    scan_result_type1 = pyqtSignal(dict)  # or whatever type your first result is
    scan_result_type2 = pyqtSignal(str)
    u_id=0
    packages=[]
    scan_id=0
    def __init__(self, u_id, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Scan Devices")
        self.resize( 700, 800)
        self.set_gradient_background()
        self.u_id = u_id
        self.init_ui()
        self.db=Database.Database()
        

    def set_gradient_background(self):
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor(135, 206, 250))  
        gradient.setColorAt(1.0, QColor(70, 130, 180))   
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

    def init_ui(self):
        layout = QVBoxLayout()
        
        font = QFont("Calibri", 15, QFont.Bold)
        label_font = QFont("Calibri", 15, QFont.Bold)

        # Instructions
        instruction_label = QLabel("Connect your Android device via USB and click 'Refresh' to detect devices.")
        instruction_label.setFont(label_font)
        instruction_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(instruction_label)
        
        # Device dropdown
        self.device_dropdown = QComboBox()
        self.device_dropdown.setFont(font)
        layout.addWidget(self.device_dropdown)

        # Refresh button
        refresh_button = QPushButton("Refresh Devices")
        refresh_button.setFont(font)
        refresh_button.setStyleSheet(self.button_style())
        refresh_button.clicked.connect(self.check_devices)
        layout.addWidget(refresh_button)

        # List packages button
        list_packages_button = QPushButton("List Installed Packages")
        list_packages_button.setFont(font)
        list_packages_button.setStyleSheet(self.button_style())
        list_packages_button.clicked.connect(self.list_installed_packages)
        layout.addWidget(list_packages_button)

        # Package dropdown
        self.package_dropdown = QComboBox()
        self.package_dropdown.setFont(font)
        layout.addWidget(self.package_dropdown)

        # Extract & Scan button
        extract_button = QPushButton("Extract & Scan APK")
        extract_button.setFont(font)
        extract_button.setStyleSheet(self.button_style())
        extract_button.clicked.connect(self.handle_extraction)
        layout.addWidget(extract_button)

        # perform full scan
        full_scan_button = QPushButton("Full Scan")
        full_scan_button.setFont(font)
        full_scan_button.setStyleSheet(self.button_style())
        full_scan_button.clicked.connect(self.handle_full_scan)
        layout.addWidget(full_scan_button)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        self.output_area.setFont(font)
        self.output_area.setStyleSheet("background-color: white; color: black; padding: 10px;")
        layout.addWidget(self.output_area)

        self.setLayout(layout)
    
    def button_style(self):
        return (
            "QPushButton {"
            "background-color: #4682B4;"
            "color: black;"
            "border-radius: 10px;"
            "padding: 10px;"
            "font-weight: bold;"
            "}" 
            "QPushButton:hover { background-color: #5A9BD5; }"
        )


    def check_devices(self):
        """Check if any device is connected."""
        try:
            result = subprocess.run([ADB_PATH, "devices"], capture_output=True, text=True, check=True)
            devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip() and "device" in line]

            if devices:
                self.device_dropdown.clear()
                self.device_dropdown.addItems(devices)
                self.output_area.setText(f"Connected devices:\n{', '.join(devices)}")

                # Connect dropdown selection to method
                #self.device_dropdown.currentIndexChanged.connect(lambda:self.device_selected)
            else:
                self.output_area.setText("No connected devices found.")
                QMessageBox.warning(self, "No Devices", "No connected devices found.")
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error checking devices:\n{e.stderr}")
            QMessageBox.critical(self, "Error", "Failed to check connected devices.")


    def list_installed_packages(self):
        """List all installed third-party packages on the selected device."""
        selected_device = self.device_dropdown.currentText()

        if not selected_device:
            QMessageBox.warning(self, "No Device Selected", "Please select a device to list installed packages.")
            return

        try:
            result = subprocess.run(
                [ADB_PATH, "-s", selected_device, "shell", "pm", "list", "packages", "-3"],
                capture_output=True, text=True, check=True
            )
            packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if line.startswith("package:")]
            self.packages=packages
            if packages:
                self.package_dropdown.clear()
                self.package_dropdown.addItems(packages)
                self.output_area.setText(f"Installed packages:\n{', '.join(packages)}")
                return packages
            else:
                self.output_area.setText("No third-party packages found on the device.")
        except subprocess.CalledProcessError as e:
            print(f"Error listing packages: {e.stderr}")  # Debug print
            QMessageBox.critical(self, "Error", "Failed to list installed packages.")

    def handle_extraction(self):
        apk_path,package_name,app_version=self.extract_apk()
        print("extraction ok")
        existing_app,app_id =self.db.previously_scanned(package_name,app_version)
        print(app_id)
        if existing_app==False:
            # print("new")
            manifest_path,appid,scan_id=self.extract_manifest(apk_path,package_name,app_version)
            # print("manifest ok")
            permissions,intents=self.extract_features(manifest_path)
            # print("permission ok")
            self.update_database(appid,permissions+intents)
            # print("database ok")
            status=self.classify_last_apk(appid)
            print(status)
            if status=='Malicious':
                self.update_status(appid)
            print("Updated")
        else:
            print("old")
            self.scan_id=self.db.log_scan(self.u_id,app_id)
            print(self.scan_id)
            features,status=self.db.get_permission_intent_status(app_id)
            mid=len(features)//2
            permissions=features[:mid]
            intents=features[mid:]
        self.generateReport(package_name,permissions,intents,status,app_version)
    
    def handle_full_scan(self):
        print("hello1")
        report = f"""<h2>Full Scan Report</h2> """
        for package_name in self.packages:
            try:
                # print("hello2")
                
                print(f"Scanning package: {package_name}")
                apk_path, packagename,app_version = self.extract_apk(package_name)
                manifest_path, app_id ,scan_id= self.extract_manifest(apk_path, package_name,app_version)
                #self.update_version(app_id,app_version)
                permissions,intents = self.extract_features(manifest_path)
                self.update_database(app_id, permissions+intents)
                status = self.classify_last_apk(app_id)
                
                if status == 'Malicious':
                    self.update_status(app_id)
                    print(f"{package_name} is Malicious. Status updated.")
                else:
                    print(f"{package_name} is Benign.")
                self.generateReport(package_name,permissions,intents,status,app_version)
            except Exception as e:
                print(f"Error scanning {package_name}: {e}")
                
            classification_color = "#FF3333" if status == "Malicious" else "#33AA33"
        
            report += f"""
            
            <p><b>Package Name:</b> {package_name}</p>
            <p><b>Version:</b> {app_version}</p>
            <p><b>Classification:</b> <span style="color: {classification_color}; font-weight: bold;">{status}</span></p>
            <p><b>Total Permissions:</b> {len(permissions)}</p>
            <p><b>Total Intents:</b> {len(intents)}</p>
            <p><b>   ---</p>
            """
        print("Full scan completed.")
        # MainWindow.MainWindow.show_report(report)
        self.scan_result_type2.emit(report)

    

    def device_selected(self):
        """Trigger when a device is selected from the dropdown."""
        selected_device = self.device_dropdown.currentText()
        if selected_device:
            self.list_installed_packages(selected_device)


    def extract_apk(self,package_name=None):
        selected_device = self.device_dropdown.currentText()
        
        
        if not selected_device:
            QMessageBox.warning(self, "No Device Selected", "Please select a device.")
            return
        if package_name is None:
            package_name = self.package_dropdown.currentText()

        if not package_name:
            QMessageBox.warning(self, "No Package Name", "Please enter a valid package name.")
            return
        

        try:
            # Get app version
            version_result = subprocess.run(
                [ADB_PATH, "-s", selected_device, "shell", "dumpsys", "package", package_name, "| grep", "versionName"],
                capture_output=True, text=True, shell=True
            )
            app_version = "Unknown"
            if version_result.stdout:
                version_lines = version_result.stdout.strip().split('\n')
                if version_lines:
                    app_version = version_lines[0].strip().split('=')[-1]
            
            # Find APK path
            result = subprocess.run(
                [ADB_PATH, "-s", selected_device, "shell", "pm", "path", package_name],
                capture_output=True, text=True, check=True
            )
            apk_paths = result.stdout.splitlines()
            base_apk_path = None
            for apk_path in apk_paths:
                if apk_path.endswith("base.apk"):
                    base_apk_path = apk_path.strip().split(":")[-1]
                    break

            if not base_apk_path:
                QMessageBox.warning(self, "Error", "Base APK not found.")
                return

            # Pull APK from device
            local_apk_dir = "extracted_apks"
            os.makedirs(local_apk_dir, exist_ok=True)
            local_apk_path = os.path.join(local_apk_dir, f"{package_name}-base.apk")
            subprocess.run([ADB_PATH, "-s", selected_device, "pull", base_apk_path, local_apk_path], check=True)

            return local_apk_path,package_name,app_version
                        
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to extract APK:\n{e.stderr}")
    

    def generateReport(self,package_name,permissions,intents,classification,app_version="2.1.0"):
        print("generating yes")
        scan_result = {
                        "package_name": package_name,
                        "app_version": app_version,
                        "classification": classification,
                        "permissions": permissions,
                        "intents": intents,
                        "scan_id":self.scan_id
                    }
                    
                    # Display basic info in the scan window
        self.output_area.setText(f"App: {package_name}\nVersion: {app_version}\nClassification: {classification}\n\n"
                                 f"Total Permissions: {len(permissions)}\n"
                                 f"Permissions List: {permissions}\n"
                                 f"Total Intents: {len(intents)}\n"
                                 f"Intents List: {intents}\n")
                    
                    # Emit the signal with scan results to update the main window
        # if self.parent:
        print("generating ok")
        self.scan_result_type1.emit(scan_result)


       
    def extract_features(self,manifest_path):
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as file:
                manifest_content = file.read()
            self.output_area.setText(f"Extracted AndroidManifest.xml:\n\n{manifest_content}")
            permissions = parsing.extract_permissions(manifest_path)
            intents = parsing.extract_intents(manifest_path)
            features=[]
            features= permissions+intents
            self.output_area.setText(f"Extracted Permissions:\n\n{permissions}\n{intents}")
            return permissions,intents
        else:
            QMessageBox.warning(self, "Manifest Extraction Failed", str(manifest_path))

    def extract_manifest(self,apk_path, package_name,app_version="2.1.0",output_dir="extracted_apks"):
        if os.path.exists(apk_path):
            app_id=self.db.store_apk_in_db(apk_path, package_name,app_version)
            self.scan_id=self.db.log_scan(self.u_id,app_id)
            
            temp_dir = os.path.join(output_dir, uuid.uuid4().hex)
            os.makedirs(temp_dir, exist_ok=True)
            try:
                command = [
                    "java", "-Xmx4G", "-jar", APKTOOL_PATH, "d", apk_path, "-o", temp_dir, "--no-src", "-f"
                ]
                result = subprocess.run(command, capture_output=True, text=True)
                if result.returncode == 0:
                    manifest_path = os.path.join(temp_dir, "AndroidManifest.xml")
                    if os.path.exists(manifest_path):
                        self.delete_all_except(manifest_path)
                        return manifest_path,app_id,self.scan_id
                    else:
                        shutil.rmtree(temp_dir)
                        return "Manifest file not found in APK."
                else:
                    return f"Error: {result.stderr}"
            except Exception as e:
                return f"An error occurred: {e}"
        else:
                QMessageBox.warning(self, "Extraction Failed", "Failed to pull the Manifest File.")

    # Clean up extracted directory
    def delete_all_except(self, file_to_keep):
        parent_dir = os.path.dirname(file_to_keep)
        for root, dirs, files in os.walk(parent_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path != file_to_keep:
                    os.remove(file_path)
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                shutil.rmtree(dir_path) 

    def update_database(self,app_id, extracted_features):
        # Connect to the database
        conn = sqlite3.connect('app_data.db')
        cursor = conn.cursor()

        # Fetch all features from the permissions_intents table
        cursor.execute("SELECT Feature_Name FROM Permissions_Intents")
        all_features = [row[0] for row in cursor.fetchall()]
        
        for feature in extracted_features:
            if feature in all_features:
                cursor.execute("INSERT INTO App_Features (App_ID, Feature_ID) SELECT ?, Feature_ID FROM permissions_intents WHERE Feature_Name = ?", (app_id, feature))

        # Commit and close the connection
        conn.commit()
        conn.close()

    def classify_last_apk(self,app_id):
        # Connect to the database
        conn = sqlite3.connect('app_data.db')
        cursor = conn.cursor()

        print(app_id)
        cursor.execute("SELECT Feature_ID, Feature_Name FROM Permissions_Intents ORDER BY Feature_ID")
        features_list = cursor.fetchall()

        # Initialize feature vector with zeros
        feature_vector = np.zeros(len(features_list))
        
        # Fetch features associated with the app_id
        cursor.execute("SELECT Feature_ID FROM App_Features WHERE app_id = ?", (app_id,))
        matched_features = {row[0] for row in cursor.fetchall()}

        # Mark matched features as 1 in the feature vector
        for index, (feature_id, _) in enumerate(features_list):
            if feature_id in matched_features:
                feature_vector[index] = 1

        # Close database connection
        conn.close()

        # Load the ML model
        with open('AppClassifier1.joblib', 'rb') as f:
            model = joblib.load(f)

        # Reshape and predict
        feature_names = joblib.load('feature_names.joblib')

        feature_vector_df = pd.DataFrame([feature_vector], columns=feature_names)
        
        # Predict
        prediction = model.predict(feature_vector_df)
        prediction_label = 'Malicious' if prediction[0] == 'S' else 'Benign'

        return prediction_label
    
    def update_status(self,app_id):
        conn = sqlite3.connect('app_data.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE App SET Status = ? WHERE App_ID = ?", ("Malicious", app_id))
        print("Status Updated Successfully")
        conn.commit()
        conn.close()
    
    