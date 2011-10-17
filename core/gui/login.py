from PySide import QtCore, QtGui
from widgets import CustomLoginWindow, URLLabel
from hashlib import md5 
import sys, time

class HCPLoginWindow(CustomLoginWindow):
    def __init__(self, client):
        super(HCPLoginWindow, self).__init__()
        
        self.client = client
        self.username = None
        self.password = None
        self.remember_me = False
        self.invisible = False
        
        self.setup_ui()
        self.load_settings()

    def load_settings(self):
        settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "HoNChatPy")
        # Nice and hackish way to center the window on first run!
        self.move(settings.value("loginwindow/pos", QtCore.QPoint(QtGui.QApplication.desktop().geometry().center() - self.geometry().center())))
        self.remember_me = settings.value("user/remember", False)
        if self.remember_me is True:
            self.u_input.setText(settings.value("user/username"))
            self.p_input.setText(settings.value("user/password"))
            self.chk_invisible.setChecked(True if settings.value("user/invisible") == "true" else False)
            self.chk_remember.setChecked(True if settings.value("user/remember") == "true" else False)

    def save_settings(self):
        # Ensure the password is hashed
        if self.password is not None and len(self.password) != 32:
            self.password = md5(self.password).hexdigest()

        settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope, "HoNChatPy")
        settings.setValue("loginwindow/pos", self.window().pos())
        if self.remember_me is True:
            settings.setValue("user/remember", self.remember_me)
            settings.setValue("user/username", self.username)
            settings.setValue("user/password", self.password)
            settings.setValue("user/invisible", self.invisible)
        else:
            settings.setValue("user/remember", False)
            settings.remove("user/username")
            settings.remove("user/password")
            settings.remove("user/invisible")
        
    def setup_ui(self):
        self.setWindowTitle("HoNChatPy")

        # Precisely positioned close button.
        b_close = QtGui.QPushButton(self)
        b_close.setObjectName('close')
        b_close.setFixedSize(19, 19)
        b_close.move(self.width() - 30, 10)
        b_close.clicked.connect(self.__on_close_clicked)
        b_close.setMouseTracking(False)

        # HoNChatPy Logo
        hcp_logo = QtGui.QLabel(self)
        hcp_logo.setObjectName('logo')
        hcp_logo.setPixmap(QtGui.QPixmap('core/gui/resources/img/hcp_logo.png'))
        hcp_logo.setAlignment(QtCore.Qt.AlignCenter)

        # Login 'form'
        # A label to hold login error messages.
        error_msg = QtGui.QLabel(self)
        error_msg.setObjectName('error_msg')
        #error_msg.setSizePolicy(QtGui.QSizePolicy.Ignore, QtGui.QSizePolicy.Ignore)
        self.error_msg = error_msg

        # Username
        u_label = QtGui.QLabel(self)
        u_label.setObjectName('username')
        u_label.setText('Username')
        u_label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        u_input = QtGui.QLineEdit(self)
        u_input.textChanged.connect(self.__on_username_update)
        u_label.setBuddy(u_input)
        u_input.maxLength = 40
        self.u_input = u_input

        # Password
        p_label = QtGui.QLabel(self)
        p_label.setObjectName('password')
        p_label.setText('Password')
        p_label.setSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        p_input = QtGui.QLineEdit(self)
        p_input.textChanged.connect(self.__on_password_update)
        p_input.setEchoMode(QtGui.QLineEdit.Password)
        p_label.setBuddy(p_input)
        self.p_input = p_input
        
        # Forgotten password url
        f_label = QtGui.QLabel(self)
        f_label = URLLabel(self, 'http://heroesofnewerth.com/cs.php', 'Forgot your password?', underline=False)
        f_label.setObjectName('forgot_pw')

        # Remember password check box
        self.chk_remember = QtGui.QCheckBox('Remember me', self)
        self.chk_remember.setObjectName('remember_me')
        self.chk_remember.toggled.connect(self.__on_remember_update)

        # Invisible mode check box
        invisible = QtGui.QCheckBox('Invisible', self)
        invisible.setObjectName('invisible')
        invisible.toggled.connect(self.__on_invisible_update)
        self.chk_invisible = invisible

        # Login button
        l_button = QtGui.QPushButton("Login", self)
        l_button.setObjectName('login')
        l_button.setCursor(QtCore.Qt.PointingHandCursor)
        l_button.clicked.connect(self.__login)
        l_button.setEnabled(False)
        self.l_button = l_button
        
        # Add all of the elements to the layout and show it.
        layout = QtGui.QGridLayout(self)
        layout.setContentsMargins(21, 0, 21, 0)
        layout.addWidget(hcp_logo, 0, 0, 1, 2, QtCore.Qt.AlignHCenter)
        layout.setRowMinimumHeight(0, 70)
        layout.addWidget(error_msg, 1, 0, 1, 2, QtCore.Qt.AlignCenter)
        layout.setRowMinimumHeight(1, 30)
        layout.addWidget(u_label, 2, 0, 1, 2, QtCore.Qt.AlignTop)
        layout.addWidget(u_input, 3, 0, 1, 2, QtCore.Qt.AlignTop)
        layout.addWidget(p_label, 4, 0, 1, 2, QtCore.Qt.AlignTop)
        layout.addWidget(p_input, 5, 0, 1, 2, QtCore.Qt.AlignTop)
        layout.addWidget(f_label, 6, 0, 1, 1, QtCore.Qt.AlignTop)
        layout.addWidget(self.chk_remember, 7, 0, 1, 2, QtCore.Qt.AlignVCenter)
        layout.addWidget(self.chk_invisible, 8, 0, 1, 2, QtCore.Qt.AlignVCenter)
        layout.addWidget(self.l_button, 7, 1, 2, 1, QtCore.Qt.AlignRight)
        layout.setRowMinimumHeight(3, 36)
        layout.setRowMinimumHeight(6, 25)
        layout.setRowStretch(9, 100)

        self.setLayout(layout)
        
        # Tab order.
        # Username field > Password field > Remember me box > Log in button
        # u_input > p_input > remember > l_button
        self.setTabOrder(u_input, p_input)
        self.setTabOrder(p_input, self.chk_remember)
        self.setTabOrder(self.chk_remember, self.chk_invisible)
        self.setTabOrder(self.chk_invisible, self.l_button)

        # Focus policies
        u_input.setFocus()
        b_close.setFocusPolicy(QtCore.Qt.NoFocus)
        f_label.setFocusPolicy(QtCore.Qt.ClickFocus)

    def keyPressEvent(self, event):
        # From QDialog source code.
        # Captures the enter key to make the login form a bit more standard.
        if not event.modifiers() or event.modifiers() & QtCore.Qt.KeypadModifier and event.key() == QtCore.Qt.Key_Enter:
            if self.l_button.isEnabled():
                self.l_button.click()
                event.accept()
        event.ignore()
    
    def __on_close_clicked(self):
       sys.exit(self.save_settings())

    def __on_username_update(self, username):
        if username == "": username = None
        self.username = username
        self.__update_login_button()

    def __on_password_update(self, password):
        if password == "": password = None
        self.password = password
        self.__update_login_button()
    
    def __on_remember_update(self, remember):
        self.remember_me = remember

    def __on_invisible_update(self, invisible):
        self.invisible = invisible
    
    def __update_login_button(self):
        if self.username != None and self.password != None:
            self.l_button.setEnabled(True)
        elif self.username == None or self.password == None:
            self.l_button.setEnabled(False)

    def __login(self):
        if self.username is None or self.password is None:
            self.l_button.setEnabled(False)
            return 

        # Save the settings before logging in.
        self.save_settings()
        
        # Clear any previous states, disable the button to prevent 'spammy' logins
        # and set the text to something nice.
        self.error_msg.setText(None)
        self.l_button.setEnabled(False)
        self.l_button.setText("Validating..")
        if self.client.login(self.username, self.password):
            self.close()
        else:
            self.error_msg.setText("Incorrect username or password")
            self.l_button.setEnabled(True)
            self.l_button.setText("Login")

    def __load_settings(self):
        pass

