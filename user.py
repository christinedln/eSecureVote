from database_service import DatabaseService
from login_service import LoginService
from utils import hash_password, generate_user_id


class User:
    _db_service = DatabaseService()
    def __init__(self, user_id, name, email, password, role, province, municipality, face_recog=False):
        self.__user_id = user_id if user_id else generate_user_id()
        self.__name = name
        self.__email = email
        self.__password = password
        self.__role = role
        self.__province = province
        self.__municipality = municipality
        self.__face_recog = face_recog
        self._login_service = LoginService()
       
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
        self._db_service.update_user_face_recog(self.get_user_id(), status)
   
    def logout(self):
        self.__email = None
        self.__password = None
       
    @staticmethod
    def login(email, password):
        return LoginService.authenticate_user(email, password)