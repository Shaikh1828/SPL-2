from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout,
    QFrame, QApplication
)
from PyQt5.QtGui import QFont, QColor, QPalette, QBrush, QLinearGradient
from PyQt5.QtCore import Qt, QSize
from AuthWindow import AuthWindows

class PortalWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Droid Scanner Portal")
        self.resize(700, 500)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.init_ui()
        self.drag_pos = None
    
    def init_ui(self):
        # Set gradient background
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 700, 500)
        gradient.setColorAt(0.0, QColor(86, 190, 228))
        gradient.setColorAt(1.0, QColor(10, 90, 170))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)

        # Title Bar
        title_bar = QWidget()
        title_bar.setStyleSheet("background-color: rgb(50, 50, 50); color: white;")
        title_bar_layout = QHBoxLayout()
        title_bar_layout.setContentsMargins(10, 5, 10, 5)
        
        title_label = QLabel("Droid Scanner Portal")
        title_label.setFont(QFont("Arial", 16, QFont.Bold))
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

        # Welcome Message
        welcome_label = QLabel("Welcome to Droid Scanner")
        welcome_label.setFont(QFont("Arial", 24, QFont.Bold))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: white; margin: 20px;")
        
        subtitle_label = QLabel("Select your profile to continue")
        subtitle_label.setFont(QFont("Arial", 14))
        subtitle_label.setAlignment(Qt.AlignCenter)
        subtitle_label.setStyleSheet("color: white; margin-bottom: 30px;")

        # Options Grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        
        # Option Cards
        options = [
            {"title": "Personal Scanner", "desc": "Scan and monitor your personal Android devices", "color": "#6BC8B4"},
            # {"title": "Business Scanner", "desc": "Security solution for corporate devices", "color": "#FF6987"},
            {"title": "Developer Scanner", "desc": "Deep analysis with custom scanning options", "color": "#D4A017"},
            # {"title": "Quick Scan", "desc": "Fast scanning for immediate threats", "color": "#8467D7"}
        ]
        
        self.option_buttons = []
        
        for i, option in enumerate(options):
            row, col = divmod(i, 2)
            
            # Create card frame
            card = QFrame()
            card.setFrameShape(QFrame.StyledPanel)
            card.setStyleSheet(f"""
                QFrame {{
                    background-color: rgba(255, 255, 255, 180);
                    border-radius: 15px;
                    padding: 10px;
                }}
            """)
            
            # Card contents
            card_layout = QVBoxLayout()
            
            # Title
            title = QLabel(option["title"])
            title.setFont(QFont("Arial", 14, QFont.Bold))
            title.setStyleSheet(f"color: {option['color']};")
            
            # Description
            desc = QLabel(option["desc"])
            desc.setWordWrap(True)
            desc.setStyleSheet("color: #333;")
            
            # Button
            btn = QPushButton("Select")
            btn.setFont(QFont("Arial", 11, QFont.Bold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: {option['color']};
                    color: white;
                    border-radius: 8px;
                    padding: 8px;
                    min-height: 30px;
                }}
                QPushButton:hover {{
                    background-color: {option['color']}CC;
                }}
            """)
            btn.clicked.connect(self.open_auth_window)
            self.option_buttons.append(btn)
            
            card_layout.addWidget(title)
            card_layout.addWidget(desc)
            card_layout.addWidget(btn)
            card.setLayout(card_layout)
            
            grid_layout.addWidget(card, row, col)
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(title_bar)
        
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(30, 20, 30, 30)
        content_layout.addWidget(welcome_label)
        content_layout.addWidget(subtitle_label)
        content_layout.addLayout(grid_layout)
        
        main_layout.addLayout(content_layout)
        self.setLayout(main_layout)
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_pos = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(event.globalPos() - self.drag_pos)
            event.accept()
    
    def open_auth_window(self):
        self.auth_window = AuthWindows()
        self.auth_window.show()
        self.close()