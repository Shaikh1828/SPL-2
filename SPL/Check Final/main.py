import sqlite3
from PyQt5.QtWidgets import QApplication
from PortalWindow import PortalWindow

# Run Application
app = QApplication([])
portal_window = PortalWindow()
portal_window.show()

app.exec_()
