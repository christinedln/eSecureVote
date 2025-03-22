from database_service import DatabaseService
from user import User 
from utils import hash_password

class VoterRegistrationService:
    _db_service = DatabaseService()  

    @staticmethod
    def register_voter(email, name, password, role, province, municipality):
        if VoterRegistrationService._db_service.check_existing_user(email):
            print("Registration failed: User already exists!")
            return False 

        if not VoterRegistrationService._db_service.check_registered_voter(email):
            print("Registration failed: You are not a registered voter!")
            return False 

        face_input = input("Press 'Enter' to approve face recognition or type 'delete' to cancel: ")
        if face_input.lower() == "delete":
            print("Face recognition failed. Registration aborted.")
            return False 

        user = User(None, name, email, password, role, province, municipality, face_recog=True) 
        user_id = user.get_user_id()

        user_data = {
            "user_id": user_id, 
            "name": name,
            "email": email,
            "password": hash_password(password, role), 
            "province": province,
            "municipality": municipality,
            "role": role,
            "face_recog": True,
            "has_voted": False
        }

        VoterRegistrationService._db_service.add_new_user(user.get_user_id(), user_data) 
        return True

register_voter = VoterRegistrationService.register_voter 
