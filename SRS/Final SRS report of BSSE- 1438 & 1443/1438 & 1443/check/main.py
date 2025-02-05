import AuthWindow

from PyQt5.QtWidgets import (
    QApplication
)

app = QApplication([])
auth_window = AuthWindow.AuthWindows()
auth_window.show()
app.exec_()
