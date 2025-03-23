from user import User
from database_service import DatabaseService
from election import Election

class Admin(User):
    _db_service = DatabaseService()
    def __init__(self, user_id: str):
        user_data = self._db_service.get_user_data(user_id)

        if user_data and user_data.get("role") == "Admin":
            super().__init__(
                user_id=user_id,
                name=user_data.get("name"),
                province=user_data.get("province"),
                municipality=user_data.get("municipality"),
                email=user_data.get("email"),
                password=user_data.get("password"),
                role="Admin",
                face_recog=True
            )
            self.__admin_level = user_data.get("admin_level", 0)
        else:
            raise ValueError("User is not an admin or does not exist.")

    def get_admin_level(self) -> int:
        return self.__admin_level

    def set_admin_level(self, admin_level: int):
        self.__admin_level = admin_level

    def check_admin_privileges(self, required_level):
        if self.get_admin_level() >= required_level:
            return True
        else:
            return False