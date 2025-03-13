from user import User

class Admin(User):

    def __init__(self, user_id: int, admin_level: int):
        super().__init__(user_id, role="Admin")  
        self.__admin_level = admin_level 

    def get_admin_level(self) -> int:
        return self.__admin_level

    def set_admin_level(self, admin_level: int):
        self.__admin_level = admin_level

    def get_user_id(self) -> int:
        return super().get_user_id() 

    @staticmethod
    def get_admin_from_db(username: str, password: str):

        # In a real application, this would query the database
        if username == "admin1" and password == "admin1password":
            user_id = 1  # Example user_id for admin1
            admin_level = 3  # Example admin level for admin1
            return Admin(user_id, admin_level)

        return None  