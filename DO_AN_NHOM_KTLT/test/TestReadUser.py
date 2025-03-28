from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.User import User

jff=JsonFileFactory()
filename="../dataset/users.json"
users=jff.read_data(filename,User)
print("Tài khoản user sau khi đọc từ file:")
for u in users:
    print(u)