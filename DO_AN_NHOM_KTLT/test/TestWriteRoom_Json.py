from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Room import Room

rooms=[]
rooms.append(Room("101","VIP",300000,500000,"trống","01"))
rooms.append(Room("102","đơn",100000,350000,"có","01"))
rooms.append(Room("103","đôi",200000,400000,"có","01"))
rooms.append(Room("104","VIP",300000,500000,"trống","01"))
rooms.append(Room("105","VIP",300000,500000,"có","01"))
rooms.append(Room("201","đơn",100000,350000,"có","02"))
rooms.append(Room("202","đôi",200000,400000,"có","02"))
rooms.append(Room("203","đơn",100000,350000,"trống","02"))
rooms.append(Room("204","đôi",200000,400000,"trống","02"))
rooms.append(Room("205","đôi",200000,400000,"trống","02"))
rooms.append(Room("301","VIP",300000,500000,"có","03"))
rooms.append(Room("302","đơn",100000,350000,"có","03"))
rooms.append(Room("303","đôi",200000,400000,"trống","03"))
rooms.append(Room("304","đơn",100000,350000,"trống","03"))
rooms.append(Room("305","VIP",300000,500000,"trống","03"))
rooms.append(Room("401","đôi",200000,400000,"có","04"))
rooms.append(Room("402","đơn",100000,350000,"có","04"))
rooms.append(Room("403","đôi",200000,400000,"trống","04"))
rooms.append(Room("404","VIP",300000,500000,"trống","04"))
rooms.append(Room("405","VIP",300000,500000,"có","04"))
print("Danh sách Room:")
for r in rooms:
    print(r)
jff=JsonFileFactory()
filename="../dataset/rooms.json"
jff.write_data(rooms,filename)