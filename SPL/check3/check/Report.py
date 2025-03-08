from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QFont, QPalette, QBrush, QLinearGradient, QColor,QTextDocument
from PyQt5.QtCore import Qt
from PyQt5.QtPrintSupport import QPrinter
import os,sqlite3,datetime

class Report:
    pdf_data=""
    def __init__(self, db_path="users.db"):
        self.db_path = db_path

    def generate_report_content(self, scan_result):
        """Generate the common HTML content for the scan result."""
        classification_color = "#FF3333" if scan_result["classification"] == "Malicious" else "#33AA33"
        
        report = f"""
        <h2>App Scan Report</h2>
        <p><b>Package Name:</b> {scan_result["package_name"]}</p>
        <p><b>Version:</b> {scan_result["app_version"]}</p>
        <p><b>Classification:</b> <span style="color: {classification_color}; font-weight: bold;">{scan_result["classification"]}</span></p>
        
        <h3>Security Analysis</h3>
        <p><b>Total Permissions:</b> {len(scan_result["permissions"])}</p>
        <p><b>Total Intents:</b> {len(scan_result["intents"])}</p>
        """
        
        # Add permissions list
        report += "<h3>Permissions</h3><ul style='color: #555555;'>"
        for perm in scan_result["permissions"]:
            report += f"<li>{perm}</li>"
        report += "</ul>"
        report += "<h3>Intents</h3><ul style='color: #555555;'>"
        for intents in scan_result["intents"]:
            report += f"<li>{intents}</li>"
        report += "</ul>"
        
        # Add security recommendations
        report += "<h3>Security Recommendations</h3>"
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
        
        return report

    def save_report_to_database(self, scan_id, html_content):
        """Generates a PDF from HTML and stores it in the database."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Convert HTML to PDF
            printer = QPrinter()
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName("temp_report.pdf")  # Temporary file
            document = QTextDocument()
            document.setHtml(html_content)
            document.print_(printer)

            # Read PDF as binary data
            with open("temp_report.pdf", "rb") as file:
                pdf_data = file.read()

            # Insert PDF into database
            cursor.execute("INSERT INTO Report (Scan_ID, Report_File) VALUES (?, ?)", (scan_id, pdf_data))
            conn.commit()
            conn.close()

            print("Report stored in database successfully.")
            self.pdf_data=pdf_data
            return pdf_data  # Return PDF data for downloading if needed

        except Exception as e:
            print(f"Error storing report: {e}")
            return None

    def generate_report(self, scan_result, user_name):
        """Generates a full report including scan details and results."""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        app_name = "Droid Scanner"
        logo_path = os.path.abspath("logo.png")  # Ensure 'logo.png' is in the same directory
        
        # Generate the report content
        report_content = self.generate_report_content(scan_result)
        
        # Construct full HTML report
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; font-size:14px; }}
                .header {{ text-align: center; margin-bottom: 20px; }}
                .header img {{ width: 100px; height: auto; display: block; margin: 0 auto; }} 
                .details {{ margin-bottom: 20px; }}
                .results {{ border-top: 2px solid #000; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <img src="{logo_path}" alt="App Logo">
                <h2>{app_name} - Security Report</h2>
            </div>
            <div class="details">
                <p><strong>User ID:</strong> {user_name}</p>
                <p><strong>Date:</strong> {current_date}</p>
            </div>
            <div class="results">
                {report_content}
            </div>
        </body>
        </html>
        """
        self.save_report_to_database(scan_result["scan_id"],html_content)
        return html_content

    def download_report(self):
        """Allow the user to download the report as a PDF."""
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Save Report", "", "PDF Files (*.pdf);;All Files (*)", options=options)

        if file_path and self.pdf_data:
            with open(file_path, "wb") as file:
                file.write(self.pdf_data)
            print(f"Report saved at {file_path}")
