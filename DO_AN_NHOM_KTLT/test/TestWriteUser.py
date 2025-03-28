from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.User import User

users=[]
users.append(User('nhi','123',"Admin"))
users.append(User('thuong','345',"Admin"))
users.append(User("Trammetmoi","tram123","Receptionist"))
users.append(User("Vytrumcoder","hacker123","Receptionist"))

print("Danh sách tài khoản user:")
for u in users:
    print(u)
jff=JsonFileFactory()
filename="../dataset/users.json"
jff.write_data(users,filename)