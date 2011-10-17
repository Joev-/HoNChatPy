from PySide import QtCore, QtGui

class HCPCoreWindow(QtGui.QMainWindow):
    def __init__(self, client):
        super(HCPCoreWindow, self).__init__()
        self.client = client
