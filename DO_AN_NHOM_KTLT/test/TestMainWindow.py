from PyQt6.QtWidgets import QApplication, QMainWindow

from DO_AN_NHOM_KTLT.ui.MainWindowAdminExt import MainWindowAdminExt

app=QApplication([])
mainwindow=QMainWindow()
myui=MainWindowAdminExt()
myui.setupUi(mainwindow)
myui.showWindow()
app.exec()