from database_service import check_existing_user, check_registered_voter, add_new_user
from utils import hash_password, generate_user_id

class VoterRegistrationService:
    @staticmethod
    def register_voter(email, name, password, role, province, municipality):
        if check_existing_user(email):
            print("❌ Registration failed: User already exists!")
            return False 

        if not check_registered_voter(email):
            print("❌ Registration failed: You are not a registered voter!")
            return False 

        # 🔍 Face Recognition Prompt
        face_input = input("Press 'Enter' to approve face recognition or type 'delete' to cancel: ")
        if face_input.lower() == "delete":
            print("❌ Face recognition failed. Registration aborted.")
            return False 

        user_data = {
            "user_id": generate_user_id(),
            "name": name,
            "email": email,
            "password": hash_password(password, role), 
            "province": province,
            "municipality": municipality,
            "role": role,
            "face_recog": True,
            "has_voted": False
        }

        add_new_user(user_data["user_id"], user_data) 
        print(f"✅ Registration successful! User ID: {user_data['user_id']}")
        return True

register_voter = VoterRegistrationService.register_voter
