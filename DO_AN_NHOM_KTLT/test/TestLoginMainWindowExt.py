from PyQt6.QtWidgets import QApplication, QMainWindow
from DO_AN_NHOM_KTLT.ui.LoginMainWindowExt import LoginMainWindowExt

app=QApplication([])
mainwindow=QMainWindow()
myui=LoginMainWindowExt()
myui.setupUi(mainwindow)
myui.showWindow()
app.exec()