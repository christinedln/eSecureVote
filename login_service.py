import bcrypt
from database_service import DatabaseService

class LoginService:
    _db_service = DatabaseService()  

    @staticmethod
    def authenticate_user(email: str, password: str):
        user_data = LoginService._db_service.get_user_by_email(email)

        if not user_data:
            print("User not found!")
            return None

        stored_password = user_data["password"]

        if not bcrypt.checkpw(password.encode(), stored_password.encode()):
            print("Invalid password!")
            return None

        from user import User  

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

        face_input = input("Face Recognition Required: Press 'Enter' to approve or type 'delete' to cancel: ")
        if face_input.lower() == "delete":
            print("Face recognition failed. Access denied!")
            return None

        LoginService._db_service.update_user_face_recog(user.get_user_id(), True)
        print("Face recognition successful! User logged in.")
        return user 