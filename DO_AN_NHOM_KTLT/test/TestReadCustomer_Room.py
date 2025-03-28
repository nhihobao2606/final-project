from DO_AN_NHOM_KTLT.models.Customer_Room import Customer_Room
from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory

jff=JsonFileFactory()
filename="../dataset/customer_room.json"
CustomerRooms=jff.read_data(filename,Customer_Room)
print("Danh sách Customer_Room sau khi đọc file:")
for cr in CustomerRooms:
    print(cr)