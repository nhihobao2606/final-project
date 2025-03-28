
import os
import webbrowser
from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox, QMainWindow

from DO_AN_NHOM_KTLT.libs.DataConnector import DataConnector
from DO_AN_NHOM_KTLT.libs.ExportTool import ExportTool
from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer import Customer
from DO_AN_NHOM_KTLT.models.Room import Room
from DO_AN_NHOM_KTLT.models.Customer_Room import Customer_Room
from DO_AN_NHOM_KTLT.ui.LoginMainWindowExt import LoginMainWindowExt
from DO_AN_NHOM_KTLT.ui.PayBillMainWindowExt import PayBillMainWindowExt
from DO_AN_NHOM_KTLT.ui.BookingAppExt import BookingAppExt
from DO_AN_NHOM_KTLT.ui.MainWindowAdmin import Ui_MainWindow


class MainWindowAdminExt(Ui_MainWindow):
    def __init__(self,uid=None):
        self.dc=DataConnector()
        self.uid = uid
        self.is_import_from_excel = False  # Chỉ đánh dấu nếu dữ liệu lấy từ Excel
        self.customers=self.dc.get_all_customer()
        self.rooms=self.dc.get_all_room()
        self.customer_rooms = self.dc.get_all_customer_room()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow=MainWindow
        if self.uid:
            self.MainWindow.setWindowTitle(f"Xin chào {self.uid}!")
        self.show_customers_gui()
        self.show_rooms_gui()
        self.setupSignalAndSlot()
    def showWindow(self):
        self.MainWindow.show()

    def show_customers_gui(self):
        self.tableWidgetCustomer.setRowCount(0)
        if self.is_import_from_excel:  # Nếu dữ liệu lấy từ Excel
            customers = self.customers
            customer_rooms = self.customer_rooms
        else:  # Nếu dữ liệu lấy từ JSON
            jff = JsonFileFactory()
            customers = jff.read_data("../dataset/customers.json", Customer)
            customer_rooms = jff.read_data("../dataset/customer_room.json", Customer_Room)

        customer_dict = {customer.customer_id: customer for customer in customers}
        for cr in customer_rooms:
            if cr.customer_id in customer_dict:
                customer = customer_dict[cr.customer_id]
                row = self.tableWidgetCustomer.rowCount()
                self.tableWidgetCustomer.insertRow(row)
                date_checkin = cr.date_checkin.strftime("%d-%m-%Y %H:%M:%S") if cr.date_checkin else "Chưa nhận phòng"

                col_customer_id = QTableWidgetItem(str(customer.customer_id))
                col_name = QTableWidgetItem(customer.name)
                col_phone = QTableWidgetItem(customer.phone)
                col_cccd = QTableWidgetItem(customer.cccd)
                col_room_id = QTableWidgetItem(cr.room_id)
                col_checkin_date = QTableWidgetItem(date_checkin)

                self.tableWidgetCustomer.setItem(row, 0, col_customer_id)
                self.tableWidgetCustomer.setItem(row, 1, col_name)
                self.tableWidgetCustomer.setItem(row, 2, col_phone)
                self.tableWidgetCustomer.setItem(row, 3, col_cccd)
                self.tableWidgetCustomer.setItem(row, 4, col_room_id)
                self.tableWidgetCustomer.setItem(row, 5, col_checkin_date)

    def show_rooms_gui(self):
        # Xóa dữ liệu cũ trong bảng phòng
        self.tableWidgetRoom.setRowCount(0)
        # Đọc dữ liệu từ JSON
        jff = JsonFileFactory()
        customers = jff.read_data("../dataset/customers.json", Customer)
        customer_rooms = jff.read_data("../dataset/customer_room.json", Customer_Room)

        # Nạp dữ liệu từ danh sách phòng
        for room in self.rooms:
            row = self.tableWidgetRoom.rowCount()
            self.tableWidgetRoom.insertRow(row)
            # Tìm thông tin đặt phòng của khách hàng
            customer_room = next((cr for cr in customer_rooms if cr.room_id == room.room_id), None)

            col_room_id = QTableWidgetItem(room.room_id)
            col_room_type = QTableWidgetItem(room.room_type)
            col_price_hourly = QTableWidgetItem(str(room.price_hourly))
            col_price_overnight = QTableWidgetItem(str(room.price_overnight))
            col_status = QTableWidgetItem(room.status)
            col_floor = QTableWidgetItem(room.floor)

            # Đặt dữ liệu vào bảng
            self.tableWidgetRoom.setItem(row, 0, col_room_id)
            self.tableWidgetRoom.setItem(row, 1, col_room_type)
            self.tableWidgetRoom.setItem(row, 2, col_price_hourly)
            self.tableWidgetRoom.setItem(row, 3, col_price_overnight)
            self.tableWidgetRoom.setItem(row, 4, col_status)
            self.tableWidgetRoom.setItem(row, 5, col_floor)
    def setupSignalAndSlot(self):
        self.tableWidgetCustomer.itemSelectionChanged.connect(self.load_customer_and_room_info)
        self.tableWidgetRoom.itemSelectionChanged.connect(self.load_room_info)
        self.pushButtonDatPhong.clicked.connect(self.process_BookingApp)
        self.pushButtonHoaDon.clicked.connect(self.open_pay_bill)
        self.lineEditSeachRoom.textChanged.connect(self.search_room)
        self.lineEditSeachCustomer.textChanged.connect(self.search_customer)
        self.pushButtonXoa.clicked.connect(self.delete_customer_room)
        self.pushButtonSua.clicked.connect(self.edit_customer)
        self.pushButtonLogout.clicked.connect(self.logout)
        self.actionExit.triggered.connect(self.exit_program)
        self.actionExcel_Export.triggered.connect(self.export_to_excel)
        self.actionExcel_Import.triggered.connect(self.import_from_excel)
        self.actionHelp.triggered.connect(self.open_help)

    # Hiển thị thông tin phòng khi bấm vào bảng
    def load_room_info(self):
        current_row = self.tableWidgetRoom.currentRow()
        if current_row >= 0:
            # Xóa sạch thông tin khách hàng trước khi điền thông tin phòng
            self.lineEditCustomerID.clear()
            self.lineEditName.clear()
            self.lineEditPhone.clear()
            self.lineEditCCCD.clear()
            self.lineEditDateCheckin.clear()

            # Lấy dữ liệu từ bảng
            room_id = self.tableWidgetRoom.item(current_row, 0).text()
            type_room = self.tableWidgetRoom.item(current_row, 1).text()
            status = self.tableWidgetRoom.item(current_row, 4).text()
            floor = self.tableWidgetRoom.item(current_row, 5).text()

            # Điền thông tin vào groupbox
            self.lineEditRoomID.setText(room_id)
            self.lineEditTypeRoom.setText(type_room)
            self.lineEditStatus.setText(status)
            self.lineEditFloor.setText(floor)

            # Nếu phòng có trạng thái "Có", tìm thông tin khách hàng
            if status.lower() == "có":
                customer_room = next((cr for cr in self.customer_rooms if cr.room_id == room_id), None)
                if customer_room:
                    customer = next((c for c in self.customers if c.customer_id == customer_room.customer_id), None)
                    if customer:
                        # Hiển thị thông tin khách hàng lên giao diện
                        self.lineEditCustomerID.setText(customer.customer_id)
                        self.lineEditName.setText(customer.name)
                        self.lineEditPhone.setText(customer.phone)
                        self.lineEditCCCD.setText(customer.cccd)
                        # Chuyển đổi ngày check-in từ chuỗi sang datetime
                        if isinstance(customer_room.date_checkin, str):
                            checkin_date = datetime.strptime(customer_room.date_checkin, "%Y-%m-%d %H:%M:%S")
                        else:
                            checkin_date = customer_room.date_checkin  # Nếu đã là datetime thì giữ nguyên
                        self.lineEditDateCheckin.setText(checkin_date.strftime("%d-%m-%Y %H:%M:%S"))

    def load_customer_and_room_info(self):
        # Lấy dòng hiện tại trong bảng khách hàng
        current_row = self.tableWidgetCustomer.currentRow()
        if current_row >= 0:
            # Lấy thông tin khách hàng từ bảng thay vì danh sách gốc
            customer_id = self.tableWidgetCustomer.item(current_row, 0).text()
            name = self.tableWidgetCustomer.item(current_row, 1).text()
            phone = self.tableWidgetCustomer.item(current_row, 2).text()
            cccd = self.tableWidgetCustomer.item(current_row, 3).text()
            room_id = self.tableWidgetCustomer.item(current_row, 4).text()
            checkin_date = self.tableWidgetCustomer.item(current_row, 5).text()

            # Điền thông tin khách hàng vào groupbox
            self.lineEditCustomerID.setText(customer_id)
            self.lineEditName.setText(name)
            self.lineEditPhone.setText(phone)
            self.lineEditCCCD.setText(cccd)
            self.lineEditDateCheckin.setText(checkin_date)
            self.lineEditRoomID.setText(room_id)

            room = next((room for room in self.rooms if room.room_id == room_id), None)
            if room:
                self.lineEditTypeRoom.setText(str(room.room_type))
                self.lineEditStatus.setText(str(room.status))
                self.lineEditFloor.setText(str(room.floor))

    def process_BookingApp(self):
        # Đóng cửa sổ hiện tại
        self.MainWindow.close()
        # Tạo cửa sổ mới cho BookingApp
        self.booking_window = QMainWindow()
        self.booking_ui = BookingAppExt(self.uid)
        self.booking_ui.setupUi(self.booking_window)
        self.booking_ui.showWindow()
    def open_pay_bill(self):
        selected_customer_row = self.tableWidgetCustomer.currentRow()
        if selected_customer_row < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn khách hàng!")
            return

        # Lấy ID khách hàng từ bảng
        customer_id = self.tableWidgetCustomer.item(selected_customer_row, 0).text()
        room_id = self.tableWidgetCustomer.item(selected_customer_row, 4).text()
        # Đọc dữ liệu từ JSON
        jff = JsonFileFactory()
        customers = jff.read_data("../dataset/customers.json", Customer)
        rooms = jff.read_data("../dataset/rooms.json", Room)
        customer_rooms = jff.read_data("../dataset/customer_room.json", Customer_Room)

        # Tìm thông tin khách hàng
        customer = next((c for c in customers if c.customer_id == customer_id), None)
        if not customer:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy khách hàng trong dữ liệu!")
            return

        customer_room = next((cr for cr in customer_rooms if cr.customer_id == customer_id and str(cr.room_id) == room_id), None)
        if not customer_room:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy thông tin đặt phòng của khách hàng!")
            return

        # Tìm thông tin phòng
        room = next((r for r in rooms if r.room_id == room_id), None)
        if not room:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy phòng trong dữ liệu!")
            return
        # Mở cửa sổ PayBillWindow và truyền dữ liệu khách hàng + phòng vào
        self.MainWindow.close()
        self.mainwindow = QMainWindow()
        self.myui = PayBillMainWindowExt(customer, room, customer_room,self.uid)
        self.myui.setupUi(self.mainwindow)
        self.myui.showWindow()
    def removeReceptionistFunctions(self):
        self.pushButtonSua.deleteLater()
        self.pushButtonDatPhong.deleteLater()
        self.pushButtonHoaDon.deleteLater()
        self.pushButtonXoa.deleteLater()
        self.groupBoxFunction.deleteLater()

    def search_room(self):
        search_text = self.lineEditSeachRoom.text().strip().lower()
        # Nếu ô tìm kiếm rỗng, hiển thị lại toàn bộ danh sách phòng
        if not search_text:
            self.show_rooms_gui()
            return
        self.tableWidgetRoom.setRowCount(0)
        for room in self.rooms:
            if isinstance(room, Room) and (search_text in str(room.room_id).lower() or search_text in str(room.floor).lower()) :
                row_position = self.tableWidgetRoom.rowCount()
                self.tableWidgetRoom.insertRow(row_position)

                # Tạo các QTableWidgetItem
                col_id = QTableWidgetItem(str(room.room_id))
                col_id.setData(Qt.ItemDataRole.UserRole, room.room_id)  # Lưu ID vào UserRole

                col_type = QTableWidgetItem(room.room_type)
                col_price_hourly = QTableWidgetItem(str(room.price_hourly))
                col_price_overnight=QTableWidgetItem(str(room.price_overnight))
                col_status = QTableWidgetItem(room.status)
                col_floor = QTableWidgetItem(str(room.floor))

                # Set dữ liệu vào bảng
                self.tableWidgetRoom.setItem(row_position, 0, col_id)
                self.tableWidgetRoom.setItem(row_position, 1, col_type)
                self.tableWidgetRoom.setItem(row_position, 2, col_price_hourly)
                self.tableWidgetRoom.setItem(row_position, 3, col_price_overnight)
                self.tableWidgetRoom.setItem(row_position, 4, col_status)
                self.tableWidgetRoom.setItem(row_position, 5, col_floor)

    def search_customer(self):
        search_text = self.lineEditSeachCustomer.text().strip().lower()
        if not search_text:
            self.show_customers_gui()
            return
        self.tableWidgetCustomer.setRowCount(0)
        for customer in self.customers:
            if search_text in customer.customer_id.lower() or search_text in customer.name.lower() or search_text in customer.phone or search_text in customer.cccd:
                row_position = self.tableWidgetCustomer.rowCount()
                self.tableWidgetCustomer.insertRow(row_position)

                customer_room = next((cr for cr in self.customer_rooms if cr.customer_id == customer.customer_id), None)
                checkin_date = customer_room.date_checkin.strftime(
                    "%d-%m-%Y %H:%M:%S") if customer_room and customer_room.date_checkin else "Chưa nhận phòng"

                # Set dữ liệu vào bảng
                self.tableWidgetCustomer.setItem(row_position, 0, QTableWidgetItem(customer.customer_id))
                self.tableWidgetCustomer.setItem(row_position, 1, QTableWidgetItem(customer.name))
                self.tableWidgetCustomer.setItem(row_position, 2, QTableWidgetItem(customer.phone))
                self.tableWidgetCustomer.setItem(row_position, 3, QTableWidgetItem(customer.cccd))
                self.tableWidgetCustomer.setItem(row_position, 4, QTableWidgetItem(customer_room.room_id))
                self.tableWidgetCustomer.setItem(row_position, 5, QTableWidgetItem(checkin_date))

    def delete_customer_room(self):
        index = self.tableWidgetCustomer.currentRow()
        if index < 0:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn khách hàng để xóa phòng!")
            return

        customer_id_item = self.tableWidgetCustomer.item(index, 0)  # Lấy Customer ID từ bảng
        if not customer_id_item:
            return
        customer_id = customer_id_item.text()
        room_id_item = self.tableWidgetCustomer.item(index, 4)  # Lấy Room ID từ bảng
        if not room_id_item:
            return
        room_id = room_id_item.text()

        # Hiển thị hộp thoại xác nhận
        reply = QMessageBox.question(
            self.MainWindow, "Xác nhận",
            f"Bạn có chắc muốn xóa phòng {room_id} của khách hàng {customer_id} không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )

        if reply == QMessageBox.StandardButton.Yes:
            jff = JsonFileFactory()
            rooms = jff.read_data("../dataset/rooms.json", Room)
            customer_rooms = jff.read_data("../dataset/customer_room.json", Customer_Room)

            # Xóa phòng đó khỏi danh sách customer_rooms
            updated_customer_rooms = [cr for cr in customer_rooms if
                                      not (cr.customer_id == customer_id and cr.room_id == room_id)]

            # Kiểm tra khách này còn phòng nào không
            remaining_rooms = [cr for cr in updated_customer_rooms if cr.customer_id == customer_id]

            # Nếu khách không còn phòng nào thì xóa luôn khách đó
            if not remaining_rooms:
                self.customers = [customer for customer in self.customers if customer.customer_id != customer_id]
                jff.write_data(self.customers, "../dataset/customers.json")

            # Cập nhật trạng thái phòng thành "trống"
            for room in rooms:
                if room.room_id == room_id:
                    room.status = "trống"
                    break

            # Ghi dữ liệu cập nhật xuống JSON
            jff.write_data(rooms, "../dataset/rooms.json")
            jff.write_data(updated_customer_rooms, "../dataset/customer_room.json")

            QMessageBox.information(self.MainWindow, "Thông báo",
                                    f"Đã xóa phòng {room_id} của khách hàng {customer_id}!")

            # Cập nhật lại giao diện
            self.rooms = jff.read_data("../dataset/rooms.json", Room)
            self.tableWidgetCustomer.setRowCount(0)
            self.show_customers_gui()
            self.show_rooms_gui()
            self.lineEditCustomerID.clear()
            self.lineEditName.clear()
            self.lineEditPhone.clear()
            self.lineEditCCCD.clear()
            self.lineEditDateCheckin.clear()
            self.lineEditStatus.setText("trống")
            self.tableWidgetCustomer.viewport().update()
            self.tableWidgetRoom.viewport().update()

    def edit_customer(self):
        # Kiểm tra xem có dòng nào được chọn không
        current_row_customer = self.tableWidgetCustomer.currentRow()
        if current_row_customer == -1:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng chọn dữ liệu ở bảng khách hàng để sửa!")
            return

        # Lấy ID khách hàng từ bảng (Không cho sửa ID)
        customer_id = self.tableWidgetCustomer.item(current_row_customer, 0).text()
        # Lấy dữ liệu mới từ giao diện
        new_name = self.lineEditName.text().strip()
        new_phone = self.lineEditPhone.text().strip()
        new_cccd = self.lineEditCCCD.text().strip()
        new_date_checkin = self.lineEditDateCheckin.text().strip()
        new_room_id = self.lineEditRoomID.text().strip()

        # Kiểm tra dữ liệu hợp lệ
        if not new_name or not new_phone or not new_cccd:
            QMessageBox.warning(self.MainWindow, "Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        if not new_phone.isdigit():
            QMessageBox.warning(self.MainWindow, "Lỗi", "Số điện thoại phải là số!")
            return

        if not new_cccd.isdigit():
            QMessageBox.warning(self.MainWindow, "Lỗi", "CCCD phải là số!")
            return

        # Chuyển đổi định dạng ngày từ dd-MM-yyyy -> yyyy-MM-dd
        date_obj = datetime.strptime(new_date_checkin, "%d-%m-%Y %H:%M:%S")
        new_date_checkin_json = date_obj.strftime("%Y-%m-%d %H:%M:%S")

        # Cập nhật dữ liệu khách hàng (chỉ sửa thông tin cá nhân, không liên quan phòng)
        for customer in self.customers:
            if str(customer.customer_id) == customer_id:
                customer.name = new_name
                customer.phone = new_phone
                customer.cccd = new_cccd
                break  # Dừng vòng lặp sau khi tìm thấy khách hàng

        # Lấy danh sách tất cả phòng mà khách đã đặt
        old_rooms = [cr.room_id for cr in self.customer_rooms if str(cr.customer_id) == customer_id]

        # Xác định phòng đang sửa (có thể là 1 trong nhiều phòng)
        old_room_id = self.tableWidgetCustomer.item(current_row_customer, 4).text()

        jff = JsonFileFactory()

        # Nếu khách không đổi phòng
        if old_room_id == new_room_id:
            for cr in self.customer_rooms:
                if str(cr.customer_id) == customer_id and cr.room_id == old_room_id:
                    cr.date_checkin = new_date_checkin_json
                    break
        else:
            # Kiểm tra phòng mới có hợp lệ không
            self.rooms = jff.read_data("../dataset/rooms.json", Room)
            room_found = next((room for room in self.rooms if room.room_id == new_room_id), None)

            if not room_found:
                QMessageBox.warning(self.MainWindow, "Lỗi", "Không tìm thấy phòng mới!")
                return

            if room_found.status.lower() == "có":
                QMessageBox.warning(self.MainWindow, "Lỗi", "Phòng mới đã được đặt trước đó!")
                return

            # Cập nhật trạng thái phòng cũ thành "trống" nếu khách không có phòng khác
            if old_room_id in old_rooms and old_rooms.count(old_room_id) == 1:
                for room in self.rooms:
                    if room.room_id == old_room_id:
                        room.status = "trống"
                        break

            # Cập nhật trạng thái phòng mới thành "có"
            room_found.status = "có"

            # Cập nhật thông tin phòng trong danh sách khách-phòng
            for cr in self.customer_rooms:
                if str(cr.customer_id) == customer_id and cr.room_id == old_room_id:
                    cr.room_id = new_room_id
                    cr.date_checkin = new_date_checkin_json
                    break

        # Lưu dữ liệu cập nhật xuống JSON
        jff.write_data(self.customers, "../dataset/customers.json")
        jff.write_data(self.customer_rooms, "../dataset/customer_room.json")
        jff.write_data(self.rooms, "../dataset/rooms.json")

        # Cập nhật trạng thái phòng trên bảng danh sách phòng
        if old_room_id != new_room_id:
            for i in range(self.tableWidgetRoom.rowCount()):
                room_id = self.tableWidgetRoom.item(i, 0).text()
                if room_id == old_room_id:
                    self.tableWidgetRoom.setItem(i, 4, QTableWidgetItem("trống"))
                elif room_id == new_room_id:
                    self.tableWidgetRoom.setItem(i, 4, QTableWidgetItem("có"))

        # Cập nhật lại bảng hiển thị thông tin khách hàng
        self.tableWidgetCustomer.setItem(current_row_customer, 1, QTableWidgetItem(new_name))
        self.tableWidgetCustomer.setItem(current_row_customer, 2, QTableWidgetItem(new_phone))
        self.tableWidgetCustomer.setItem(current_row_customer, 3, QTableWidgetItem(new_cccd))
        self.tableWidgetCustomer.setItem(current_row_customer, 4, QTableWidgetItem(new_room_id))
        self.tableWidgetCustomer.setItem(current_row_customer, 5, QTableWidgetItem(new_date_checkin))
        self.update_customer_room_type()
        QMessageBox.information(self.MainWindow, "Thông báo", "Sửa thành công!")

    def update_customer_room_type(self):
        current_row = self.tableWidgetCustomer.currentRow()
        if current_row == -1:
            return

        room_id = self.tableWidgetCustomer.item(current_row, 4).text()
        room_type = "Không xác định"

        for room in self.rooms:
            if room.room_id == room_id:
                room_type = room.room_type
                break

        self.lineEditTypeRoom.setText(room_type)
    def logout(self):
        """Quay về màn hình đăng nhập"""
        reply = QMessageBox.question(self.MainWindow,"Xác nhận đăng xuất","Bạn có chắc chắn muốn đăng xuất không?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.Yes
        )
        if reply == QMessageBox.StandardButton.No:
            return
        self.MainWindow.close()  # Đóng cửa sổ chính
        self.mainwindow = QMainWindow()  # Tạo cửa sổ mới cho màn hình đăng nhập
        self.myui = LoginMainWindowExt()  # Khởi tạo giao diện đăng nhập
        self.myui.setupUi(self.mainwindow)
        self.myui.showWindow()
    def exit_program(self):
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText(f"Bạn có chắc chắn muốn thoát phần mềm này không?")
        msgbox.setWindowTitle("Xác nhận thoát")
        msgbox.setIcon(QMessageBox.Icon.Critical)
        buttons = QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        msgbox.setStandardButtons(buttons)
        if msgbox.exec() == QMessageBox.StandardButton.Yes:
            exit()
    def export_to_excel(self):
        self.customer_rooms = [cr for cr in self.customer_rooms if
                               cr.customer_id in [c.customer_id for c in self.customers]]

        filename="../dataset/rooms.xlsx"
        extool=ExportTool()
        extool.export_room_to_excel(filename,self.rooms)
        filename_cus="../dataset/customers.xlsx"
        extool.export_customer_to_excel(filename_cus,self.customers, self.customer_rooms)
        msgbox = QMessageBox(self.MainWindow)
        msgbox.setText(f"Đã Export Excel thành công!")
        msgbox.setWindowTitle("Thông báo")
        msgbox.exec()
    def import_from_excel(self):
        filename = "../dataset/rooms.xlsx"
        filename_cus = "../dataset/customers.xlsx"
        extool = ExportTool()
        self.customers, self.customer_rooms = extool.import_customer_excel(filename_cus)
        self.rooms = extool.import_room_excel(filename)
        self.is_import_from_excel = True
        self.show_customers_gui()
        self.show_rooms_gui()
        QMessageBox.information(self.MainWindow, "Thông báo", "Import dữ liệu từ Excel thành công!")
    def open_help(self):
        file_help='HELP.pdf'
        #ta cần mở file_help lên
        # lấy đường dẫn hiện tại của phần mềm:
        current_path = os.getcwd()
        file_help = f"{current_path}/../assets/{file_help}"
        webbrowser.open_new(file_help)