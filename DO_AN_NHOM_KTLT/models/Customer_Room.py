from datetime import datetime


class Customer_Room:
    def __init__(self, customer_id, room_id, date_checkin):
        self.customer_id = customer_id
        self.room_id = room_id
        self.date_checkin = date_checkin
        if isinstance(self.date_checkin, str):  # Nếu là chuỗi, chuyển thành datetime
            self.date_checkin = datetime.strptime(self.date_checkin, "%Y-%m-%d %H:%M:%S")
        else:
            self.date_checkin = date_checkin
    def __str__(self):
        return (f"Mã KH: {self.customer_id}\n"
                f"Mã phòng: {self.room_id}\n"
                f"Ngày nhận phòng: {self.date_checkin.strftime('%d-%m-%Y %H:%M:%S')}\n")
