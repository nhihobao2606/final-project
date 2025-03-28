from PyQt6.QtWidgets import QMessageBox, QMainWindow


from DO_AN_NHOM_KTLT.libs.DataConnector import DataConnector
from DO_AN_NHOM_KTLT.ui.LoginMainWindow import Ui_MainWindow


class LoginMainWindowExt(Ui_MainWindow):
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonLogin.clicked.connect(self.process_login)
        self.pushButtonExit.clicked.connect(self.exit_login)
    def process_login(self):
        dc=DataConnector()
        uid = self.lineEditUsername.text()
        pwd = self.lineEditPassword.text()
        user = dc.login(uid, pwd)
        if user != None:
            self.uid = uid
            dlg = QMessageBox(self.MainWindow)
            dlg.setWindowTitle("Xác nhận quyền truy cập")
            dlg.setText(f"Bạn đang truy cập với vai trò {user.role}")
            dlg.setIcon(QMessageBox.Icon.Question)
            buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            dlg.setStandardButtons(buttons)
            button = dlg.exec()
            if button == QMessageBox.StandardButton.No:
                return
            self.MainWindow.close()
            from DO_AN_NHOM_KTLT.ui.MainWindowAdminExt import MainWindowAdminExt
            self.mainwindow = QMainWindow()
            self.myui = MainWindowAdminExt(self.uid)
            self.myui.setupUi(self.mainwindow)
            if user.role=="Admin":
                self.myui.removeReceptionistFunctions()
            self.myui.showWindow()
        else:
            self.mgs = QMessageBox(self.MainWindow)
            self.mgs.setWindowTitle("Thông báo")
            self.mgs.setText("Đăng nhập thất bại")
            self.mgs.exec()
    def exit_login(self):
        msg = QMessageBox(self.MainWindow)
        msg.setWindowTitle("Xác nhận thoát")
        msg.setText("Bạn muốn thoát ư?")
        msg.setIcon(QMessageBox.Icon.Question)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msg.setStandardButtons(buttons)
        button = msg.exec()
        if button == QMessageBox.StandardButton.No:
            return
        self.MainWindow.close()
        msg.setStyleSheet(self.MainWindow().styleSheet())


