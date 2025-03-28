from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Room import Room

rooms=[]
jff=JsonFileFactory()
filename="../dataset/rooms.json"
rooms=jff.read_data(filename,Room)
print("List of Room after Loading Json:")
for room in rooms:
    print(room)