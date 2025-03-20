from database_service import update_user_profile, add_new_user, update_user_face_recog
from utils import hash_password, generate_user_id

class User:
    def __init__(self, user_id, name, email, password, role, province, municipality, face_recog=False):
        self.__user_id = user_id
        self.__name = name
        self.__email = email
        self.__password = password
        self.__role = role
        self.__province = province
        self.__municipality = municipality
        self.__face_recog = face_recog
        
    def get_user_id(self):
        return self.__user_id
    
    def get_name(self):
        return self.__name
    
    def get_email(self):
        return self.__email
    
    def get_role(self):
        return self.__role
    
    def get_province(self):
        return self.__province
    
    def get_municipality(self):
        return self.__municipality
    
    def get_face_recog(self):
        return self.__face_recog
    
    def get_password(self):
        return self.__password
    
    # ✅ Setters
    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_password(self, password, role):
        self.__password = hash_password(password, role)

    def set_role(self, role):
        self.__role = role

    def set_province(self, province):
        self.__province = province

    def set_municipality(self, municipality):
        self.__municipality = municipality

    def set_face_recog(self, status):
        self.__face_recog = status
        update_user_face_recog(self.get_user_id(), status)
    
    def update_profile(self, name=None, email=None, password=None):
        updated_data = {}
        if name:
            self.set_name(name)
            updated_data["name"] = name
        if email:
            self.set_email(email)
            updated_data["email"] = email
        if password:
            self.set_password(password, self.get_role())
            updated_data["password"] = self.__password
        if updated_data:
            update_user_profile(self.get_user_id(), updated_data)
            print("✅ Profile updated successfully!")

    def to_dict(self):
        """Converts User object to a dictionary for Firestore."""
        return {
            "user_id": self.get_user_id(),
            "name": self.get_name(),
            "email": self.get_email(),
            "password": self.get_password(),
            "role": self.get_role(),
            "province": self.get_province(),
            "municipality": self.get_municipality(),
            "face_recog": self.get_face_recog(),
        }
