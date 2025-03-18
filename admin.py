from user import User
from database_service import DatabaseService
from election import Election

class Admin(User):
    def __init__(self, user_id: str):
        self.db_service = DatabaseService()
        user_data = self.db_service.get_user_data(user_id)

        if user_data and user_data.get("role") == "Admin":
            super().__init__(
                user_id=user_id,
                name=user_data.get("name"),
                province=user_data.get("province"),
                municipality=user_data.get("municipality"),
                email=user_data.get("email"),
                password=user_data.get("password"), #hashed
                role="Admin"
            )
            self.__admin_level = user_data.get("admin_level", 0)
        else:
            raise ValueError("User is not an admin or does not exist.")

    def get_admin_level(self) -> int:
        return self.__admin_level

    def set_admin_level(self, admin_level: int):
        self.__admin_level = admin_level

    def create_election(self, election: Election):
        election_data = {
            "election_id": election.get_election_id(),
            "date": election.get_date(),
            "time": election.get_time(),
            "location": election.get_location(),
            "is_open": election.get_is_open()
        }
        self.db_service.save_election(election_data)

    def start_election(self, election_id: str):
        Election.start_election(election_id)

    def close_election(self, election_id: str):
        Election.close_election(election_id)
