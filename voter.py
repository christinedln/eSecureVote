from user import User
from database_service import DatabaseService
from vote import Vote
from register_service import VoterRegistrationService

class Voter(User):
    _db_service = DatabaseService()
    _register_service=VoterRegistrationService()

    def __init__(self, user_id, name="", email="", password="", province="", municipality="", address=None, face_recog=None, has_voted=False):
        super().__init__(user_id, name, email, password, "Voter", province, municipality, face_recog)
        self.__address = address
        self.__has_voted = has_voted
        self.__votes = []

    def get_address(self):
        return self.__address
   
    def set_address(self, address):
        self.__address = address
        
    def get_face_recog(self) -> str:
        return self.__face_data

    def set_face_recog(self, face_data: str):
        self.__face_data = face_data

    def has_already_voted(self) -> bool:
        return self.__has_voted

    def set_has_voted(self, status: bool):
        self.__has_voted = status

    def get_votes(self):
        return self.__votes  

    def cast_vote(self, vote: Vote) -> bool:
        for existing_vote in self.__votes:
            if existing_vote.get_position() == vote.get_position():
                return False  
        self.__votes.append(vote)  
        return True  
   
    def register(self):
        return self._register_service.register_voter(
            self.get_email(), self.get_name(), self.get_password(), "Voter",
            self.get_province(), self.get_municipality()
        )