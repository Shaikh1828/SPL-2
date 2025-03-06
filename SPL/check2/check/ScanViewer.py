def save_credentials(self):
    user_id = self.user_id_input.text().strip()
    password = self.password_input.text()
    
    if not user_id:
        QMessageBox.warning(self, "Input Error", "User ID cannot be empty.")
        return
    
    if len(password) < 8:
        QMessageBox.warning(self, "Input Error", "Password must be at least 8 characters long.")
        return
    
    # If user is logged in and has an ID, use database update
    if self.user_credentials.get("id"):
        success = self.update_user_in_database(
            self.user_credentials["id"],
            user_id,
            password
        )
        if success:
            self.user_credentials["user_id"] = user_id
            self.user_credentials["password"] = password
            self.credentials_updated.emit(self.user_credentials)
            QMessageBox.information(self, "Success", "Credentials updated successfully.")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Username already taken or update failed.")
    else:
        # If not logged in, just update local credentials
        self.user_credentials = {"user_id": user_id, "password": password}
        self.credentials_updated.emit(self.user_credentials)
        QMessageBox.information(self, "Success", "Your credentials have been updated successfully.")
        self.close()

def update_user_in_database(self, user_id, new_username, new_password):
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
        cursor.execute("SELECT id FROM users WHERE user_id = ? AND id != ?", (new_username, user_id))
        if cursor.fetchone():
            conn.close()
            return False  # Username already taken
        
        # Update the user with the new credentials
        cursor.execute(
            "UPDATE users SET user_id = ?, password = ? WHERE id = ?", 
            (new_username, new_password, user_id)
        )
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        
        # Return True if at least one row was affected
        return cursor.rowcount > 0
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False