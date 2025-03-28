class User:
    def __init__(self,username,password,role):
        self.username=username
        self.password=password
        self.role=role
    def __str__(self):
        return f"{self.username}\t{self.password}\t{self.role}"