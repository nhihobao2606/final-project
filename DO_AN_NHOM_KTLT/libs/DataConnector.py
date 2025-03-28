

from DO_AN_NHOM_KTLT.libs.JsonFileFactory import JsonFileFactory
from DO_AN_NHOM_KTLT.models.Customer import Customer
from DO_AN_NHOM_KTLT.models.Customer_Room import Customer_Room
from DO_AN_NHOM_KTLT.models.Room import Room
from DO_AN_NHOM_KTLT.models.User import User


class DataConnector:
    def get_all_users(self):
        jff = JsonFileFactory()
        filename = "../dataset/users.json"
        users = jff.read_data(filename, User)
        return users
    def get_all_customer(self):
        jff = JsonFileFactory()
        filename = "../dataset/customers.json"
        customers = jff.read_data(filename, Customer)
        return customers
    def get_all_room(self):
        jff = JsonFileFactory()
        filename = "../dataset/rooms.json"
        rooms = jff.read_data(filename, Room)
        return rooms
    def get_all_customer_room(self):
        jff = JsonFileFactory()
        filename = "../dataset/customer_room.json"
        obj = jff.read_data(filename, Customer_Room)
        return obj

    def login(self,username,password):
        users=self.get_all_users()
        for u in users:
            if u.username==username and u.password==password:
                return u
        return None
