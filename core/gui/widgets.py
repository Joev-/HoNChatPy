from PySide import QtCore, QtGui

class CustomLoginWindow(QtGui.QWidget):
    def __init__(self, parent=None):
        super(CustomLoginWindow, self).__init__()
        self.setFixedSize(292, 357)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_NoSystemBackground)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.moving = False
        self.bg = QtGui.QPixmap("core/gui/resources/img/login-frame.png")
        self.setStyleSheet(open('core/gui/resources/style/login.qss', 'r').read())

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.drawPixmap(0, 0, self.bg)

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton and self.moving:
            self.move(event.globalPos() - self.offset)
        event.accept()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.moving = True; self.offset = event.globalPos() - self.frameGeometry().topLeft()
        event.accept()

    def mouseReleaseEvent(self, event):
        self.moving = False
        event.accept()

    def mouseDoubleClickEvent(self, event):
        event.accept()

class URLLabel(QtGui.QLabel):
    def __init__(self, parent, url, text=None, underline=False):
        super(URLLabel, self).__init__(parent)
        self.parent = parent
        self.url = url
        self.text = text if text is not None else url
        self.underline = underline
        self.setCursor(QtCore.Qt.PointingHandCursor)
        self.setText(self.text)
       
        self.base_font = QtGui.QFont("Sans Serif")
        self.base_font.setPixelSize(11)
        self.setFont(self.base_font)

    def __set_underline(self, on):
        font = self.base_font
        font.setUnderline(on)
        self.setFont(font)
    
    def enterEvent(self, event):
        if self.underline:
            self.__set_underline(True)

    def leaveEvent(self, event):
        if self.underline:
            self.__set_underline(False)
    
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            QtGui.QDesktopServices.openUrl(self.url)
