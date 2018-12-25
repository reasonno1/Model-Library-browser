# from PyQt5 import QtCore as qc
# from PyQt5 import QtGui as qg
from PyQt5 import QtWidgets as qw


class NameListWidgetItem(qw.QListWidgetItem):

    def __init__(self, name, parent, keywords):
        super().__init__(name, parent)
        self.keywords = keywords




