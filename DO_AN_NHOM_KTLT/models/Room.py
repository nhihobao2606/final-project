class Room:
    def __init__(self,room_id,room_type,price_hourly,price_overnight,status,floor):
        self.room_id=room_id
        self.room_type=room_type
        self.price_hourly=price_hourly
        self.price_overnight=price_overnight
        self.status=status
        self.floor=floor
    def __str__(self):
        return (f"Phòng: {self.room_id}\n"
                f"Tầng: {self.floor}\n"
                f"Loại phòng: {self.room_type}\n"
                f"Giá theo giờ: {self.price_hourly}\n"
                f"Giá qua đêm: {self.price_overnight}\n"
                f"Tình trạng: {self.status}")

