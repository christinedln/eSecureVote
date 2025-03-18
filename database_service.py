import firebase_admin
from firebase_admin import credentials, firestore

class DatabaseService:
    def __init__(self):
        if not firebase_admin._apps:  
            cred = credentials.Certificate(r"C:\Users\Christine Joyce\Desktop\eSecureVote\config\FirebaseConfig.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def save_election(self, election_data: dict):
        elections_ref = self.db.collection("Elections")

        election_id = election_data.pop("election_id", None) 
        if not election_id:
            raise ValueError("Election ID is missing from the election data.")

        elections_ref.document(election_id).set(election_data)

    def save_candidate(self, election_id: str, candidate_data: dict):
        elections_ref = self.db.collection("Elections").document(election_id)
        candidates_ref = elections_ref.collection("Candidates")  
        all_candidates_ref = self.db.collection("Candidates")  

        candidate_id = candidate_data.pop("candidate_id", None)
        if not candidate_id:
            raise ValueError("Candidate ID is missing from the candidate data.")

        candidates_ref.document(candidate_id).set(candidate_data)

        candidate_data["election_id"] = election_id  

        all_candidates_ref.document(candidate_id).set(candidate_data)

    def get_user_data(self, user_id: int):
        user_doc = self.db.collection("Users").document(str(user_id)).get()
        return user_doc.to_dict() if user_doc.exists else None

    def get_admin_level(self, user_id: int):
        user_data = self.get_user_data(user_id)
        if user_data and user_data.get("role") == "Admin":
            return user_data.get("adminLevel")
        return None  
    
    def get_last_election(self):

        try:
            elections_ref = self.db.collection("Elections").get() 
            if elections_ref:
                last_election = elections_ref[-1] 
                election_data = {"election_id": last_election.id, **last_election.to_dict()}
                return election_data  

        except Exception as e:
            print(f"Error fetching last election: {e}") 

        print("No elections found in the database.") 

        return None
    
    def get_last_candidate(self):
        try:
            candidates_ref = self.db.collection("Candidates").get() 
            if candidates_ref:
                last_candidate = candidates_ref[-1] 
                candidate_data = {"candidate_id": last_candidate.id, **last_candidate.to_dict()}
                return candidate_data  

        except Exception as e:
            print(f"Error fetching last candidate: {e}") 

        return None
    
    def get_last_ballot(self):
        try:
            ballots_ref = self.db.collection("Ballots").get() 
            if ballots_ref:
                last_ballot = ballots_ref[-1] 
                ballot_data = {"ballot_id": last_ballot.id, **last_ballot.to_dict()}
                return ballot_data  

        except Exception as e:
            print(f"Error fetching last ballot: {e}") 

        return None
    
    def get_all_elections(self):
        """Fetch all elections from the database and print the results."""
        try:
            elections_ref = self.db.collection("Elections").get() 
            election_list = []

            for doc in elections_ref:
                election_data = {"election_id": doc.id, **doc.to_dict()}
                election_list.append(election_data)

            return election_list

        except Exception as e:
            print(f"Error fetching elections: {e}")
            return []

    def set_election_status_to_open(self, election_id: str, is_open: bool):
        elections_ref = self.db.collection("Elections").document(election_id)
    
        if elections_ref.get().exists:
            elections_ref.update({"is_open": is_open})

    def set_election_status_to_close(self, election_id: str, is_open: bool):
        elections_ref = self.db.collection("Elections").document(election_id)
    
        if elections_ref.get().exists:
            elections_ref.update({"is_open": is_open})

    def get_candidates_for_election(self, election_id: str):
        try:
            candidates_ref = self.db.collection("Elections").document(election_id).collection("Candidates").get()
            candidates_list = []

            for doc in candidates_ref:
                candidate_data = {"candidate_id": doc.id, **doc.to_dict()}
                candidates_list.append(candidate_data)

            return candidates_list  

        except Exception as e:
            print(f"Error fetching candidates for election {election_id}: {e}")
            return []
        
    def get_voter_vote_status(self, user_id: str):
        voter_doc = self.db.collection("Users").document(user_id).get()
        if voter_doc.exists:
            return voter_doc.to_dict()
        return None
    
    def record_encrypted_ballot(self, ballot_id: str, encrypted_votes: list):
        """Stores the encrypted ballot and its votes in the database."""
        try:
            ballot_data = {
                "encrypted_votes": encrypted_votes,
            }

            self.db.collection("Ballots").document(ballot_id).set(ballot_data)

            print(f"[SUCCESS] Encrypted ballot recorded with ID: {ballot_id}")

        except Exception as e:
            print(f"[ERROR] Failed to record encrypted ballot: {e}")