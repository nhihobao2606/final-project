from DO_AN_NHOM_KTLT.libs.DataConnector import DataConnector

dc=DataConnector()
users=dc.get_all_users()
print("List of users in dataset:")
for u in users:
    print(u)

# Kiểm tra danh sách Customers
customers = dc.get_all_customer()
print("List of customers in dataset:")
for customer in customers:
    print(customer)

# Kiểm tra danh sách Rooms
rooms = dc.get_all_room()
print("List of rooms in dataset:")
for room in rooms:
    print(room)

# Kiểm tra danh sách Customer_Room (khách thuê phòng)
customer_rooms = dc.get_all_customer_room()
print("\nList of customer_room (rented rooms) in dataset:")
for cr in customer_rooms:
    print(cr)
#Test chức năng đăng nhập hệ thống
uid="thuong"
pwd="345"
user=dc.login(uid,pwd)
if user!=None:
    print("Đăng nhập thành công")
else:
    print("Đăng nhập thất bại")


