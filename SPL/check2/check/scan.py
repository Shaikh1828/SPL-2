# # from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QTextEdit
# # import subprocess

# # class Scan(QWidget):
# #     def __init__(self):
# #         super().__init__()
# #         self.setWindowTitle("Scan Devices")
# #         self.resize(600, 400)
# #         self.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
# #         self.init_ui()

# #     def init_ui(self):
# #         layout = QVBoxLayout()

# #         # Instructions
# #         instruction_label = QLabel("Connect your Android device via USB and click 'Refresh' to detect devices.")
# #         layout.addWidget(instruction_label)

# #         # Device dropdown
# #         self.device_dropdown = QComboBox()
# #         layout.addWidget(self.device_dropdown)

# #         # Refresh button
# #         refresh_button = QPushButton("Refresh Devices")
# #         refresh_button.clicked.connect(self.check_devices)
# #         layout.addWidget(refresh_button)

# #         # List packages button
# #         list_packages_button = QPushButton("List Installed Packages")
# #         list_packages_button.clicked.connect(self.list_installed_packages)
# #         layout.addWidget(list_packages_button)

# #         # Output area
# #         self.output_area = QTextEdit()
# #         self.output_area.setReadOnly(True)
# #         layout.addWidget(self.output_area)

# #         self.setLayout(layout)

# #     def check_devices(self):
# #         """Check if any device is connected."""
# #         try:
# #             result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
# #             devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip() and "device" in line]

# #             if devices:
# #                 self.device_dropdown.clear()
# #                 self.device_dropdown.addItems(devices)
# #                 self.output_area.setText(f"Connected devices:\n{', '.join(devices)}")
# #             else:
# #                 self.output_area.setText("No connected devices found.")
# #                 QMessageBox.warning(self, "No Devices", "No connected devices found.")
# #         except subprocess.CalledProcessError as e:
# #             self.output_area.setText(f"Error checking devices:\n{e.stderr}")
# #             QMessageBox.critical(self, "Error", "Failed to check connected devices.")

# #     def list_installed_packages(self):
# #         """List all installed packages on the selected device."""
# #         selected_device = self.device_dropdown.currentText()

# #         if not selected_device:
# #             QMessageBox.warning(self, "No Device Selected", "Please select a device to list installed packages.")
# #             return

# #         try:
# #             result = subprocess.run(["adb","-s", selected_device, "shell", "pm", "list", "packages", "-3"], capture_output=True, text=True, check=True)
# #             packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if line.startswith("package:")]

# #             if packages:
# #                 self.output_area.setText(f"Installed packages:\n{', '.join(packages)}")
# #             else:
# #                 self.output_area.setText("No third-party packages found on the device.")
# #                 QMessageBox.information(self, "No Packages", "No third-party packages found on the device.")
# #         except subprocess.CalledProcessError as e:
# #             self.output_area.setText(f"Error listing packages:\n{e.stderr}")
# #             QMessageBox.critical(self, "Error", "Failed to list installed packages.")


# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QTextEdit
# import subprocess
# import sqlite3
# import numpy as np
# import joblib, os, shutil, uuid, parsing

# class Scan(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Scan Devices")
#         self.resize(600, 400)
#         self.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
#         self.init_ui()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         # Instructions
#         instruction_label = QLabel("Connect your Android device via USB and click 'Refresh' to detect devices.")
#         layout.addWidget(instruction_label)

#         # Device dropdown
#         self.device_dropdown = QComboBox()
#         layout.addWidget(self.device_dropdown)

#         # Refresh button
#         refresh_button = QPushButton("Refresh Devices")
#         refresh_button.clicked.connect(self.check_devices)
#         layout.addWidget(refresh_button)

#         # List packages button
#         list_packages_button = QPushButton("List Installed Packages")
#         list_packages_button.clicked.connect(self.list_installed_packages)
#         layout.addWidget(list_packages_button)

#         # Package dropdown
#         self.package_dropdown = QComboBox()
#         layout.addWidget(self.package_dropdown)
#         selected_device = self.device_dropdown.currentText()
#         selected_package = self.package_dropdown.currentText()
#         extract_button = QPushButton("Extract APK")
#         extract_button.clicked.connect(self.extract_apk)
#         layout.addWidget(extract_button)

#         # Open package button
#         # self.open_package_button = QPushButton("Open Selected Package")
#         # self.open_package_button.clicked.connect(self.open_selected_package)
#         # layout.addWidget(self.open_package_button)

#         # Output area
#         self.output_area = QTextEdit()
#         self.output_area.setReadOnly(True)
#         layout.addWidget(self.output_area)

#         self.setLayout(layout)

#     def check_devices(self):
#         """Check if any device is connected."""
#         try:
#             result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
#             devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip() and "device" in line]

#             if devices:
#                 self.device_dropdown.clear()
#                 self.device_dropdown.addItems(devices)
#                 self.output_area.setText(f"Connected devices:\n{', '.join(devices)}")
#             else:
#                 self.output_area.setText("No connected devices found.")
#                 QMessageBox.warning(self, "No Devices", "No connected devices found.")
#         except subprocess.CalledProcessError as e:
#             self.output_area.setText(f"Error checking devices:\n{e.stderr}")
#             QMessageBox.critical(self, "Error", "Failed to check connected devices.")

#     def list_installed_packages(self):
#         """List all installed packages on the selected device."""
#         selected_device = self.device_dropdown.currentText()

#         if not selected_device:
#             QMessageBox.warning(self, "No Device Selected", "Please select a device to list installed packages.")
#             return

#         try:
#             result = subprocess.run(["adb", "-s", selected_device, "shell", "pm", "list", "packages", "-3"], capture_output=True, text=True, check=True)
#             packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if line.startswith("package:")]

#             if packages:
#                 self.package_dropdown.clear()
#                 self.package_dropdown.addItems(packages)
#                 self.output_area.setText(f"Installed packages:\n{', '.join(packages)}")
#             else:
#                 self.package_dropdown.clear()
#                 self.output_area.setText("No third-party packages found on the device.")
#                 QMessageBox.information(self, "No Packages", "No third-party packages found on the device.")
#         except subprocess.CalledProcessError as e:
#             self.output_area.setText(f"Error listing packages:\n{e.stderr}")
#             QMessageBox.critical(self, "Error", "Failed to list installed packages.")

#     # def open_selected_package(self):
#     #     """Open the selected package on the connected device."""
#     #     selected_device = self.device_dropdown.currentText()
#     #     selected_package = self.package_dropdown.currentText()

#     #     if not selected_device:
#     #         QMessageBox.warning(self, "No Device Selected", "Please select a device before opening a package.")
#     #         return

#     #     if not selected_package:
#     #         QMessageBox.warning(self, "No Package Selected", "Please select a package from the dropdown.")
#     #         return

#     #     try:
#     #         subprocess.run(["adb", "-s", selected_device, "shell", "monkey", "-p", selected_package, "-c", "android.intent.category.LAUNCHER", "1"], check=True)
#     #         self.output_area.setText(f"Opened package: {selected_package}")
#     #     except subprocess.CalledProcessError as e:
#     #         self.output_area.setText(f"Error opening package:\n{e.stderr}")
#     #         QMessageBox.critical(self, "Error", "Failed to open the selected package.")


#     def extract_apk(self):
#         selected_device = self.device_dropdown.currentText()
#         package_name = self.package_dropdown.currentText()
#         """Extract APK from the selected device based on package name."""
       
#         if not selected_device:
#             QMessageBox.warning(self, "No Device Selected", "Please select a device.")
#             return
#         if not package_name:
#             QMessageBox.warning(self, "No Package Name", "Please enter a valid package name.")
#             return

#         try:
#             result = subprocess.run(
#                 ["adb", "-s", selected_device, "shell", "pm", "path", package_name],
#                 capture_output=True, text=True, check=True
#             )
#             apk_paths = result.stdout.splitlines()
#             base_apk_path = None
#             for apk_path in apk_paths:
#                 if apk_path.endswith("base.apk"):
#                     base_apk_path = apk_path.strip().split(":")[-1]
#                     break

#             if not base_apk_path:
#                 QMessageBox.warning(self, "Error", "Base APK not found.")
#                 return

#             # Pull APK from device
#             local_apk_dir = "D:\\Git\\SPL-2\\SPL\\check2\\check copy\\extracted_apks"
#             os.makedirs(local_apk_dir, exist_ok=True)
#             local_apk_path = os.path.join(local_apk_dir, f"{package_name}-base.apk")
#             subprocess.run(["adb", "-s", selected_device, "pull", base_apk_path, local_apk_path], check=True)

#             if os.path.exists(local_apk_path):
#                 manifest_path = self.extract_manifest(local_apk_path, local_apk_dir)
#                 if os.path.exists(manifest_path):
#                     with open(manifest_path, 'r', encoding='utf-8') as file:
#                         manifest_content = file.read()
#                     self.output_area.setText(f"Extracted AndroidManifest.xml:\n\n{manifest_content}")
#                     permissions = parsing.extract_permissions(manifest_path)
#                     intents = parsing.extract_intents(manifest_path)
#                     features=[]
#                     features= permissions+intents
#                     self.output_area.setText(f"Extracted Permissions:\n\n{permissions}\n{intents}")
#                 else:
#                     QMessageBox.warning(self, "Manifest Extraction Failed", str(manifest_path))
#                 QMessageBox.information(self, "Success", f"APK successfully extracted to:\n{local_apk_path}")
#             else:
#                 QMessageBox.warning(self, "Extraction Failed", "Failed to pull the APK.")
#         except subprocess.CalledProcessError as e:
#             QMessageBox.critical(self, "Error", f"Failed to extract APK:\n{e.stderr}")

#     def extract_manifest(self,apk_path, output_dir):
#         apktool_jar = "C:\\apktool\\apktool_2.10.0.jar"
#         temp_dir = os.path.join(output_dir, uuid.uuid4().hex)
#         os.makedirs(temp_dir, exist_ok=True)
#         try:
#             command = [
#                 "java", "-Xmx4G", "-jar", apktool_jar, "d", apk_path, "-o", temp_dir, "--no-src", "-f"
#             ]
#             result = subprocess.run(command, capture_output=True, text=True)
#             if result.returncode == 0:
#                 manifest_path = os.path.join(temp_dir, "AndroidManifest.xml")
#                 if os.path.exists(manifest_path):
#                     self.delete_all_except(manifest_path)
#                     return manifest_path
#                 else:
#                     shutil.rmtree(temp_dir)
#                     return "Manifest file not found in APK."
#             else:
#                 return f"Error: {result.stderr}"
#         except Exception as e:
#             return f"An error occurred: {e}"

#     # Clean up extracted directory
#     def delete_all_except(self,file_to_keep):
#         parent_dir = os.path.dirname(file_to_keep)
#         for root, dirs, files in os.walk(parent_dir, topdown=False):
#             for file in files:
#                 file_path = os.path.join(root, file)
#                 if file_path != file_to_keep:
#                     os.remove(file_path)
#             for directory in dirs:
#                 dir_path = os.path.join(root, directory)
#                 shutil.rmtree(dir_path) 


#     def update_database(package_name, extracted_features):
#         # Connect to the database
#         conn = sqlite3.connect('D:\\Git\\SPL-2\\SPL\\check2\\check copy\\app_data.db')
#         cursor = conn.cursor()

#         # Fetch all features from the permissions_intents table
#         cursor.execute("SELECT Feature_Name FROM Permissions_Intents")
#         all_features = [row[0] for row in cursor.fetchall()]

#         # Insert matched features into app_features table
#         cursor.execute("INSERT INTO App_Features (package_name) VALUES (?)", (package_name,))
#         app_id = cursor.lastrowid  # Get the last inserted app_id

#         for feature in extracted_features:
#             if feature in all_features:
#                 cursor.execute("INSERT INTO app_features_features (app_id, feature_id) SELECT ?, id FROM permissions_intents WHERE feature_name = ?", (app_id, feature))

#         # Commit and close the connection
#         conn.commit()
#         conn.close()

#     def classify_last_apk():
#         # Connect to the database
#         conn = sqlite3.connect('droid_scanner.db')
#         cursor = conn.cursor()

#         # Fetch the last inserted app_id from app_features
#         cursor.execute("SELECT id FROM app_features ORDER BY id DESC LIMIT 1")
#         last_row = cursor.fetchone()
#         if not last_row:
#             conn.close()
#             return "No app data found."
#         app_id = last_row[0]

#         # Fetch all features from the permissions_intents table
#         cursor.execute("SELECT id, feature_name FROM permissions_intents ORDER BY id")
#         features_list = cursor.fetchall()

#         # Initialize feature vector with zeros
#         feature_vector = np.zeros(len(features_list))

#         # Fetch features associated with the app_id
#         cursor.execute("SELECT feature_id FROM app_features_features WHERE app_id = ?", (app_id,))
#         matched_features = {row[0] for row in cursor.fetchall()}

#         # Mark matched features as 1 in the feature vector
#         for index, (feature_id, _) in enumerate(features_list):
#             if feature_id in matched_features:
#                 feature_vector[index] = 1

#         # Close database connection
#         conn.close()

#         # Load the ML model
#         with open('AppClassifier1.joblib', 'rb') as f:
#             model = joblib.load(f)

#         # Reshape and predict
#         prediction = model.predict(feature_vector.reshape(1, -1))
#         prediction_label = 'Malicious' if prediction[0] == 'S' else 'Benign'

#         return prediction_label


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QTextEdit
from PyQt5.QtCore import pyqtSignal
import subprocess
import sqlite3
import numpy as np
import joblib, os, shutil, uuid, parsing

class Scan(QWidget):
    # Add signal to communicate with MainWindow
    scan_completed = pyqtSignal(dict)
    
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Scan Devices")
        self.resize(600, 400)
        self.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Instructions
        instruction_label = QLabel("Connect your Android device via USB and click 'Refresh' to detect devices.")
        layout.addWidget(instruction_label)

        # Device dropdown
        self.device_dropdown = QComboBox()
        layout.addWidget(self.device_dropdown)

        # Refresh button
        refresh_button = QPushButton("Refresh Devices")
        refresh_button.clicked.connect(self.check_devices)
        layout.addWidget(refresh_button)

        # List packages button
        list_packages_button = QPushButton("List Installed Packages")
        list_packages_button.clicked.connect(self.list_installed_packages)
        layout.addWidget(list_packages_button)

        # Package dropdown
        self.package_dropdown = QComboBox()
        layout.addWidget(self.package_dropdown)
        
        # Extract & Scan button
        extract_button = QPushButton("Extract & Scan APK")
        extract_button.clicked.connect(self.extract_and_scan_apk)
        layout.addWidget(extract_button)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        self.setLayout(layout)

    def check_devices(self):
        """Check if any device is connected."""
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
            devices = [line.split()[0] for line in result.stdout.splitlines()[1:] if line.strip() and "device" in line]

            if devices:
                self.device_dropdown.clear()
                self.device_dropdown.addItems(devices)
                self.output_area.setText(f"Connected devices:\n{', '.join(devices)}")
            else:
                self.output_area.setText("No connected devices found.")
                QMessageBox.warning(self, "No Devices", "No connected devices found.")
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error checking devices:\n{e.stderr}")
            QMessageBox.critical(self, "Error", "Failed to check connected devices.")

    def list_installed_packages(self):
        """List all installed packages on the selected device."""
        selected_device = self.device_dropdown.currentText()

        if not selected_device:
            QMessageBox.warning(self, "No Device Selected", "Please select a device to list installed packages.")
            return

        try:
            result = subprocess.run(["adb", "-s", selected_device, "shell", "pm", "list", "packages", "-3"], capture_output=True, text=True, check=True)
            packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if line.startswith("package:")]

            if packages:
                self.package_dropdown.clear()
                self.package_dropdown.addItems(packages)
                self.output_area.setText(f"Installed packages:\n{', '.join(packages)}")
            else:
                self.package_dropdown.clear()
                self.output_area.setText("No third-party packages found on the device.")
                QMessageBox.information(self, "No Packages", "No third-party packages found on the device.")
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error listing packages:\n{e.stderr}")
            QMessageBox.critical(self, "Error", "Failed to list installed packages.")

    def extract_and_scan_apk(self):
        selected_device = self.device_dropdown.currentText()
        package_name = self.package_dropdown.currentText()
        
        if not selected_device:
            QMessageBox.warning(self, "No Device Selected", "Please select a device.")
            return
        if not package_name:
            QMessageBox.warning(self, "No Package Name", "Please enter a valid package name.")
            return

        try:
            # Get app version
            version_result = subprocess.run(
                ["adb", "-s", selected_device, "shell", "dumpsys", "package", package_name, "| grep", "versionName"],
                capture_output=True, text=True, shell=True
            )
            app_version = "Unknown"
            if version_result.stdout:
                version_lines = version_result.stdout.strip().split('\n')
                if version_lines:
                    app_version = version_lines[0].strip().split('=')[-1]

            # Find APK path
            result = subprocess.run(
                ["adb", "-s", selected_device, "shell", "pm", "path", package_name],
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
            local_apk_dir = "D:\\Git\\SPL-2\\SPL\\check2\\check copy\\extracted_apks"
            os.makedirs(local_apk_dir, exist_ok=True)
            local_apk_path = os.path.join(local_apk_dir, f"{package_name}-base.apk")
            subprocess.run(["adb", "-s", selected_device, "pull", base_apk_path, local_apk_path], check=True)

            permissions = []
            intents = []
            scan_result = {
                "package_name": package_name,
                "app_version": app_version,
                "classification": "Unknown",
                "permissions": [],
                "intents": [],
                "suspicious_permissions": [],
                "suspicious_intents": []
            }

            if os.path.exists(local_apk_path):
                manifest_path = self.extract_manifest(local_apk_path, local_apk_dir)
                if os.path.exists(manifest_path):
                    # Extract permissions and intents
                    permissions = parsing.extract_permissions(manifest_path)
                    intents = parsing.extract_intents(manifest_path)
                    
                    # List of potentially suspicious permissions (you can expand this list)
                    suspicious_permission_list = [
                        "android.permission.READ_CONTACTS",
                        "android.permission.WRITE_CONTACTS",
                        "android.permission.ACCESS_FINE_LOCATION",
                        "android.permission.READ_CALL_LOG",
                        "android.permission.READ_SMS",
                        "android.permission.SEND_SMS",
                        "android.permission.RECORD_AUDIO",
                        "android.permission.CAMERA",
                        "android.permission.READ_PHONE_STATE"
                    ]
                    
                    # List of potentially suspicious intents (you can expand this list)
                    suspicious_intent_list = [
                        "android.intent.action.BOOT_COMPLETED",
                        "android.intent.action.NEW_OUTGOING_CALL",
                        "android.intent.action.SMS_RECEIVED"
                    ]
                    
                    # Find suspicious permissions and intents
                    suspicious_permissions = [p for p in permissions if p in suspicious_permission_list]
                    suspicious_intents = [i for i in intents if i in suspicious_intent_list]
                    
                    # Classify the app (simplified version, use your ML model in production)
                    classification = self.classify_app(permissions, intents)
                    
                    scan_result = {
                        "package_name": package_name,
                        "app_version": app_version,
                        "classification": classification,
                        "permissions": permissions,
                        "intents": intents,
                        "suspicious_permissions": suspicious_permissions,
                        "suspicious_intents": suspicious_intents
                    }
                    
                    # Display basic info in the scan window
                    self.output_area.setText(f"App: {package_name}\nVersion: {app_version}\nClassification: {classification}\n\n"
                                            f"Total Permissions: {len(permissions)}\nSuspicious Permissions: {len(suspicious_permissions)}\n"
                                            f"Total Intents: {len(intents)}\nSuspicious Intents: {len(suspicious_intents)}")
                    
                    # Emit the signal with scan results to update the main window
                    if self.parent:
                        self.scan_completed.emit(scan_result)
                else:
                    QMessageBox.warning(self, "Manifest Extraction Failed", str(manifest_path))
                QMessageBox.information(self, "Scan Completed", f"APK successfully scanned. Results are available in the main window.")
            else:
                QMessageBox.warning(self, "Extraction Failed", "Failed to pull the APK.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to extract APK:\n{e.stderr}")

    def extract_manifest(self, apk_path, output_dir):
        apktool_jar = "C:\\apktool\\apktool_2.10.0.jar"
        temp_dir = os.path.join(output_dir, uuid.uuid4().hex)
        os.makedirs(temp_dir, exist_ok=True)
        try:
            command = [
                "java", "-Xmx4G", "-jar", apktool_jar, "d", apk_path, "-o", temp_dir, "--no-src", "-f"
            ]
            result = subprocess.run(command, capture_output=True, text=True)
            if result.returncode == 0:
                manifest_path = os.path.join(temp_dir, "AndroidManifest.xml")
                if os.path.exists(manifest_path):
                    self.delete_all_except(manifest_path)
                    return manifest_path
                else:
                    shutil.rmtree(temp_dir)
                    return "Manifest file not found in APK."
            else:
                return f"Error: {result.stderr}"
        except Exception as e:
            return f"An error occurred: {e}"

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

    def classify_app(self, permissions, intents):
        """Simplified classification for demonstration. 
        In production, you would load your ML model and perform proper classification."""
        try:
            # Load the model
            model_path = "AppClassifier1.joblib"
            if not os.path.exists(model_path):
                return "Unknown (Model not found)"
                
            model = joblib.load(model_path)
            
            # Create feature vector - this is simplified and should match how your model was trained
            # You'll need to adapt this based on your actual model implementation
            all_known_features = self.get_all_known_features()
            feature_vector = np.zeros(len(all_known_features))
            
            for i, feature in enumerate(all_known_features):
                if feature in permissions or feature in intents:
                    feature_vector[i] = 1
                    
            # Predict
            prediction = model.predict(feature_vector.reshape(1, -1))
            if prediction[0] == 'S':
                return "Malicious"
            else:
                return "Benign"
        except Exception as e:
            print(f"Classification error: {e}")
            return "Error in classification"
    
    def get_all_known_features(self):
        """Get all known features (permissions and intents) that the model was trained on.
        This is a placeholder - you should replace it with your actual features."""
        # This should return the exact set of features your model was trained on
        # For demonstration, we'll use a simplified list
        try:
            # Check if we can load features from a database
            conn = sqlite3.connect("app_data.db")
            cursor = conn.cursor()
            cursor.execute("SELECT Feature_Name FROM Permissions_Intents")
            features = [row[0] for row in cursor.fetchall()]
            conn.close()
            if features:
                return features
        except Exception as e:
            print(f"Error loading features from database: {e}")
            
        # Fallback to a simplified list
        return [
            "android.permission.INTERNET",
            "android.permission.ACCESS_NETWORK_STATE",
            "android.permission.READ_EXTERNAL_STORAGE",
            "android.permission.WRITE_EXTERNAL_STORAGE",
            "android.permission.READ_CONTACTS",
            "android.permission.CAMERA",
            "android.permission.ACCESS_FINE_LOCATION",
            "android.permission.READ_PHONE_STATE",
            "android.intent.action.MAIN",
            "android.intent.category.LAUNCHER",
            "android.intent.action.BOOT_COMPLETED"
        ]