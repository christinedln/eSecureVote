from admin import Admin
from database_service import DatabaseService
from election import Election  
from candidate import Candidate
from voter import Voter
from ballot import Ballot
from vote import Vote


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

def voter_menu(voter: Voter): 
    db_service = DatabaseService()
    election = Election()

    while True:
        print("\n1. Vote")
        print("2. View Results")
        print("3. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            if election.has_voter_voted(voter.get_user_id()):
                print("You already voted.")
                continue

            municipality = voter.get_municipality()
            province = voter.get_province()

            print(f"[DEBUG] Voter location - Municipality: {municipality}, Province: {province}")

            elections = db_service.get_all_elections()
            print(f"[DEBUG] Retrieved {len(elections)} elections from database.")

            matched_elections = [
                election for election in elections
                if municipality.lower() in election["location"].lower() or province.lower() in election["location"].lower()
            ]

            print(f"[DEBUG] Found {len(matched_elections)} matching elections.")

            if matched_elections:
                total_required_positions = 0  
                ballot = Ballot() 
                last_position = None  
                election_voted = False

                for matched_election in matched_elections:
                    print(f"[DEBUG] Processing election: {matched_election['election_id']}")
                    candidates = db_service.get_candidates_for_election(matched_election["election_id"])

                    if candidates:
                        grouped_candidates = ballot.get_candidates_by_position(candidates)
                        print(f"[DEBUG] Found {len(grouped_candidates)} positions in election.")

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
                                        vote = Vote(position, selected_candidate_id)
                                    elif selected_idx == len(candidate_list):
                                        vote = Vote(position, "VOID")
                                    else:
                                        print("Invalid selection. Try again.")
                                        continue

                                    print(f"[DEBUG] Voter selected - Position: {position}, Candidate ID: {vote.get_candidate_id()}")

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
                if election_voted:
                    print("You have completed voting for all positions.")
                    confirm_submission = input("Do you want to submit your ballot? (yes/no): ").strip().lower()
                    print(f"[DEBUG] Submission confirmation: {confirm_submission}")
                    
                    if confirm_submission == "yes":
                        print("\n[DEBUG] Submitting the ballot...\n")

                        for vote in ballot.get_votes():
                            encrypted_vote = vote.get_encrypted_vote()

                            print(f"Encrypted Vote: {encrypted_vote}")

                        print(f"\nYour ballot has been submitted and encrypted.")
                        election.submit_ballot(ballot)
                    else:
                        print("Ballot submission canceled.")

            else:
                print("\nNo elections found in your municipality and province.")

        elif choice == "2":
            print("Viewing results...")

        elif choice == "3":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please select a valid option.")
def main():
    
    user_id = "usid01"
    voter = Voter(user_id) 
    voter_menu(voter)
    

    """
    user_id =  "usid02"
    admin = Admin(user_id) 
    admin_menu(admin)
    """

if __name__ == "__main__":
    main()
