from datetime import datetime, timedelta

from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer_Room import Customer_Room


class Bill:
    def __init__(self, bill_id, customer_id, customer_name, room_id, room_type, date_checkin, date_checkout, stay_duration, rent_price, price, extra_fee, total_price, payment_method=None):
        self.bill_id = bill_id
        self.customer_id=customer_id
        self.customer_name = customer_name
        self.room_id = room_id
        self.room_type=room_type
        self.date_checkin = self.get_checkin_date(customer_id)
        if isinstance(self.date_checkin, str):  # Nếu là chuỗi, chuyển thành datetime
            self.date_checkin = datetime.strptime(self.date_checkin, "%Y-%m-%d %H:%M:%S")
        else:
            self.date_checkin = date_checkin
        if isinstance(date_checkout, str):  # Chỉ chuyển đổi nếu nó là chuỗi
            self.date_checkout = datetime.strptime(date_checkout, "%Y-%m-%d %H:%M:%S")
        else:
            self.date_checkout = date_checkout  # Nếu đã là datetime thì giữ nguyên

        self.stay_duration=stay_duration
        self.rent_price = float(rent_price) if isinstance(rent_price, str) else rent_price
        self.price = float(price) if price not in [None, ""] else 0.0
        self.extra_fee = float(extra_fee) if extra_fee not in [None, ""] else 0.0
        self.total_price = float(total_price) if total_price not in [None, ""] else 0.0
        self.payment_method = payment_method

    def get_checkin_date(self, customer_id):
        jff = JsonFileFactory()
        customer_rooms = jff.read_data("../dataset/customer_room.json",Customer_Room)

        customer_room = next((cr for cr in customer_rooms if cr.customer_id == customer_id), None)
        if customer_room:
            return customer_room.date_checkin
        return None

    @staticmethod
    def determine_price_type(date_checkin,date_checkout):
        if isinstance(date_checkin, str):
            date_checkin = datetime.strptime(date_checkin, "%Y-%m-%d %H:%M:%S")
        if isinstance(date_checkout, str):
            date_checkout = datetime.strptime(date_checkout, "%Y-%m-%d %H:%M:%S")
        duration = (date_checkout - date_checkin).total_seconds() / 3600
        overnight_start = datetime.combine(date_checkin.date(), datetime.min.time()) + timedelta(hours=14)
        overnight_end = datetime.combine(date_checkin.date(), datetime.min.time()) + timedelta(hours=12 + 24)

        if date_checkin >= overnight_start and date_checkout <= overnight_end or duration >= 12:
            return 'overnight'
        return 'hourly'

    def calculate_stay_duration(self):
        """Tính thời gian lưu trú (số giờ hoặc số đêm)"""
        duration = (self.date_checkout - self.date_checkin).total_seconds() / 3600  # Số giờ
        if self.determine_price_type(self.date_checkin,self.date_checkout) == "overnight":
            return "1 ngày" if duration < 24 else f"{int(duration // 24)} ngày"
        return f"{int(duration)} giờ"

    def calculate_total_price(self, room):
        """Tính tổng tiền hóa đơn"""
        duration_days = (self.date_checkout - self.date_checkin).days

        self.extra_fee = float(self.extra_fee) if isinstance(self.extra_fee, str) else self.extra_fee

        price_hourly = float(room.price_hourly) if isinstance(room.price_hourly, str) else room.price_hourly
        price_overnight = float(room.price_overnight) if isinstance(room.price_overnight, str) else room.price_overnight

        if self.determine_price_type(self.date_checkin, self.date_checkout) == 'hourly':
            duration = (self.date_checkout - self.date_checkin).total_seconds() / 3600
            self.price = round(duration * price_hourly, 2)

        elif self.determine_price_type(self.date_checkin, self.date_checkout) == 'overnight':
            self.price = price_overnight * (duration_days if duration_days > 1 else 1)

            if 5 <= self.date_checkin.hour < 9:
                self.extra_fee += price_overnight * 0.5
            elif 9 <= self.date_checkin.hour < 14:
                self.extra_fee += price_overnight * 0.3

            if 12 < self.date_checkout.hour < 15:
                self.extra_fee += price_overnight * 0.3
            elif 15 <= self.date_checkout.hour < 18:
                self.extra_fee += price_overnight * 0.5
            elif self.date_checkout.hour >= 18:
                self.extra_fee += price_overnight

        self.total_price = round(self.price + self.extra_fee, 2)
        return self.total_price

    def __str__(self):
        return (f"Hóa đơn: {self.bill_id}\nKhách hàng: {self.customer_id}\nTên Khách hàng: {self.customer_name}\nPhòng: {self.room_id}\nLoại phòng: {self.room_type}"
                f"Ngày nhận: {self.date_checkin.strftime('%d-%m-%Y %H:%M:%S')}\nNgày trả: {self.date_checkout.strftime('%d-%m-%Y %H:%M')}\n"
                f"Tiền thuê phòng: {self.rent_price} VND\nThành tiền: {self.price}\nPhụ thu: {self.extra_fee} VND\n"
                f"Tổng tiền: {self.total_price} VND\n"
                f"Phương thức thanh toán: {self.payment_method if self.payment_method else 'Chưa xác định'}")

