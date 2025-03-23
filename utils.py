import bcrypt
from database_service import DatabaseService
db_service = DatabaseService()
def hash_password(password, role):
    if role.lower() == "admin":
        return password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def generate_user_id() -> str:
    last_user_id = db_service.get_last_user_id()

    if last_user_id:
        last_id = last_user_id["user_id"]
        if last_id.startswith("usid") and last_id[4:].isdigit():
            return f"usid{int(last_id[4:]) + 1:02d}"

    return "usid01"

