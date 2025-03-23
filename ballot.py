from database_service import DatabaseService
from vote import Vote
from encryption_service import EncryptionService
from utils import generate_ballot_id

class Ballot:
    _db_service = DatabaseService()
    _encryption_service = EncryptionService()

    def __init__(self, ballot_id: str = None):
        self.__ballot_id = ballot_id if ballot_id else generate_ballot_id()
        self.__votes = []  
        self.__encrypted_ballot_id = self._encryption_service.encrypt_ballot_id(self.__ballot_id)

    def add_vote(self, vote: Vote):
        self.__votes.append(vote)

    def is_complete(self, required_positions: int) -> bool:
        return len(self.__votes) == required_positions

    def get_ballot_id(self) -> str:
        return self.__ballot_id

    def get_votes(self) -> list:
        return self.__votes

    def get_encrypted_ballot_id(self) -> str:
        return self.__encrypted_ballot_id
   
    def get_decrypt_ballot_id(self, encrypted_ballot_id: str) -> str:
        return self._encryption_service.decrypt_ballot_id(encrypted_ballot_id)
