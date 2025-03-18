from user import User
from database_service import DatabaseService
from vote import Vote

class Voter(User):
    def __init__(self, user_id: str):
        self.db_service = DatabaseService()
        user_data = self.db_service.get_user_data(user_id)

        if user_data and user_data.get("role") == "Voter":
            super().__init__(
                user_id=user_id,
                name=user_data.get("name"),
                province=user_data.get("province"),
                municipality=user_data.get("municipality"),
                email=user_data.get("email"),
                password=user_data.get("password"),  
                role="Voter"
            )
            self.__has_voted = user_data.get("has_voted", False)
            self.__face_recog = user_data.get("face_recog", str)
            self.__votes = [] 
        else:
            raise ValueError("User is not a voter or does not exist.")

    def has_voted(self) -> bool:
        return self.__has_voted

    def set_has_voted(self, has_voted: bool):
        self.__has_voted = has_voted

    def get_face_recog(self) -> str:
        return self.__face_recog

    def set_face_recog(self, face_recog: str):
        self.__face_recog = face_recog

    def get_votes(self):
        return self.__votes  

    def cast_vote(self, vote: Vote) -> bool:

        for existing_vote in self.get_votes():
            if existing_vote.get_position() == vote.get_position():
                return False  
        self.__votes.append(vote)  
        return True


