from PyQt5.QtWidgets import QMessageBox
import jwt
from datetime import datetime, timedelta
import random
import smtplib
from email.mime.text import MIMEText
from config import EMAIL, EMAIL_PASSWORD, JWT_SECRET_KEY

# Use the secret key from config
SECRET_KEY = JWT_SECRET_KEY

class Authentication:
    def __init__(self, db_connection):
        self.db = db_connection

    def generate_otp(self):
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))

    def send_email(self, recipient, otp):
        """Send OTP via email"""
        try:
            subject = "Your Droid Scanner Verification Code"
            body = f"""
            Hello,
            
            Your verification code for Droid Scanner is: {otp}
            
            This code will expire in 5 minutes.
            
            Thank you,
            Droid Scanner Team
            """
            
            msg = MIMEText(body)
            msg["Subject"] = subject
            msg["From"] = EMAIL
            msg["To"] = recipient

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(EMAIL, EMAIL_PASSWORD)
            server.sendmail(EMAIL, recipient, msg.as_string())
            server.quit()
            print(f"Verification email sent to {recipient}")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

    def create_jwt(self, email, otp):
        """Create JWT token containing OTP with 5-minute expiration"""
        payload = {
            "email": email,
            "otp": otp,
            "exp": datetime.utcnow() + timedelta(minutes=5)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        # In newer versions of PyJWT, encode returns bytes, so convert to string if needed
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return token

    def verify_otp(self, token, input_otp):
        """Verify OTP using JWT token"""
        try:
            # Handle string or bytes token
            if isinstance(token, bytes):
                token = token.decode('utf-8')
                
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            if payload["otp"] == input_otp:
                return True  # OTP is valid
            return False  # OTP is incorrect
        except jwt.ExpiredSignatureError:
            print("OTP has expired")
            return "expired"
        except jwt.InvalidTokenError as e:
            print(f"Invalid token: {e}")
            return "invalid"
        except Exception as e:
            print(f"Verification error: {e}")
            return False

    # In Authentication.py, modify the validate_user method
    def validate_user(self, username, password, email, mode, parent):
        """Handle user login and registration with email verification and user types"""
        if not username or not password:
            QMessageBox.warning(parent, "Input Error", "Username and Password cannot be empty.")
            return False

        try:
            if mode == "login":
                # Check credentials and verification status
                u_id,login_status = self.db.check_login(username, password)
                
                if login_status == True:
                    # Store the user type in the parent for future reference
                    user_type = self.db.get_user_type(username)
                    parent.user_type = user_type
                    
                    QMessageBox.information(parent, "Success", "Login Successful!")
                    return u_id
                elif login_status == "unverified":
                    # Get the email for this unverified user
                    u_id,user_email = self.db.get_user_email(username)
                    if user_email:
                        verification_response = QMessageBox.question(
                            parent, 
                            "Unverified Account", 
                            "Your account is not verified. Would you like to verify it now?",
                            QMessageBox.Yes | QMessageBox.No
                        )
                        
                        if verification_response == QMessageBox.Yes:
                            # Regenerate OTP and send it
                            otp = self.generate_otp()
                            jwt_token = self.create_jwt(user_email, otp)
                            
                            # Update the verification token
                            self.db.update_verification_token(user_email, jwt_token)
                            
                            # Send the email
                            if self.send_email(user_email, otp):
                                parent.current_email = user_email
                                if parent.show_verification_dialog(user_email):
                                    u_id,user_email = self.db.get_user_email(username)
                                    return u_id
                                else:
                                    return 0
                            else:
                                QMessageBox.warning(
                                    parent, 
                                    "Email Error", 
                                    "Failed to send verification email. Please check your email settings."
                                )
                        return False
                    else:
                        QMessageBox.warning(parent, "Error", "Could not retrieve email for verification.")
                        return False
                else:
                    QMessageBox.warning(parent, "Error", "Invalid credentials.")
                    return False
            
            elif mode == "register":
                # Check if email is provided for registration
                if not email:
                    QMessageBox.warning(parent, "Input Error", "Email address is required for registration.")
                    return False
                
                # Validate email format (basic check)
                if "@" not in email or "." not in email:
                    QMessageBox.warning(parent, "Input Error", "Please enter a valid email address.")
                    return False
                
                # Generate OTP and token for email verification
                otp = self.generate_otp()
                jwt_token = self.create_jwt(email, otp)
                
                # Add user to database with user_type
                if self.db.add_user(username, password, email, jwt_token, parent.user_type):
                    # Send verification email
                    if self.send_email(email, otp):
                        QMessageBox.information(
                            parent,
                            "Registration",
                            "Account created! Please verify your email address to activate your account."
                        )
                        parent.current_email = email
                        if parent.show_verification_dialog(email):
                            u_id,user_email = self.db.get_user_email(username)
                            return u_id
                        else:
                            return 0
                    else:
                        QMessageBox.warning(
                            parent,
                            "Email Error",
                            "Failed to send verification email. Please check your email settings."
                        )
                        return False
                else:
                    QMessageBox.warning(
                        parent,
                        "Registration Error",
                        "Username or email already exists. Please choose a different one."
                    )
                    return False

        except Exception as e:
            QMessageBox.critical(parent, "Error", f"An error occurred: {e}")
            return False

    def verify_email(self, email, verification_code):
        """Verify user's email with the provided OTP"""
        try:
            # Get the stored JWT token from database
            jwt_token = self.db.get_verification_token(email)
            
            if not jwt_token:
                print("No verification token found for this email")
                return False
                
            # Verify the OTP
            verification_result = self.verify_otp(jwt_token, verification_code)
            
            if verification_result == True:
                # Update user as verified in database
                self.db.mark_user_verified(email)
                return True
            elif verification_result == "expired":
                return "expired"
            else:
                return False
        except Exception as e:
            print(f"Email verification error: {e}")
            return False