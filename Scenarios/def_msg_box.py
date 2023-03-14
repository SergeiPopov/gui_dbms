from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *


class DefMsgBox(QMessageBox):
    def __init__(self, title, text):
        super(DefMsgBox, self).__init__()

        self.setIcon(QMessageBox.Information)
        self.setText(title)
        self.setWindowTitle(text)
        self.setStandardButtons(QMessageBox.Ok)

        self.exec()

