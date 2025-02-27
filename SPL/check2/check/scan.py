import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QTextEdit, QLineEdit
import subprocess
import os
import shutil
import uuid
import parsing


class Scan(QWidget):
    def __init__(self):
        super().__init__()
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

        # List installed packages button
        list_packages_button = QPushButton("List Installed Packages")
        list_packages_button.clicked.connect(self.list_installed_packages)
        layout.addWidget(list_packages_button)

        # Input field for package name
        self.package_input = QLineEdit(self)
        self.package_input.setPlaceholderText("Enter Package Name")
        layout.addWidget(self.package_input)

        # Extract APK button
        extract_button = QPushButton("Extract APK")
        extract_button.clicked.connect(self.extract_apk)
        layout.addWidget(extract_button)

        # Output area
        self.output_area = QTextEdit()
        self.output_area.setReadOnly(True)
        layout.addWidget(self.output_area)

        self.setLayout(layout)

    def check_devices(self):
        """Check for connected devices using ADB."""
        try:
            result = subprocess.run(["adb", "devices"], capture_output=True, text=True, check=True)
            devices = [line.split()[0] for line in result.stdout.splitlines() if "\tdevice" in line]

            self.device_dropdown.clear()
            if devices:
                self.device_dropdown.addItems(devices)
                QMessageBox.information(self, "Devices Found", "Devices detected successfully.")
            else:
                QMessageBox.warning(self, "No Devices", "No connected devices found.")
        except subprocess.CalledProcessError as e:
            print(f"ADB Error: {e.stderr}")  # Debug print
            QMessageBox.critical(self, "ADB Error", f"Failed to fetch devices:\n{e.stderr}")
        except Exception as ex:
            print(f"Unexpected Error: {ex}")  # Catch any other error

    def list_installed_packages(self):
        """List all installed third-party packages on the selected device."""
        selected_device = self.device_dropdown.currentText()

        if not selected_device:
            QMessageBox.warning(self, "No Device Selected", "Please select a device to list installed packages.")
            return

        try:
            result = subprocess.run(
                ["adb", "-s", selected_device, "shell", "pm", "list", "packages", "-3"],
                capture_output=True, text=True, check=True
            )
            packages = [line.split(":")[1].strip() for line in result.stdout.splitlines() if line.startswith("package:")]

            if packages:
                self.output_area.setText(f"Installed packages:\n{', '.join(packages)}")
            else:
                self.output_area.setText("No third-party packages found on the device.")
        except subprocess.CalledProcessError as e:
            print(f"Error listing packages: {e.stderr}")  # Debug print
            QMessageBox.critical(self, "Error", "Failed to list installed packages.")
    
    def extract_apk(self):
        """Extract APK from the selected device based on package name."""
        selected_device = self.device_dropdown.currentText()
        package_name = self.package_input.text().strip()

        if not selected_device:
            QMessageBox.warning(self, "No Device Selected", "Please select a device.")
            return
        if not package_name:
            QMessageBox.warning(self, "No Package Name", "Please enter a valid package name.")
            return

        try:
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
            local_apk_dir = "E:\\5th Sem\\SPL-2\\new bullshit\\SPL\\check\\extracted_apks"
            os.makedirs(local_apk_dir, exist_ok=True)
            local_apk_path = os.path.join(local_apk_dir, f"{package_name}-base.apk")
            subprocess.run(["adb", "-s", selected_device, "pull", base_apk_path, local_apk_path], check=True)

            if os.path.exists(local_apk_path):
                manifest_path = self.extract_manifest(local_apk_path, local_apk_dir)
                if os.path.exists(manifest_path):
                    with open(manifest_path, 'r', encoding='utf-8') as file:
                        manifest_content = file.read()
                    self.output_area.setText(f"Extracted AndroidManifest.xml:\n\n{manifest_content}")
                    permissions = parsing.extract_permissions(manifest_path)
                    intents = parsing.extract_intents(manifest_path)
                    features=[]
                    features= permissions+intents
                    self.output_area.setText(f"Extracted Permissions:\n\n{permissions}\n{intents}")
                else:
                    QMessageBox.warning(self, "Manifest Extraction Failed", str(manifest_path))
                QMessageBox.information(self, "Success", f"APK successfully extracted to:\n{local_apk_path}")
            else:
                QMessageBox.warning(self, "Extraction Failed", "Failed to pull the APK.")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to extract APK:\n{e.stderr}")

    def extract_manifest(self,apk_path, output_dir):
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
    def delete_all_except(self,file_to_keep):
        parent_dir = os.path.dirname(file_to_keep)
        for root, dirs, files in os.walk(parent_dir, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                if file_path != file_to_keep:
                    os.remove(file_path)
            for directory in dirs:
                dir_path = os.path.join(root, directory)
                shutil.rmtree(dir_path) 

import sqlite3
import numpy as np
import joblib

def update_database(package_name, extracted_features):
    # Connect to the database
    conn = sqlite3.connect('app_data.db')
    cursor = conn.cursor()

    # Fetch all features from the permissions_intents table
    cursor.execute("SELECT Feature_Name FROM Permissions_Intents")
    all_features = [row[0] for row in cursor.fetchall()]

    # Insert matched features into app_features table
    cursor.execute("INSERT INTO App_Features (package_name) VALUES (?)", (package_name,))
    app_id = cursor.lastrowid  # Get the last inserted app_id

    for feature in extracted_features:
        if feature in all_features:
            cursor.execute("INSERT INTO app_features_features (app_id, feature_id) SELECT ?, id FROM permissions_intents WHERE feature_name = ?", (app_id, feature))

    # Commit and close the connection
    conn.commit()
    conn.close()

def classify_last_apk():
    # Connect to the database
    conn = sqlite3.connect('droid_scanner.db')
    cursor = conn.cursor()

    # Fetch the last inserted app_id from app_features
    cursor.execute("SELECT id FROM app_features ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()
    if not last_row:
        conn.close()
        return "No app data found."
    app_id = last_row[0]

    # Fetch all features from the permissions_intents table
    cursor.execute("SELECT id, feature_name FROM permissions_intents ORDER BY id")
    features_list = cursor.fetchall()

    # Initialize feature vector with zeros
    feature_vector = np.zeros(len(features_list))

    # Fetch features associated with the app_id
    cursor.execute("SELECT feature_id FROM app_features_features WHERE app_id = ?", (app_id,))
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
    prediction = model.predict(feature_vector.reshape(1, -1))
    prediction_label = 'Malicious' if prediction[0] == 'S' else 'Benign'

    return prediction_label



# # Extract APK from device
# def extract_apk(self):
#     selected_device = self.device_dropdown.currentText()
#     package_name = self.package_input.text().strip()

#     if not selected_device:
#         QMessageBox.warning(self, "No Device Selected", "Please select a device.")
#         return
#     if not package_name:
#         QMessageBox.warning(self, "No Package Name", "Please enter a valid package name.")
#         return

#     try:
#         result = subprocess.run(
#             ["adb", "-s", selected_device, "shell", "pm", "path", package_name],
#             capture_output=True, text=True, check=True
#         )
#         apk_paths = result.stdout.splitlines()
#         base_apk_path = None
#         for apk_path in apk_paths:
#             if apk_path.endswith("base.apk"):
#                 base_apk_path = apk_path.strip().split(":")[-1]
#                 break

#         if not base_apk_path:
#             QMessageBox.warning(self, "Error", "Base APK not found.")
#             return

#         # Pull APK from device
#         local_apk_dir = "E:\\5th Sem\\SPL-2\\new bullshit\\SPL\\check\\decoded_apk"
#         os.makedirs(local_apk_dir, exist_ok=True)
#         local_apk_path = os.path.join("E:\\5th Sem\\SPL-2\\new bullshit\\SPL\\check\\extracted_apks", f"{package_name}-base.apk")
#         subprocess.run(["adb", "-s", selected_device, "pull", base_apk_path, local_apk_path], check=True)

#         if os.path.exists(local_apk_path):
#             QMessageBox.information(self, "Success", f"APK successfully extracted to:\n{local_apk_path}")
#             # Extract manifest immediately after APK extraction
#             manifest_path = extract_manifest(local_apk_path, local_apk_dir)
#             if os.path.exists(manifest_path):
#                 with open(manifest_path, 'r', encoding='utf-8') as file:
#                     manifest_content = file.read()
#                 self.output_area.setText(f"Extracted AndroidManifest.xml:\n\n{manifest_content}")
#             else:
#                 QMessageBox.warning(self, "Manifest Extraction Failed", str(manifest_path))
#         else:
#             QMessageBox.warning(self, "Extraction Failed", "Failed to pull the APK.")
#     except subprocess.CalledProcessError as e:
#         QMessageBox.critical(self, "Error", f"Failed to extract APK:\n{e.stderr}")

# # Extract manifest using apktool



    

    # def extract_manifest(self):

    #     apk_path = self.package_input.text().strip()

    #     if not apk_path or not os.path.exists(apk_path):
    #         QMessageBox.warning(self, "Invalid APK Path", "Please enter a valid APK path after extraction.")
    #         return

    #     output_dir = "./decoded_apk"
    #     os.makedirs(output_dir, exist_ok=True)

    #     try:
    #         result = subprocess.run(
    #             ["apktool", "d", apk_path, "-o", output_dir, "-f"],
    #             capture_output=True, text=True, check=True
    #         )

    #         manifest_path = os.path.join(output_dir, "AndroidManifest.xml")
    #         if os.path.exists(manifest_path):
    #             with open(manifest_path, 'r', encoding='utf-8') as file:
    #                 manifest_content = file.read()
    #             self.output_area.setText(f"Extracted AndroidManifest.xml:\n\n{manifest_content}")
    #             QMessageBox.information(self, "Success", "Manifest extracted successfully.")
    #         else:
    #             QMessageBox.warning(self, "Error", "Failed to extract AndroidManifest.xml.")
    #     except subprocess.CalledProcessError as e:
    #         QMessageBox.critical(self, "Apktool Error", f"Failed to extract manifest:\n{e.stderr}")

