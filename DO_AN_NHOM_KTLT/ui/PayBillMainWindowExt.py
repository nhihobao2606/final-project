import datetime

from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QMessageBox, QMainWindow

from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer_Room import Customer_Room
from DO_AN_NHOM_KTLT.models.Room import Room
from DO_AN_NHOM_KTLT.models.Bill import Bill
from DO_AN_NHOM_KTLT.ui.PayBillMainWindow import Ui_MainWindow


class PayBillMainWindowExt(Ui_MainWindow):
    def __init__(self, customer, room, customer_room, uid=None):
        self.bills=[]
        self.customer = customer  # Lưu dữ liệu khách hàng
        self.room = room  # Lưu dữ liệu phòng
        self.customer_room = customer_room
        self.uid=uid
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        if self.customer and self.room and self.customer_room:
            self.show_detail_customer(self.customer,self.room)
        current_datetime = QDateTime.currentDateTime()
        self.dateTimeEditcheckout.setDateTime(current_datetime)
        self.dateTimeEditcheckout.setDisplayFormat("dd-MM-yyyy HH:mm:ss")
        self.create_bill()
        self.update_total_price()
        self.load_next_bill_id()
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()
    def setupSignalAndSlot(self):
        self.pushButtonxacnhan.clicked.connect(self.confirm_payment)
        self.pushButtonthoat.clicked.connect(self.confirm_exit)
    def show_detail_customer(self,customer,room):
        self.lineEditcustomerId.setText(customer.customer_id)
        self.lineEditname.setText(customer.name)
        self.lineEditroomId.setText(room.room_id)
        self.lineEditroom_type.setText(room.room_type)

        checkin_value = self.customer_room.date_checkin

            # Kiểm tra nếu checkin là datetime, chuyển thành chuỗi
        if isinstance(checkin_value, datetime.datetime):
            checkin_qdatetime = QDateTime(
                checkin_value.year, checkin_value.month, checkin_value.day,
                checkin_value.hour, checkin_value.minute, checkin_value.second
            )
        else:
            checkin_qdatetime = QDateTime.fromString(checkin_value, "dd-MM-yyyy HH:mm:ss")

        self.dateTimeEditcheckin.setDateTime(checkin_qdatetime)
        self.dateTimeEditcheckin.setDisplayFormat("dd-MM-yyyy HH:mm:ss")

    def create_bill(self):
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        bill_type = Bill.determine_price_type(self.customer_room.date_checkin,current_datetime)
        rent_price = self.room.price_hourly if bill_type == "hourly" else self.room.price_overnight
        """Tạo hóa đơn và tính tổng tiền"""
        self.bill = Bill(
            bill_id=self.lineEditbillId.text(),
            customer_id=self.customer.customer_id,
            customer_name=self.customer.name,
            room_id=self.customer_room.room_id,
            room_type=self.room.room_type,
            stay_duration=self.lineEdittime.text(),
            date_checkin=self.customer_room.date_checkin,
            date_checkout=current_datetime,
            rent_price=rent_price,
            price=self.lineEditprice.text() ,
            extra_fee=self.lineEditphuthu.text(),
            total_price=self.lineEdittongtien.text(),
            payment_method=self.cbphuongthuc.currentText()
        )
        self.bill.calculate_total_price(self.room)

    def update_total_price(self):
        stay_duration = self.bill.calculate_stay_duration()
        determine=self.bill.determine_price_type(self.bill.date_checkin,self.bill.date_checkout)
        self.lineEdittime.setText(stay_duration)
        """Cập nhật giao diện với giá phòng, phụ thu và tổng tiền"""
        self.lineEditprice.setText(str(self.bill.price))
        self.lineEditphuthu.setText(str(self.bill.extra_fee))
        self.lineEdittongtien.setText(str(self.bill.total_price))
        if determine=="hourly":
            self.lineEditrent_price.setText(str(self.room.price_hourly))
        else:
            self.lineEditrent_price.setText(str(self.room.price_overnight))

    def confirm_payment(self):
        # Lấy thông tin từ giao diện
        customer_id = self.lineEditcustomerId.text()
        customer_name = self.lineEditname.text()  # ID khách hàng
        room_id = self.lineEditroomId.text()# ID phòng
        room_type=self.lineEditroom_type.text()
        stay_duration=self.lineEdittime.text()
        rent_price=self.lineEditrent_price.text()
        price=self.lineEditprice.text()
        extra_fee = self.lineEditphuthu.text()
        payment_method = self.cbphuongthuc.currentText()
        total_price = str(self.lineEdittongtien.text())  # Tổng tiền
        checkin_time = self.dateTimeEditcheckin.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")
        checkout_time = self.dateTimeEditcheckout.dateTime().toPyDateTime().strftime("%Y-%m-%d %H:%M:%S")

        # Tạo mã hóa đơn tự động
        last_bill_id = self.get_last_bill_id()
        new_bill_id = self.generate_next_bill_id(last_bill_id)
        self.bill.bill_id=new_bill_id

        new_bill = Bill(
            bill_id=new_bill_id,
            customer_id=customer_id,
            customer_name=customer_name,
            room_id=room_id,
            room_type=room_type,
            stay_duration=stay_duration,
            rent_price=rent_price,
            price=price,
            extra_fee=extra_fee,
            payment_method=payment_method,
            total_price=total_price,
            date_checkin=checkin_time,
            date_checkout=checkout_time
        )

        # Lưu hóa đơn xuống file JSON
        jff = JsonFileFactory()
        bills = jff.read_data("../dataset/bills.json", Bill)

        if not isinstance(bills, list):  # Đảm bảo bills là list
            bills = []
        bills.append(new_bill)
        filename = "../dataset/bills.json"
        jff.write_data(bills, filename)

        # Cập nhật trạng thái phòng thành "Trống"
        self.update_room_status(room_id)
        self.remove_customer_room(customer_id, room_id)
        QMessageBox.information(self.MainWindow, "Thông báo", f"Hóa đơn {new_bill_id} đã được lưu thành công!")
        self.bill.calculate_total_price(self.room)

    def get_last_bill_id(self):
        jff = JsonFileFactory()
        bills = jff.read_data("../dataset/bills.json", Bill)
        if not bills:
            return None
        return bills[-1].bill_id  # Lấy mã hóa đơn cuối cùng

    def generate_next_bill_id(self, last_bill_id):
        if not last_bill_id:
            return "HD001"
        last_number = int(last_bill_id[2:])  # Lấy số từ HDxxx
        return f"HD{last_number + 1:03d}"  # Tạo mã tiếp theo

    def load_next_bill_id(self):
        last_bill_id = self.get_last_bill_id()
        new_bill_id = self.generate_next_bill_id(last_bill_id)
        self.lineEditbillId.setText(new_bill_id)

    def update_room_status(self, room_id):
        # Cập nhật trạng thái phòng trong file JSON
        jff = JsonFileFactory()
        rooms = jff.read_data("../dataset/rooms.json", Room)
        for room in rooms:
            if room.room_id == room_id:
                room.status = "trống"
                break
        filename = "../dataset/rooms.json"
        jff.write_data(rooms, filename)

    def remove_customer_room(self, customer_id, room_id):
        """Xóa thông tin đặt phòng khỏi customer_room.json sau khi thanh toán"""
        jff = JsonFileFactory()
        filename_customer_room = "../dataset/customer_room.json"

        customer_room=jff.read_data(filename_customer_room, Customer_Room)

        # Xóa phòng đã thanh toán, nhưng giữ khách hàng
        customer_room = [cr for cr in customer_room if not (cr.customer_id == customer_id and cr.room_id == room_id)]

        # Ghi lại danh sách mới vào JSON
        jff.write_data(customer_room, filename_customer_room)

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















