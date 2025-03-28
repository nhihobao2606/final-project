from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer import Customer

customers=[]
jff=JsonFileFactory()
filename="../dataset/customers.json"
customers=jff.read_data(filename,Customer)
print("List of Customer after Loading Json:")
for customer in customers:
    print(customer)