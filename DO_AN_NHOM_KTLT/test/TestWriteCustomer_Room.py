from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer_Room import Customer_Room

customerrooms=[]
customerrooms.append(Customer_Room("M01","102","2025-03-28 04:30:00"))
customerrooms.append(Customer_Room("M02","103","2025-03-27 14:50:00"))
customerrooms.append(Customer_Room("M03","105","2025-03-26 09:30:00"))
customerrooms.append(Customer_Room("M04","201","2025-03-27 21:15:00"))
customerrooms.append(Customer_Room("M05","202","2025-03-27 10:10:00"))
customerrooms.append(Customer_Room("M06","301","2025-03-26 16:19:00"))
customerrooms.append(Customer_Room("M07","302","2025-03-25 18:14:00"))
customerrooms.append(Customer_Room("M08","401","2025-03-24 09:23:00"))
customerrooms.append(Customer_Room("M09","402","2025-03-25 08:02:00"))
customerrooms.append(Customer_Room("M10","405","2025-03-23 07:40:00"))

print("Danh sách Customer theo Room:")
for cr in customerrooms:
    print(cr)
jff=JsonFileFactory()
filename="../dataset/customer_room.json"
jff.write_data(customerrooms,filename)
