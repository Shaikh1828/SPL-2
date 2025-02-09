# Imports
from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout

# App Settings
app = QApplication([])
main_window = QWidget()
main_window.setWindowTitle("Calculator App")
main_window.resize(450,300)
main_window.setStyleSheet("QWidget { background-color:rgb(166, 220, 219)}")

# Create Widgets
text_box = QLineEdit()
grid = QGridLayout()
text_box.setStyleSheet("QLineEdit { background-color:rgb(224, 243, 250); color:rgb(6, 33, 33); font:25pt Arial; padding: 10px;}")

buttons = [
    "7", "8", "9", "/",
    "4", "5", "6", "*",
    "1", "2", "3", "-",
    "0", ".", "=", "+"
]

clear = QPushButton("Clear")
delete = QPushButton("Del")
clear.setStyleSheet("QPushButton { background-color:rgb(107, 142, 141);font:25pt Comic Sans MS; padding: 10px;}")
delete.setStyleSheet("QPushButton { background-color:rgb(107, 142, 141);font:25pt Comic Sans MS; padding: 10px;}")

def button_click():
    button = app.sender()
    text = button.text()

    if text == "=":
        symbol = text_box.text()
        try:
            res = eval(symbol)
            text_box.setText(str(res))
        except Exception as e:
            print("Error:", e)
    elif text == "Clear":
        text_box.clear()
    elif text == "Del":
        current_value = text_box.text()
        text_box.setText(current_value[:-1])
    else:
        current_value = text_box.text()
        text_box.setText(current_value + text)

#Loop for Buttons
row = 0
col = 0
for text in buttons:
    button = QPushButton(text)
    button.clicked.connect(button_click)
    button.setStyleSheet("QPushButton { background-color:rgb(134, 182, 181); font:25pt Comic Sans MS; padding: 10px;}")
    grid.addWidget(button, row, col)
    col += 1
    if col > 3:
        col = 0
        row += 1

#Design
master_layout = QVBoxLayout()
master_layout.addWidget(text_box)
master_layout.addLayout(grid)

button_row = QHBoxLayout()
button_row.addWidget(clear)
button_row.addWidget(delete)

master_layout.addLayout(button_row)
master_layout.setContentsMargins(25,25,25,25)
main_window.setLayout(master_layout)

clear.clicked.connect(button_click)
delete.clicked.connect(button_click)

#Run
# main_window.setStyleSheet("QWidget { background-color:rgb(166, 220, 219)}")
main_window.show()
app.exec_()