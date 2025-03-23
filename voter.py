from user import User
from database_service import DatabaseService
from vote import Vote
from register_service import VoterRegistrationService

class Voter(User):
    _db_service = DatabaseService()
    _register_service=VoterRegistrationService()


    def __init__(self, user_id, name=None, email=None, password=None, province=None, municipality=None, address=None, face_recog=None, has_voted=False):
        if name is None:  
            user_data = self._db_service.get_user_data(user_id)


            if not user_data or user_data.get("role") != "Voter":
                raise ValueError("User is not a voter or does not exist.")
           
            name = user_data.get("name")
            email = user_data.get("email")
            password = user_data.get("password")
            province = user_data.get("province")
            municipality = user_data.get("municipality")
            face_recog = user_data.get("face_recog", None)  
            has_voted = user_data.get("has_voted", False)


        super().__init__(user_id, name, email, password, "Voter", province, municipality, face_recog)


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