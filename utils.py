import bcrypt
from database_service import db  # Import Firestore instance

def hash_password(password, role):
    """Hashes the password only for voters, keeps plain text for admins."""
    if role.lower() == "admin":
        return password 
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def generate_user_id():
    """Generates a sequential user ID (usid01, usid02, etc.)."""
    users_ref = db.collection("Users")
    users = users_ref.stream()

    user_ids = [doc.id for doc in users if doc.id.startswith("usid")]

    if not user_ids:
        return "usid01"

    user_numbers = [int(uid[4:]) for uid in user_ids if uid[4:].isdigit()]
    
    new_id_number = max(user_numbers) + 1 if user_numbers else 1

    return f"usid{new_id_number:02d}"
