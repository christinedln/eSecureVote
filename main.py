from admin import Admin

def main():
    email = input("Enter email: ")
    password = input("Enter password: ")
    
    admin = Admin.get_admin_from_db(email, password)

    """
    this part is just for checking and should be deleted later
    if admin:
        print("Logged-in Admin ID:", admin.get_user_id()) 
        print("Admin Level:", admin.get_admin_level())
    else:
        print("Invalid email or password.")"
    """

if __name__ == "__main__":
    main()