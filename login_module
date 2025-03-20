import bcrypt
from database_service import get_user_by_email, update_user_face_recog
from user import User

class LoginService:
    @staticmethod
    def authenticate_user(email: str, password: str):
        user_data = get_user_by_email(email)
        if not user_data:
            print("❌ User not found!")
            return None

        stored_password = user_data["password"]
        role = user_data["role"].lower()

        if role == "admin":
            if password != stored_password:
                print("❌ Invalid password!")
                return None
        else:
            if not bcrypt.checkpw(password.encode(), stored_password.encode()):
                print("❌ Invalid password!")
                return None

        user = User(
            user_id=user_data["user_id"],
            name=user_data["name"],
            email=user_data["email"],
            password=stored_password,  
            role=user_data["role"],
            province=user_data.get("province", "Unknown"),
            municipality=user_data.get("municipality", "Unknown"),
            face_recog=user_data["face_recog"]
        )

        face_input = input("🔍 Face Recognition Required: Press 'Enter' to approve or type 'delete' to cancel: ")
        if face_input.lower() == "delete":
            print("❌ Face recognition failed. Access denied!")
            return None

        update_user_face_recog(user.get_user_id(), True)
        print("✅ Face recognition successful! User logged in.")
        return user 

    @staticmethod
    def logout(user):
        """Logs out the user by resetting session state and updating face recognition."""
        if user:
            update_user_face_recog(user.get_user_id(), False) 
            print(f"✅ {user.get_name()} has been logged out successfully!")
            return None 
        else:
            print("⚠ No valid user is logged in.")
