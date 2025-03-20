from database_service import add_new_user, check_registered_voter
from user import User

class Voter(User):
    def __init__(self, user_id, name, email, password, province, municipality, address, face_data, has_voted=False):
        super().__init__(user_id, name, email, password, "Voter", province, municipality, face_recog=True)
        self.__address = address
        self.__face_data = face_data
        self.__has_voted = has_voted

    def get_address(self):
        return self.__address
    
    def has_already_voted(self):
        return self.__has_voted
    
    def set_address(self, address):
        self.__address = address
    
    def set_has_voted(self, status):
        self.__has_voted = status
    
    def register(self):
        if check_registered_voter(self.get_email()):
            voter_data = self.to_dict()
            voter_data.update({"address": self.__address, "face_data": self.__face_data, "has_voted": self.__has_voted})
            add_new_user(self.get_user_id(), voter_data)
            print("✅ Voter registration successful!")
            return self
        print("❌ Registration failed: You are not a registered voter.")
        return None
