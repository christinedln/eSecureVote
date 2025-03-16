from admin import Admin
from database_service import DatabaseService
from election import Election  
from candidate import Candidate


def admin_menu(admin: Admin):
    while True:
        print("1. Create Election")
        print("2. Add Candidate")
        print("3. Start Election")
        print("4. Close Election")
        print("5. Count Results")
        print("6. View and Publish Results")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            if admin.get_admin_level() == 1:
                election_date = input("Enter the date of the election(YYYY-MM-DD): ") 
                election_time = input("Enter the time of the election(HH:MM AM/PM): ") 
                election_location = input("Enter election location: ")
                is_open = False
                election = Election(election_id=None, election_date=election_date, election_time=election_time, location=election_location, is_open=is_open)
                admin.create_election(election)
                print("Election has been saved successfully")
            else:
                print("Access Denied: You do not have the required admin level.")

        elif choice == "2":
            if admin.get_admin_level() == 1:
                db_service = DatabaseService()
                election = Election()
                elections = db_service.get_all_elections() 

                if elections:
                    print("\nStored Elections:")
                    for election in elections:
                        print(f"ID: {election['election_id']}, Date: {election['date']}, Time: {election['time']}, Location: {election['location']}")
                    
                    election_id = input("\nEnter the Election ID you want to select: ")
                    
                    selected_election = next((e for e in elections if e['election_id'] == election_id), None)

                    if selected_election:
                        print(f"\nYou selected Election ID: {selected_election['election_id']}")

                        election = Election(selected_election['election_id'], selected_election['date'], 
                                    selected_election['time'], selected_election['location'])

                        name = input("Enter the name of the candidate: ")
                        position = input("Enter the position: ")
                        is_independent = input("Is the candidate independent? (y/n): ").strip().lower()
                        is_independent = True if is_independent == 'y' else False
                        political_party = input("Enter the political party: ") if not is_independent else "Independent"
                        candidate = Candidate(name, position, is_independent, political_party)
                        election.add_candidate(selected_election["election_id"], candidate)

                        print("Candidate has been saved successfully.")
                    else:
                        print("Invalid Election ID. Please enter a valid one.")
                else:
                    print("No elections found in the database.")
            else:
                print("Access Denied: You do not have the required admin level.")
        elif choice in ["3", "4"]:
            if admin.get_admin_level() != 2:
                print("Access Denied: You do not have the required admin level.")
                return

            db_service = DatabaseService()
            elections = db_service.get_all_elections()

            if not elections:
                print("No elections found in the database.")
                return

            print("\nStored Elections:")
            for election in elections:
                print(f"ID: {election['election_id']}, Date: {election['date']}, Time: {election['time']}, Location: {election['location']}")

            action = "start" if choice == "3" else "close"
            election_id = input(f"\nEnter the Election ID you want to {action}: ")
            selected_election = next((e for e in elections if e['election_id'] == election_id), None)

            if selected_election:
                print(f"\nYou selected Election ID: {selected_election['election_id']}")
                getattr(admin, f"{action}_election")(selected_election["election_id"])
                print(f"Election is now {action}ed!")
            else:
                print("Invalid Election ID. Please enter a valid one.")
        elif choice == "5":
            print("5")
        elif choice == "6":
            print("6")
        elif choice == "7":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def main():
    user_id = 1
    admin = Admin(user_id) 
    admin_menu(admin)  

if __name__ == "__main__":
    main()
