from user import User
from database_service import DatabaseService
from election import Election

class Admin(User):
    def __init__(self, user_id: int):
        self.db_service = DatabaseService()
        user_data = self.db_service.get_user_data(user_id)

        if user_data and user_data.get("role") == "Admin":
            super().__init__(user_id, role="Admin")
            self.__admin_level = user_data.get("adminLevel", 0)
        else:
            raise ValueError("User is not an admin or does not exist.")

    def get_admin_level(self) -> int:
        return self.__admin_level

    def set_admin_level(self, admin_level: int):
        self.__admin_level = admin_level

    def get_user_id(self) -> int:
        return super().get_user_id()

    def create_election(self, election: Election):
        election_data = {
            "election_id" : election.get_election_id(),
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
