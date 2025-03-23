import bcrypt
from database_service import DatabaseService
db_service = DatabaseService()

def hash_password(password, role):
    if role.lower() == "admin":
        return password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def generate_id(prefix: str, object :str , get_last_entry):
    last_entry = get_last_entry()
    if last_entry:
        last_id = last_entry[f"{object}_id"]
        if last_id.startswith(prefix) and last_id[4:].isdigit():
            return f"{prefix}{int(last_id[4:]) + 1:02d}"
    return f"{prefix}01"

def generate_user_id() -> str:
    return generate_id("usid", "user", db_service.get_last_user_id)

def generate_ballot_id() -> str:
    return generate_id("baid", "ballot", db_service.get_last_ballot)

def generate_election_id() -> str:
    return generate_id("elid", "election", db_service.get_last_election)

def generate_candidate_id() -> str:
    return generate_id("caid", "candidate", db_service.get_last_candidate)
