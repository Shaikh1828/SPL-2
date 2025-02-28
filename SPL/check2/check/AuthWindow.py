# auth_windows.py
from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QLineEdit, 
    QMessageBox, QDialog, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from Authentication import Authentication
from Database import Database

class VerificationDialog(QDialog):
    def __init__(self, email, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Email Verification")
        self.setFixedWidth(300)
        self.email = email
        
        layout = QVBoxLayout()
        
        info_label = QLabel(f"Verification code sent to:\n{email}")
        info_label.setWordWrap(True)
        info_label.setAlignment(Qt.AlignCenter)
        
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter 6-digit verification code")
        self.code_input.setMaxLength(6)
        
        verify_button = QPushButton("Verify")
        verify_button.clicked.connect(self.accept)
        
        resend_button = QPushButton("Resend Code")
        resend_button.clicked.connect(self.resend_code)
        
        layout.addWidget(info_label)
        layout.addWidget(QLabel("Please enter the verification code:"))
        layout.addWidget(self.code_input)
        layout.addWidget(verify_button)
        layout.addWidget(resend_button)
        
        self.setLayout(layout)

    def get_code(self):
        return self.code_input.text()
        
    def resend_code(self):
        # Signal to parent that code should be resent
        self.parent().resend_verification_code(self.email)
        QMessageBox.information(
            self,
            "Code Resent",
            "A new verification code has been sent to your email."
        )

class AuthWindows(QWidget):
    # List of allowed organizational domains for business users
    ALLOWED_ORG_DOMAINS = ['company.com', 'enterprise.org', 'corp.net']
    
    def __init__(self, user_type="personal"):
        super().__init__()
        self.user_type = user_type
        self.setWindowTitle("Login/Register")
        self.resize(500, 350)
        self.setStyleSheet("background-color: #E2F6FD;")
        
        # Initialize database and authentication
        self.db = Database()
        self.auth = Authentication(self.db)
        self.init_ui()
    
    def init_ui(self):
        # Title
        title_prefix = "Welcome to Droid Scanner"
        if self.user_type != "personal":
            title_prefix += f" ({self.user_type.capitalize()} Portal)"
            
        self.title_label = QLabel(title_prefix)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.title_label.setStyleSheet("color: #1E90FF;")

        # Username Input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter Username")
        self.username_input.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px; margin: 5px;"
        )

        # Password Input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px; margin: 5px;"
        )

        # Email Input (initially hidden)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter Email")
        self.email_input.setStyleSheet(
            "background-color: #FFF; padding: 5px; border-radius: 5px; margin: 5px;"
        )
        self.email_input.hide()
        
        # Domain info label (for business users)
        self.domain_info_label = QLabel()
        self.domain_info_label.setWordWrap(True)
        self.domain_info_label.setStyleSheet("color: #666; font-style: italic; margin-left: 10px;")
        self.domain_info_label.hide()
        
        if self.user_type == "business" or self.user_type == "admin":
            domains_text = ", ".join(self.ALLOWED_ORG_DOMAINS)
            self.domain_info_label.setText(f"Required: Email must be from an approved domain: {domains_text}")

        # Buttons
        self.submit_button = QPushButton("Login")
        self.submit_button.clicked.connect(self.validate_user)
        self.submit_button.setStyleSheet(
            "background-color: #FFF; padding: 8px; border-radius: 5px; margin: 5px; font-weight: bold;"
        )

        self.toggle_button = QPushButton("Switch to Register")
        self.toggle_button.clicked.connect(self.toggle_mode)
        self.toggle_button.setStyleSheet(
            "background-color: #FFF; padding: 8px; border-radius: 5px; margin: 5px;"
        )
        
        # Back to portal button
        self.back_button = QPushButton("Back to Portal")
        self.back_button.clicked.connect(self.back_to_portal)
        self.back_button.setStyleSheet(
            "background-color: #FFF; padding: 8px; border-radius: 5px; margin: 5px;"
        )

        # Layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.username_input)
        self.layout.addWidget(self.password_input)
        self.layout.addWidget(self.email_input)
        self.layout.addWidget(self.domain_info_label)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.submit_button)
        button_layout.addWidget(self.toggle_button)
        
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.back_button)
        
        self.setLayout(self.layout)
        
        self.mode = "login"
        self.current_email = None

    def validate_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text() if self.mode == "register" else None

        # Additional validation for business/admin users
        if self.mode == "register" and email and (self.user_type == "business" or self.user_type == "admin"):
            domain_valid = False
            for domain in self.ALLOWED_ORG_DOMAINS:
                if email.endswith(f"@{domain}"):
                    domain_valid = True
                    break
            
            if not domain_valid:
                QMessageBox.warning(
                    self,
                    "Domain Error",
                    f"For {self.user_type} users, you must use an approved organizational email domain."
                )
                return

        result = self.auth.validate_user(username, password, email, self.mode, self)
        
        if result == "verify":
            self.current_email = email
            self.show_verification_dialog(email)
        elif result:
            if self.mode == "login":
                self.open_main_window()

    def show_verification_dialog(self, email):
        while True:  # Use a loop instead of recursion
            dialog = VerificationDialog(email, self)
            if dialog.exec_() != QDialog.Accepted:
                # User cancelled the dialog
                break
                
            verification_code = dialog.get_code()
            verification_result = self.auth.verify_email(email, verification_code)
            
            if verification_result == True:
                QMessageBox.information(
                    self,
                    "Success",
                    "Email verified successfully! You can now login."
                )
                self.toggle_mode()  # Switch back to login
                break  # Exit the loop after successful verification
            elif verification_result == "expired":
                user_response = QMessageBox.warning(
                    self,
                    "Expired Code",
                    "Your verification code has expired. Would you like to try again?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if user_response == QMessageBox.No:
                    break  # Exit the loop if user doesn't want to try again
            else:
                user_response = QMessageBox.warning(
                    self,
                    "Error",
                    "Invalid verification code. Would you like to try again?",
                    QMessageBox.Yes | QMessageBox.No
                )
                if user_response == QMessageBox.No:
                    break  # Exit the loop if user doesn't want to try again

    def resend_verification_code(self, email):
        """Resend verification code to user"""
        try:
            # Generate new OTP and token
            otp = self.auth.generate_otp()
            jwt_token = self.auth.create_jwt(email, otp)
            
            # Update token in database
            self.db.cursor.execute(
                "UPDATE users SET verification_token = ? WHERE email = ?",
                (jwt_token, email)
            )
            self.db.connection.commit()
            
            # Send new email
            self.auth.send_email(email, otp)
        except Exception as e:
            print(f"Error resending verification code: {e}")

    def toggle_mode(self):
        if self.mode == "login":
            self.mode = "register"
            self.submit_button.setText("Register")
            self.toggle_button.setText("Switch to Login")
            self.title_label.setText(f"Register for Droid Scanner ({self.user_type.capitalize()})")
            self.email_input.show()
            if self.user_type == "business" or self.user_type == "admin":
                self.domain_info_label.show()
        else:
            self.mode = "login"
            self.submit_button.setText("Login")
            self.toggle_button.setText("Switch to Register")
            title_prefix = "Welcome to Droid Scanner"
            if self.user_type != "personal":
                title_prefix += f" ({self.user_type.capitalize()} Portal)"
            self.title_label.setText(title_prefix)
            self.email_input.hide()
            self.domain_info_label.hide()

    def open_main_window(self):
        from MainWindow import MainWindow
        self.main_window = MainWindow()
        self.main_window.show()
        self.close()
        
    def back_to_portal(self):
        from PortalWindow import PortalWindow
        self.portal_window = PortalWindow()
        self.portal_window.show()
        self.close()