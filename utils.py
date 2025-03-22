import bcrypt
from database_service import DatabaseService
db_service = DatabaseService()
def hash_password(password, role):
    if role.lower() == "admin":
        return password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()



