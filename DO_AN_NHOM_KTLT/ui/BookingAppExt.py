from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem, QMessageBox
from PyQt6 import uic
import os

from DO_AN_NHOM_KTLT.libs.DataConnector import DataConnector
from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer import Customer
from DO_AN_NHOM_KTLT.models.Customer_Room import Customer_Room
from DO_AN_NHOM_KTLT.models.Room import Room
from DO_AN_NHOM_KTLT.ui.BookingApp import Ui_MainWindow




class BookingAppExt(QMainWindow, Ui_MainWindow):
    def __init__(self,uid=None):
        super().__init__()
        uic.loadUi(os.path.join(os.path.dirname(__file__), "BookingApp.ui"), self)
        self.data_connector = DataConnector()
        self.uid=uid
        self.setupSignalAndSlot()
        self.customers = self.data_connector.get_all_customer()
        self.rooms=self.data_connector.get_all_room()
        self.customer_room=self.data_connector.get_all_customer_room()

    def setupSignalAndSlot(self):
        """Kết nối các nút với các hàm xử lý"""
        self.pushButtonBook.clicked.connect(self.save_booking)
        self.pushButtonNew.clicked.connect(self.clear_form)
        self.pushButtonExit.clicked.connect(self.confirm_exit)

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        self.load_available_rooms()
        self.setupSignalAndSlot()
        self.lineEditSDT.textChanged.connect(self.auto_fill_customer_info)
        self.lineEditCCCD.textChanged.connect(self.auto_fill_customer_info)
        self.dateTimeEdit.dateTimeChanged.connect(self.update)
        self.dateTimeEdit.setDisplayFormat("dd-MM-yyyy HH:mm:ss")
    def showWindow(self):
        self.MainWindow.show()

    def update(self):
        self.dateTimeEdit.dateTime()

    def load_available_rooms(self):
        """ Nạp dữ liệu các phòng có trạng thái 'trống' vào bảng """
        self.tableWidget.setRowCount(0)  # Xóa dữ liệu cũ
        rooms = self.data_connector.get_all_room()
        if not rooms:
            return
        available_rooms = [room for room in rooms if isinstance(room.status, str) and room.status.lower() == "trống"]
        for room in available_rooms:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)

            # Thêm dữ liệu vào từng cột
            self.tableWidget.setItem(row, 0, QTableWidgetItem(str(room.room_id)))
            self.tableWidget.setItem(row, 1, QTableWidgetItem(room.room_type))
            self.tableWidget.setItem(row, 2, QTableWidgetItem(str(room.price_hourly)))
            self.tableWidget.setItem(row, 3, QTableWidgetItem(str(room.price_overnight)))
            self.tableWidget.setItem(row, 4, QTableWidgetItem(room.status))
            self.tableWidget.setItem(row, 5, QTableWidgetItem(room.floor))


    def save_booking(self):
        name = self.lineEditTenKH.text()
        phone = self.lineEditSDT.text()
        cccd = self.lineEditCCCD.text()
        room_id = self.lineEditSTTP.text()
        date_checkin = self.dateTimeEdit.dateTime()
        #Chuyển đổi ngày giờ thành định dạng lưu trữ
        date_format = '%Y-%m-%d %H:%M:%S'
        date_checkin_format = date_checkin.toPyDateTime().strftime(date_format)

        if not ( name and phone and cccd and date_checkin):
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return
        jff = JsonFileFactory()
        self.customers = jff.read_data("../dataset/customers.json", Customer)
        self.rooms = jff.read_data("../dataset/rooms.json", Room)
        self.customer_rooms = jff.read_data("../dataset/customer_room.json", Customer_Room)

        #  Kiểm tra khách hàng có tồn tại không (dựa trên số điện thoại hoặc CCCD)
        customer_found = None
        for customer in self.customers:
            if customer.phone == phone or customer.cccd == cccd:
                customer_found = customer
                break

        if customer_found:
            customer_id = customer_found.customer_id# Lấy mã khách hàng cũ
        else:
            max_id = 0
            for customer in self.customers:
                if customer.customer_id.startswith("M"):
                        num = int(customer.customer_id[1:])  # Lấy số sau "M"
                        max_id = max(max_id, num)
            customer_id = f"M{max_id + 1:02d}"
            new_customer = Customer(customer_id, name, phone, cccd)
            self.customers.append(new_customer)
            jff.write_data(self.customers, "../dataset/customers.json")

        # Tìm phòng theo room_id
        room_found = None
        for room in self.rooms:
            if room.room_id == room_id:
                room_found = room
                break

        if not room_found:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy phòng có mã số này!")
            return

        if room_found.status.lower() == "có":
            QMessageBox.warning(self.MainWindow, "Lỗi", "Phòng đã được đặt trước đó!")
            return
        customer_room = Customer_Room(customer_id, room_id, date_checkin_format)
        self.customer_room.append(customer_room)
        room_found.status = "có"
        jff.write_data(self.rooms, "../dataset/rooms.json")
        self.add_new_booking(customer_id, room_id, date_checkin_format)
        self.update_room_table()

    def add_new_booking(self, customer_id, room_id, date_checkin):
        """Nếu khách đã tồn tại, chỉ thêm phòng mới"""
        jff = JsonFileFactory()
        self.customer_rooms = jff.read_data("../dataset/customer_room.json", Customer_Room)

        # Thêm phòng mới cho khách
        new_customer_room = Customer_Room(customer_id, room_id, date_checkin)
        self.customer_rooms.append(new_customer_room)

        # Ghi dữ liệu mới vào JSON
        jff.write_data(self.customer_rooms, "../dataset/customer_room.json")
        QMessageBox.information(self.MainWindow, "Thông báo", f"Khách {customer_id} đã đặt phòng {room_id} thành công!")

    def auto_fill_customer_info(self):
        """Tự động điền thông tin khách hàng khi nhập số điện thoại hoặc CCCD"""
        phone = self.lineEditSDT.text().strip()
        cccd = self.lineEditCCCD.text().strip()

        if not phone and not cccd:
            return  # Không nhập gì thì không kiểm tra

        jff = JsonFileFactory()
        self.customers = jff.read_data("../dataset/customers.json", Customer)

        # Kiểm tra khách cũ dựa trên số điện thoại hoặc CCCD
        for customer in self.customers:
            if customer.phone == phone or customer.cccd == cccd:
                self.lineEditTenKH.setText(customer.name)
                self.lineEditSDT.setText(customer.phone)
                self.lineEditCCCD.setText(customer.cccd)
                return  # Dừng lại nếu tìm thấy khách hàng

    def update_room_table(self):
        """ Cập nhật danh sách phòng trống trên table """
        self.tableWidget.setRowCount(0)  # Xóa tất cả dữ liệu cũ
        for room in self.rooms:
            if room.status.lower() == "trống":  # Chỉ hiển thị phòng trống
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)
                self.tableWidget.setItem(row_position, 0, QTableWidgetItem(room.room_id))
                self.tableWidget.setItem(row_position, 1, QTableWidgetItem(room.room_type))
                self.tableWidget.setItem(row_position, 2, QTableWidgetItem(str(room.price_hourly)))
                self.tableWidget.setItem(row_position, 3, QTableWidgetItem(str(room.price_overnight)))
                self.tableWidget.setItem(row_position, 4, QTableWidgetItem(room.status))
                self.tableWidget.setItem(row_position, 5, QTableWidgetItem(room.floor))

    def clear_form(self):
        self.lineEditSDT.textChanged.disconnect(self.auto_fill_customer_info)
        self.lineEditCCCD.textChanged.disconnect(self.auto_fill_customer_info)
        """Xóa dữ liệu trên màn hình để nhập mới"""
        self.lineEditTenKH.clear()
        self.lineEditSDT.clear()
        self.lineEditCCCD.clear()
        self.lineEditSTTP.clear()
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTime())
        self.lineEditSDT.textChanged.connect(self.auto_fill_customer_info)
        self.lineEditCCCD.textChanged.connect(self.auto_fill_customer_info)

    def confirm_exit(self):
        """Hiện thông báo xác nhận trước khi thoát"""
        reply = QMessageBox.question(self.MainWindow, "Xác nhận thoát", "Bạn có chắc chắn muốn thoát không?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.No:
            return
        self.MainWindow.close()
        from DO_AN_NHOM_KTLT.ui.MainWindowAdminExt import MainWindowAdminExt
        self.mainwindow = QMainWindow()  
        self.myui = MainWindowAdminExt(self.uid)
        self.myui.setupUi(self.mainwindow)
        self.myui.showWindow()
