class User:
    def __init__(self, user_id: str, name: str = None, province: str = None, municipality: str = None, email: str = None, password: str = None, role: str = "User"):
        self.__user_id = user_id
        self.__name = name
        self.__province = province
        self.__municipality = municipality
        self.__email = email
        self.__password = password #hash this
        self.__role = role

    def get_user_id(self) -> str:
        return self.__user_id
    
    def get_name(self) -> str:
        return self.__name
    
    def get_email(self) -> str:
        return self.__email
    
    def get_role(self) -> str:
        return self.__role
    
    def get_province(self) -> str:
        return self.__province
    
    def get_municipality(self) -> str:
        return self.__municipality

    def set_user_id(self, user_id: str):
        self.__user_id = user_id
    
    def set_name(self, name: str):
        self.__name = name
    
    def set_municipality(self, municipality: str):
        self.__municipality = municipality

    def set_province(self, province: str):
        self.__province = province
    
    def set_email(self, email: str):
        self.__email = email
    
    def set_role(self, role: str):
        self.__role = role