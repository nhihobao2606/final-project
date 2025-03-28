from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer import Customer

customers=[]
customers.append(Customer("M01","Lung Linh","0709315384","0522306574"))
customers.append(Customer("M02","Thanh Thản","0587684258","0792012345"))
customers.append(Customer("M03","Long Lanh","0308593673","0547254762"))
customers.append(Customer("M04","Lấp Lánh","0956384652","0823045678"))
customers.append(Customer("M05","Kiêu Sa","0853795273","0654071238"))
customers.append(Customer("M06","Hột Lựu","0625739406","0285078923"))
customers.append(Customer("M07","Lựu Đạn","0506384624","0945098760"))
customers.append(Customer("M08","Aka","0383825403","0104646832"))
customers.append(Customer("M09","Mèo Sammy","0264835463","0352846348"))
customers.append(Customer("M10","Vy đẹp gái","0756835483","0592467490"))
print("Danh sách Customer:")
for c in customers:
    print(c)
jff=JsonFileFactory()
filename="../dataset/customers.json"
jff.write_data(customers,filename)