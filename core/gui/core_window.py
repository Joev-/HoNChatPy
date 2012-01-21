from PySide import QtCore, QtGui
import sys

class PanelUserInfo(QtGui.QWidget):
    def __init__(self, parent=None):
        super(PanelUserInfo, self).__init__(parent)
        self.parent = parent
        
        self.setup_user_menu()
        self.setup_ui()
    
    def setup_ui(self):
        self.user_options = QtGui.QPushButton(self)
        # self.user_options.setText(self.parent.client.logged_in_user)
        self.user_options.setText("Username")
        self.user_options.setMenu(self.user_options_menu)
        
    def setup_user_menu(self):
        # Logout action

        self.user_options_menu = QtGui.QMenu(self)
        a_logout = self.user_options_menu.addAction("Logout")
        a_close = self.user_options_menu.addAction("Close")

        a_logout.triggered.connect(self.logout_clicked)
        a_close.triggered.connect(self.close_clicked)

    def logout_clicked(self):
        print "logout clicked"
        #if self.parent.client.disconnect() is True and self.parent.client.logout() is True:
            #self.close()

    def close_clicked(self):
        print "close clicked"
        #self.parent.client.disconnect()
        #self.parent.client.logout()
        #sys.exit()


class HCPCoreWindow(QtGui.QWidget):
    def __init__(self, client):
        super(HCPCoreWindow, self).__init__()
        self.client = client
       
        self.setup_ui()
        #self.show.connect(self.on_show)

    def setup_ui(self):
        self.setWindowTitle("HoNChatPy")
        self.user_panel = PanelUserInfo(self)
         
        # ------ TEMPORARY ---
        #b_logout = QtGui.QPushButton(self)
        #b_logout.setText("log out")
        #b_logout.clicked.connect(self.logout_clicked)

        #b_close = QtGui.QPushButton(self)
        #b_close.setText("Close")
        #b_close.clicked.connect(self.close_clicked)
        # ---------------------

        layout = QtGui.QGridLayout(self)
        layout.addWidget(self.user_panel)
        #layout.addWidget(b_logout)
        #layout.addWidget(b_close)
        self.setLayout(layout)
            
    @QtCore.Slot()
    def initial_run(self):
        # This method results in the window not being shown until the following code has run. 
        print "initial run!"
        self.client.connect() 

    def on_show(self):
        print "Show signal triggered"

class FakeClient(object):
    def connect(self):
        pass
    def logout(self):
        pass
    def disconnect(self):
        pass
    @property
    def logged_in_user(self):
        return "Joev"
    
if __name__ == '__main__':
    client = FakeClient()

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("HoNChatPy")
    #app.setQuitOnLastWindowClosed(True) # May need to change for system tray behaviour
    
    core_window = HCPCoreWindow(client)
    core_window.setObjectName('hcp_window')
    core_window.show()
    app.exec_()

