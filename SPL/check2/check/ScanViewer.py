import sys
import sqlite3
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, 
                            QComboBox, QFrame, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


class PermissionsFeatureDropdown(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.load_features()
        
    def init_ui(self):
        # Set up the window
        self.setWindowTitle('Permissions Features')
        self.setGeometry(300, 300, 400, 200)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Feature selection label
        label = QLabel('Select Feature:')
        layout.addWidget(label)
        
        # Create dropdown (combo box)
        self.feature_combo = QComboBox()
        self.feature_combo.setMinimumWidth(350)
        self.feature_combo.addItem('-- Select a feature --')  # Default placeholder
        self.feature_combo.currentIndexChanged.connect(self.on_feature_selected)
        layout.addWidget(self.feature_combo)
        
        # Add separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        # Display selected feature
        self.selected_label = QLabel('No feature selected')
        layout.addWidget(self.selected_label)
        
        # Add some spacing
        layout.addSpacing(20)
        
        # Refresh button
        refresh_btn = QPushButton('Refresh Features')
        refresh_btn.clicked.connect(self.load_features)
        layout.addWidget(refresh_btn)
        
        # Set the layout
        self.setLayout(layout)
        
    def load_features(self):
        """Load feature names from the database"""
        try:
            # Save current selection if any
            current_selection = self.feature_combo.currentText()
            if current_selection == '-- Select a feature --':
                current_selection = None
                
            # Clear the combo box but keep the placeholder
            self.feature_combo.clear()
            self.feature_combo.addItem('-- Select a feature --')
            
            # Connect to SQLite database
            conn = sqlite3.connect('app_data.db')
            cursor = conn.cursor()
            
            # Query to get distinct feature names
            cursor.execute('SELECT DISTINCT feature_name FROM Permissions_Intents ORDER BY feature_name')
            features = cursor.fetchall()
            
            # Add features to the combo box
            for feature in features:
                self.feature_combo.addItem(feature[0])
                
            # Restore previous selection if it exists
            if current_selection and current_selection != '-- Select a feature --':
                index = self.feature_combo.findText(current_selection)
                if index >= 0:
                    self.feature_combo.setCurrentIndex(index)
            
            # Close connection
            conn.close()
            
        except sqlite3.Error as e:
            QMessageBox.critical(self, 'Database Error', 
                                f'Failed to load features from database: {str(e)}')
    
    def on_feature_selected(self):
        """Handle the feature selection change"""
        selected = self.feature_combo.currentText()
        if selected != '-- Select a feature --':
            self.selected_label.setText(f'Selected feature: {selected}')
        else:
            self.selected_label.setText('No feature selected')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PermissionsFeatureDropdown()
    window.show()
    sys.exit(app.exec_())