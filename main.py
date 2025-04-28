from admin import Admin
from database_service import DatabaseService
from election import Election  
from candidate import Candidate
from voter import Voter
from ballot import Ballot
from vote import Vote
from login_service import LoginService
from encryption_service import EncryptionService
from election_manager import ElectionManager
from auditbook import AuditBook
from auditbook_manager import AuditBookManager
from user import User
from datetime import datetime
encryption_service = EncryptionService()
login_service = LoginService()
db_service = DatabaseService()
current_user = None

def admin_menu(admin: Admin):
    while True:
        print("1. Create Election")
        print("2. Add Candidate")
        print("3. Start Election")
        print("4. Close Election")
        print("5. Count Results")
        print("6. View and Publish Results")
        print("7. View Logs")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            if admin.check_admin_privileges(1):
                date = input("Enter the date of the election(YYYY-MM-DD): ")
                time = input("Enter the time of the election(HH:MM AM/PM): ")
                location = input("Enter election location: ")
                is_open = False
                election = Election(election_id=None, date=date, time=time, location=location, is_open=is_open)
                result = election.create_election()

                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                action = f"added election {election.get_election_id()}"
                user_id = admin.get_user_id()  
                manager = AuditBookManager()
                log = AuditBook(auditlog_id = None, user_id=user_id, action=action, timestamp=timestamp)
                manager.create_log(log)

                if result:
                    print("Election has been saved successfully!")
                else:
                    print("Election creation failed.")
            else:
                print("Access Denied: You do not have the required admin level.")

        elif choice == "2":
            if admin.check_admin_privileges(1):
                elections = db_service.get_all_elections()

                if elections:
                    print("\nStored Elections:")
                    for election in elections:
                        print(f"ID: {election['election_id']}, Date: {election['date']}, Time: {election['time']}, Location: {election['location']}")
                   
                    election_id = input("\nEnter the Election ID you want to select: ")
                   
                    selected_election = next((e for e in elections if e['election_id'] == election_id), None)

                    if selected_election:
                        election = Election(selected_election['election_id'], selected_election['date'],
                                    selected_election['time'], selected_election['location'])

                        name = input("Enter the name of the candidate: ")
                        position = input("Enter the position: ")
                        is_independent = input("Is the candidate independent? (y/n): ").strip().lower()
                        is_independent = True if is_independent == 'y' else False
                        political_party = input("Enter the political party: ") if not is_independent else "Independent"
                        candidate = Candidate(name, position, is_independent, political_party)
                        result = election.add_candidate(selected_election["election_id"], candidate)

                        user_id = admin.get_user_id()
                        action = f"Added candidate {name} to election {election_id}"
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        manager = AuditBookManager()
                        log = AuditBook(auditlog_id = None, user_id=user_id, action=action, timestamp=timestamp)
                        manager.create_log(log)

                        if result:
                            print("Candidate has been added successfully!")
                        else:
                            print("Adding a candidate failed.")
                       
                    else:
                        print("Invalid Election ID. Please enter a valid one.")
                else:
                    print("No elections found in the database.")
            else:
                print("Access Denied: You do not have the required admin level.")

        elif choice in ["3", "4"]:
            election_manager = ElectionManager(db_service, encryption_service)
            if  admin.check_admin_privileges(2):
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
                    result = getattr(election_manager, f"{action}_election")(selected_election["election_id"])
                    if result:
                        if action == "start":
                            print("Election started successfully.")
                        else:
                            print("Election closed successfully.")
                    else:
                        print(f"Failed to {action} the election.")
                        
                    user_id = admin.get_user_id()
                    action = f"{action.capitalize()}ed election {election_id}"
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                    manager = AuditBookManager()
                    log = AuditBook(auditlog_id = None, user_id=user_id, action=action, timestamp=timestamp)
                    manager.create_log(log)
                else:
                    print("Invalid Election ID. Please enter a valid one.")
            else: print("Access Denied: You do not have the required admin level.")

        elif choice == "5":
            election_manager = ElectionManager(db_service, encryption_service)
            if admin.check_admin_privileges(3):
                location = input("Enter the location of the election you want to count the votes: ").strip()
               
                elections = db_service.get_elections_by_location(location)
                if not elections:
                    print(f"No elections found for location: {location}")
                    continue
                    
                election_id = elections[0]["election_id"]  
                if not election_manager.is_election_open(election_id):
                    encrypted_ballots = db_service.get_all_encrypted_ballots(election_id)
                    election_manager.get_decrypted_ballots(election_id, encrypted_ballots)
                    result = election_manager.encrypt_result(election_id)

                    user_id = admin.get_user_id()
                    action = f"Decrypted and encrypted results for election {election_id} at location {location}"
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    manager = AuditBookManager()
                    log = AuditBook(auditlog_id = None, user_id=user_id, action=action, timestamp=timestamp)
                    manager.create_log(log)
                    if result:
                        print("Counting of votes finished!")
                    else: 
                        print("Counting of votes failed.")
                else:
                    print("The election is currently open. You can't count the votes yet.")
            else:
                print("Access Denied: You do not have the required admin level.")

        elif choice == "6":
            if admin.check_admin_privileges(4):
                election_manager = ElectionManager(db_service, encryption_service)
                location = input("Enter the location of the election you want to publish the results: ").strip()
                elections = db_service.get_elections_by_location(location)
                if not elections:
                    print(f"No elections found for location: {location}")
                    continue
               
                election_id = elections[0]["election_id"]
                result = election_manager.decrypt_results(election_id)
                if result:
                    print("Results are out!")
                else:
                    print(f"Error: Getting results failed for election_id={election_id}")
           
                election_id = elections[0]["election_id"]
                election_manager.view_results(election_id)
                user_id = admin.get_user_id()  
                action = f"Published results for election {election_id} at location {location}"
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                manager = AuditBookManager()
                log = AuditBook(auditlog_id = None, user_id=user_id, action=action, timestamp=timestamp)
                manager.create_log(log)
            else:
                print("Access Denied: You do not have the required admin level.")

        elif choice =="7":
            if admin.check_admin_privileges(5):
                audit_book = AuditBookManager()

                logs = audit_book.view_logs()
                if logs:
                    print("Audit Logs:")
                    for log in logs:
                        print(log)
                else:
                    print("No logs found!")
            else: 
                print("Access Denied: You do not have the required admin level.")
                
        elif choice == "8":
            admin.logout()
            print("User logged out successfully. Email and password have been reset.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

def voter_menu(voter: Voter):
    db_service = DatabaseService()
    election_manager = ElectionManager(db_service, encryption_service)

    while True:
        print("\n1. Vote")
        print("2. View Results")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            if election_manager.has_voter_voted(voter.get_user_id()):
                print("You already voted.")
                continue

            municipality = voter.get_municipality()
            province = voter.get_province()

            elections = db_service.get_all_elections()

            matched_elections = [
                election for election in elections
                if municipality.lower() in election["location"].lower() or province.lower() in election["location"].lower()
            ]

            if matched_elections:
                total_required_positions = 0  
                ballot = Ballot()
                last_position = None  
                election_voted = False

                for matched_election in matched_elections:
                    candidates = db_service.get_candidates_for_election(matched_election["election_id"])
                    if election_manager.is_election_open(matched_election["election_id"]):
                        if candidates:
                            grouped_candidates = election_manager.get_candidates_by_position(candidates)

                            total_required_positions += len(grouped_candidates)

                            last_position_in_election = list(grouped_candidates.keys())[-1]  
                            last_position = last_position_in_election if last_position is None else last_position

                            for position, candidate_list in grouped_candidates.items():
                                print(f"\n{position}")
                                for idx, (candidate_id, name) in enumerate(candidate_list, start=1):
                                    print(f"{idx}. {name}")
                                print(f"{len(candidate_list) + 1}. Void Vote")

                                while True:
                                    try:
                                        selected_idx = int(input(f"Select a candidate for {position}: ")) - 1
                                    
                                        if 0 <= selected_idx < len(candidate_list):
                                            selected_candidate_id = candidate_list[selected_idx][0]
                                
                                            election_id = db_service.get_election_id_by_candidate(selected_candidate_id)

                                            if election_id:
                                                vote = Vote(position, selected_candidate_id, election_id)
                                            else:
                                                print("Error: Election ID not found for this candidate.")
                                                continue
                                    
                                        elif selected_idx == len(candidate_list):
                                            if "election_id" in matched_election:    
                                                election_id = matched_election["election_id"] 
                                            vote = Vote(position, "VOID", election_id)  
                                        else:
                                            print("Invalid selection. Try again.")
                                            continue

                                        if voter.cast_vote(vote):  
                                            ballot.add_vote(vote)

                                            if position == last_position and ballot.is_complete(total_required_positions):
                                                election_voted = True
                                            break  
                                        else:
                                            print(f"Error: You have already voted for {position}.")
                                    except ValueError:
                                        print("Invalid input. Please enter a number.")
                        else:
                            print("No candidates available for this election.")
                    else:
                        print(f"Election is CLOSED or does not exist.")

                if election_voted:
                    confirm_submission = input("Do you want to submit your ballot? (yes/no): ").strip().lower()
                
                    if confirm_submission == "yes":

                        for vote in ballot.get_votes():
                            encrypted_vote = vote.get_encrypted_vote()
                        result1 =  election_manager.submit_ballot(ballot)
                        if result1 == True:
                            result2 = election_manager.get_voter_status(voter.get_user_id())
                        else:
                            print("Ballot submission failed.")
                    else:
                        print("Ballot submission canceled.")

                    if result1 and result2 == True:
                        print("Ballot submitted successfully!")
                    else:
                        print("Ballot submission failed.")

            else:
                print("\nNo elections found in your municipality and province.")

        elif choice == "2":
       
            location = input("Enter the location of the election you want to view the result: ").strip()
               
            elections = db_service.get_elections_by_location(location)
            if not elections:
                print(f"No elections found for location: {location}")
                continue
           
            election_id = elections[0]["election_id"]  
            election_manager.view_results(election_id)

        elif choice == "3":
            voter.logout()
            print("User logged out successfully. Email and password have been reset.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

def main():
    global current_user  
    while True:
        print("\n=== Menu ===")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":

            email = input("Enter Email: ")
            password = input("Enter Password: ")

            user = User.login(email, password)

            if user:
                user_id = user.get_user_id()

                if user.get_role() == "Voter":
                    voter = Voter(user_id)
                    voter_menu(voter)
                elif user.get_role() == "Admin":
                    admin = Admin(user_id)
                    admin_menu(admin)
           
            input("\nPress Enter to return to the menu")  

        elif choice == "2":  
            email = input("Enter Email: ").strip()
            name = input("Enter Name: ").strip()
            password = input("Enter Password: ").strip()
            province = input("Enter Province: ").strip()
            municipality = input("Enter Municipality: ").strip()

            if not all([email, name, password, province, municipality]):
                print("All fields are required to register!")
            else:
                voter = Voter(user_id=None, name=name, email=email, password=password, province=province, municipality=municipality)
                success = voter.register()

                if success:  
                    print("Registration successful")

            input("\nPress Enter to return to the menu")  

        elif choice == "3":
            print("Exiting program")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()