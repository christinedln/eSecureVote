import firebase_admin
from firebase_admin import credentials, firestore
import json


class DatabaseService:
    def __init__(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate(r"C:\Users\Christine Joyce\Desktop\eSecureVote\config\FirebaseConfig.json")
            firebase_admin.initialize_app(cred)
        self.db = firestore.client()


    def get_user_by_email(self, email: str):
        users_ref = self.db.collection("Users").where("email", "==", email).stream()
        users = list(users_ref)
        if not users:
            return None
        user_doc = users[0]
        user_data = user_doc.to_dict()
        user_data["user_id"] = user_doc.id
        user_data.setdefault("face_recog", False)
        return user_data


    def check_existing_user(self, email: str) -> bool:
        return any(self.db.collection("Users").where("email", "==", email).stream())


    def check_registered_voter(self, email: str) -> bool:
        return any(self.db.collection("registered_voters").where("email", "==", email).stream())


    def add_new_user(self, user_id: str, user_data: dict):
        user_data.setdefault("face_recog", False)
        self.db.collection("Users").document(user_id).set(user_data)


    def update_user_profile(self, user_id: str, updated_data: dict):
        self.db.collection("Users").document(user_id).update(updated_data)


    def update_user_face_recog(self, user_id: str, status: bool):
        self.db.collection("Users").document(user_id).update({"face_recog": status})


    def save_election(self, election_data: dict):
        elections_ref = self.db.collection("Elections")
        election_id = election_data.pop("election_id", None)
        if not election_id:
            raise ValueError("Election ID is missing from the election data.")
        elections_ref.document(election_id).set(election_data)


    def save_log(self, audit_data):
        audit_data_ref = self.db.collection("AuditBook")
        auditlog_id = audit_data.pop("auditlog_id", None)
        if not auditlog_id:
            raise ValueError("Election ID is missing from the election data.")
        audit_data_ref.document(auditlog_id).set(audit_data)


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
        return user_data.get("adminLevel") if user_data and user_data.get("role") == "Admin" else None


    def get_last_document(self, collection_name: str, doc_id_key: str):
        try:
            docs_ref = self.db.collection(collection_name).get()
            if docs_ref:
                last_doc = docs_ref[-1]
                return {doc_id_key: last_doc.id, **last_doc.to_dict()}
        except Exception as e:
            print(f"Error fetching last document from {collection_name}: {e}")
        return None


    def get_last_election(self):
        return self.get_last_document("Elections", "election_id")
   
    def get_last_auditlog(self):
        return self.get_last_document("AuditBook", "auditlog_id")
   
    def get_last_user_id(self):
        return self.get_last_document("Users", "user_id")


    def get_last_candidate(self):
        return self.get_last_document("Candidates", "candidate_id")


    def get_last_ballot(self):
        return self.get_last_document("Ballots", "ballot_id")


    def get_all_elections(self):
        try:
            return [{"election_id": doc.id, **doc.to_dict()} for doc in self.db.collection("Elections").get()]
        except Exception as e:
            print(f"Error fetching elections: {e}")
            return []
       
    def get_election_id_by_candidate(self, candidate_id):
        candidates_ref = self.db.collection("Candidates").document(candidate_id)
        candidate_doc = candidates_ref.get()


        if candidate_doc.exists:
            return candidate_doc.to_dict().get("election_id")
        return None  




    def set_election_status_to_open(self, election_id: str, is_open: bool):
        elections_ref = self.db.collection("Elections").document(election_id)
   
        if elections_ref.get().exists:
            elections_ref.update({"is_open": is_open})


    def set_election_status_to_close(self, election_id: str, is_open: bool):
        elections_ref = self.db.collection("Elections").document(election_id)
   
        if elections_ref.get().exists:
            elections_ref.update({"is_open": is_open})


    def set_voter_status(self, user_id: str):
        user_ref = self.db.collection("Users").document(user_id)




        if user_ref.get().exists:
            user_ref.update({"has_voted": True})
            return True
        return False


    def get_candidates_for_election(self, election_id: str):
        try:
            return [{"candidate_id": doc.id, **doc.to_dict()} for doc in self.db.collection("Elections").document(election_id).collection("Candidates").get()]
        except Exception as e:
            print(f"Error fetching candidates for election {election_id}: {e}")
            return []


    def get_voter_vote_status(self, user_id: str):
        voter_doc = self.db.collection("Users").document(user_id).get()
        return voter_doc.to_dict() if voter_doc.exists else None


    def record_encrypted_ballot(self, ballot_id: str, encrypted_votes: list):
        try:
            self.db.collection("Ballots").document(ballot_id).set({"encrypted_votes": encrypted_votes})
        except Exception as e:
            print(f"[ERROR] Failed to record encrypted ballot: {e}")


    def get_all_encrypted_ballots(self, election_id: str):
        try:
            ballots_ref = self.db.collection("Ballots").stream()
            encrypted_ballots = []


            for doc in ballots_ref:
                ballot_data = doc.to_dict()
                if "encrypted_votes" in ballot_data:
                    for encrypted_vote in ballot_data["encrypted_votes"]:
                        vote_data, vote_election_id = encrypted_vote.rsplit(" - ", 1)


                        if vote_election_id == election_id:
                            encrypted_ballots.append({
                                "ballot_id": doc.id,
                                "encrypted_vote": vote_data
                            })


            return encrypted_ballots


        except Exception as e:
            print(f"Error fetching encrypted ballots: {e}")
            return []


    def get_elections_by_location(self, location: str):
        try:
            elections_ref = self.db.collection("Elections")
            query = elections_ref.where("location", "==", location).stream()


            elections = [{"election_id": doc.id, **doc.to_dict()} for doc in query]
            return elections


        except Exception as e:
            print(f"Error fetching elections by location: {e}")
            return []


    def update_candidate_vote_count(self, election_id: str, candidate_id: str, vote_count: int):


        if not isinstance(vote_count, int):
            vote_count = 0


        candidate_ref_main = self.db.collection('Candidates').document(candidate_id)
        candidate_doc_main = candidate_ref_main.get()


        candidate_ref_election = self.db.collection('Elections').document(election_id).collection('Candidates').document(candidate_id)
        candidate_doc_election = candidate_ref_election.get()


        if candidate_doc_main.exists:
            candidate_ref_main.update({'vote_count': vote_count})
        else:
            candidate_ref_main.set({'vote_count': vote_count})


        if candidate_doc_election.exists:
            candidate_ref_election.update({'vote_count': vote_count})
        else:
            candidate_ref_election.set({'vote_count': vote_count})


    def get_highest_vote(self, election_id: str):
        try:
            election_ref = self.db.collection('Elections').document(election_id)
            election_doc = election_ref.get()


            if not election_doc.exists:
                return None


            candidates_ref = election_ref.collection('Candidates')
            candidates_docs = candidates_ref.stream()


            highest_votes = {}


            for candidate_doc in candidates_docs:
                candidate_data = candidate_doc.to_dict()
                candidate_name = candidate_data.get('name')
                position = candidate_data.get('position')
                votes = candidate_data.get('vote_count', 0)  


                if position not in highest_votes or votes > highest_votes[position]['vote_count']:
                    highest_votes[position] = {
                        'candidate_name': candidate_name,
                        'vote_count': votes
                    }


            return highest_votes


        except Exception as e:
            print(f"Error fetching election results: {e}")
            return None
       
    def store_encrypted_result(self, election_id: str, encrypted_result: str):
        election_ref = self.db.collection('Elections').document(election_id)
        election_ref.set({
            'encrypted_result': encrypted_result
        }, merge=True)


    def get_encrypted_results(self, election_id: str):
        election_ref = self.db.collection('Elections').document(election_id)
       
        election_doc = election_ref.get()
       
        if election_doc.exists:
 
            encrypted_result = election_doc.to_dict().get('encrypted_result')
           
            if encrypted_result:
                return encrypted_result
            else:
                return None
        else:
            return None
   
    def store_result(self, json_data, election_id):


        result_data = json.loads(json_data)


        collection_ref = self.db.collection('Results')


        doc_ref = collection_ref.document(election_id)
        doc_ref.set(result_data)


    def get_election_result(self, election_id: str):


        collection_ref = self.db.collection('Results')


        doc_ref = collection_ref.document(election_id)
        doc = doc_ref.get()


        if doc.exists:


            result_dict = doc.to_dict()


            result_string = ""
            for position, details in result_dict.items():
                result_string += f"{position}:\n"
                for key, value in details.items():
                    result_string += f"  {key}: {value}\n"
                result_string += "\n"  


            return result_string.strip()
        else:
            return None

