class Customer:
    def __init__(self,customer_id,name,phone,cccd):
        self.customer_id=customer_id
        self.name=name
        self.phone=phone
        self.cccd=cccd
    def __str__(self):
        return (f"Mã KH: {self.customer_id}\n"
                f"Tên KH: {self.name}\n"
                f"SĐT: {self.phone}\n"
                f"Số CCCD: {self.cccd}")