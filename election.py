from database_service import DatabaseService
from candidate import Candidate
from ballot import Ballot
from vote import Vote
from utils import generate_election_id
from encryption_service import EncryptionService
from Crypto.Cipher import AES
import json
import base64

class Election:
    _db_service = DatabaseService()  
    _encryption_service = EncryptionService()

    def __init__(self, election_id: str = None, election_date: str = None, election_time: str = None, location: str = "", is_open: bool = False):
        self.__election_id = election_id if election_id else generate_election_id()
        self.__election_date = election_date
        self.__election_time = election_time
        self.__election_location = location
        self.__is_open = is_open
        self.__candidates = {}  
        self.__void_votes = []  

    def get_election_id(self) -> str:
        return self.__election_id

    def get_date(self) -> str:
        return self.__election_date

    def get_time(self) -> str:
        return self.__election_time

    def get_location(self) -> str:
        return self.__election_location

    def get_is_open(self) -> bool:
        return self.__is_open

    def set_date(self, election_date: str):
        self.__election_date = election_date

    def set_time(self, election_time: str):
        self.__election_time = election_time

    def set_location(self, location: str):
        self.__election_location = location

    def set_is_open(self, is_open: bool):
        self.__is_open = is_open

    def is_election_open(self, election_id: str) -> bool:
        election_data = self._db_service.get_election_by_id(election_id)
        if election_data:
            return election_data.get("is_open", False)
        return False

    @classmethod
    def start_election(cls, election_id: str):
        cls._db_service.set_election_status_to_open(election_id, True)

    @classmethod
    def close_election(cls, election_id: str):
        cls._db_service.set_election_status_to_close(election_id, False)

    @classmethod
    def has_voter_voted(cls, user_id: str) -> bool:
        vote_record = cls._db_service.get_voter_vote_status(user_id)
        return vote_record is not None and vote_record.get("has_voted", False)
   
    @classmethod
    def __record_voter(cls, user_id: str) -> bool:
        return cls._db_service.set_voter_status(user_id)
   
    def get_voter_status(self, user_id: str) -> bool:
        return self.__record_voter(user_id)
   
    def add_candidate(self, election_id: str, candidate: Candidate):
        candidate_data = {
            "candidate_id": candidate.get_candidate_id(),
            "name": candidate.get_name(),
            "position": candidate.get_position(),
            "is_independent": candidate.get_is_independent(),
            "political_party": candidate.get_political_party(),
        }
        self._db_service.save_candidate(election_id, candidate_data)
   
    def submit_ballot(self, ballot: Ballot):

        ballot_id = ballot.get_encrypted_ballot_id()
        encrypted_votes = [vote.get_encrypted_vote() for vote in ballot.get_votes()]  

        self._db_service.record_encrypted_ballot(ballot_id,  encrypted_votes)
   
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

    def encrypt_result(self, election_id: str):
        highest_votes = self._db_service.get_highest_vote(election_id)
        result_json = json.dumps(highest_votes)
        encrypted_result = self._encryption_service.encrypt_result(result_json)
        self._db_service.store_encrypted_result(election_id, encrypted_result)
   
    def decrypt_results(self, election_id:str):
        encrypted_data = self._db_service.get_encrypted_results(election_id)
        decrypted_result = self._encryption_service.decrypt_result(encrypted_data)
        self._db_service.store_result(decrypted_result, election_id)

    def view_results(self, election_id:str):
        results = self._db_service.get_election_result(election_id)
        print(results)
        return results