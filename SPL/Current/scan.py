from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QTextEdit
import subprocess


class Scan(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scan Devices")
        self.resize(600, 400)
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
                self.output_area.setText(f"Installed packages:\n{', '.join(packages)}")
            else:
                self.output_area.setText("No third-party packages found on the device.")
                QMessageBox.information(self, "No Packages", "No third-party packages found on the device.")
        except subprocess.CalledProcessError as e:
            self.output_area.setText(f"Error listing packages:\n{e.stderr}")
            QMessageBox.critical(self, "Error", "Failed to list installed packages.")
