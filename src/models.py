class Customer:
    def __init__(self, name, email, city):
        self.name = name
        self.email = email
        self.city = city
        self.is_active = True


    def deactivate(self):
        self.is_active = False
        print(f"Customer {self.name} deactivated")


    def show_info(self):
        status = "active" if self.is_active else "inactive"
        print(f"{self.name} | {self.email} | {self.city} | {status}")