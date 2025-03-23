from database_service import DatabaseService
from encryption_service import EncryptionService
from ballot import Ballot
from vote import Vote
import json

class ElectionManager:
    def __init__(self, db_service: DatabaseService, encryption_service: EncryptionService):
        self._db_service = db_service
        self._encryption_service = encryption_service
        self.__candidates = {}  
        self.__void_votes = []

    def start_election(self, election_id: str):
        self._db_service.set_election_status_to_open(election_id, True)

    def close_election(self, election_id: str):
        self._db_service.set_election_status_to_close(election_id, False)

    def has_voter_voted(self, user_id: str) -> bool:
        vote_record = self._db_service.get_voter_vote_status(user_id)
        return vote_record is not None and vote_record.get("has_voted", False)
    
    def get_voter_status(self, user_id: str) -> bool:
        return self.__record_voter(user_id)

    def __record_voter(self, user_id: str) -> bool:
        return self._db_service.set_voter_status(user_id)

    def submit_ballot(self, ballot: Ballot):
        ballot_id = ballot.get_encrypted_ballot_id()
        encrypted_votes = [vote.get_encrypted_vote() for vote in ballot.get_votes()]
        self._db_service.record_encrypted_ballot(ballot_id, encrypted_votes)

    def count_votes(self, election_id: str, decrypted_vote: str):
        vote_info = decrypted_vote.split(":")
        if len(vote_info) == 2:
            position, candidate_id = vote_info
            if candidate_id == "VOID":
                self._db_service.increment_void_votes(election_id)
            else:
                self._db_service.update_candidate_vote_count(election_id, candidate_id)

    def encrypt_result(self, election_id: str):
        highest_votes = self._db_service.get_highest_vote(election_id)
        result_json = json.dumps(highest_votes)
        encrypted_result = self._encryption_service.encrypt_result(result_json)
        self._db_service.store_encrypted_result(election_id, encrypted_result)

    def decrypt_results(self, election_id: str):
        encrypted_data = self._db_service.get_encrypted_results(election_id)
        decrypted_result = self._encryption_service.decrypt_result(encrypted_data)
        self._db_service.store_result(decrypted_result, election_id)

    def view_results(self, election_id: str):
        results = self._db_service.get_election_result(election_id)
        print(results)
        return results
    
    def __retrieve_decrypted_ballots(self, election_id: str, encrypted_ballots: list):
        for encrypted_ballot in encrypted_ballots:
            encrypted_ballot_id = encrypted_ballot['ballot_id']
            encrypted_vote = encrypted_ballot['encrypted_vote']
            ballot = Ballot()
            decrypted_ballot_id = ballot.get_decrypt_ballot_id(encrypted_ballot_id)
            vote = Vote()
            vote.set_encrypted_vote(encrypted_vote)
            decrypted_vote = vote.get_decrypted_vote()
            self.count_votes(election_id, decrypted_vote)
   
    def get_decrypted_ballots(self, election_id: str, encrypted_ballots: list):
        return self.__retrieve_decrypted_ballots(election_id, encrypted_ballots)
   
    def count_votes(self, election_id:str, decrypted_vote: str):
        vote_info = decrypted_vote.split(":")
        if len(vote_info) == 2:
            position, candidate_id = vote_info
            if candidate_id == "VOID":
       
                self.__void_votes.append(decrypted_vote)
            else:
                if candidate_id not in self.__candidates:
                    self.__candidates[candidate_id] = 0
                self.__candidates[candidate_id] += 1
                self._db_service.update_candidate_vote_count(election_id, candidate_id, self.__candidates[candidate_id])

        else:
            print(f"Invalid vote format")
    
    def get_candidates_by_position(self, candidates: list):
        grouped_candidates = {}
        for candidate in candidates:
            position = candidate["position"]
            if position not in grouped_candidates:
                grouped_candidates[position] = []
            grouped_candidates[position].append((candidate["candidate_id"], candidate["name"]))
        return grouped_candidates
    
    def is_election_open(self, election_id: str) -> bool:
        election_data = self._db_service.get_election_by_id(election_id)
        if election_data:
            return election_data.get("is_open", False)
        return False