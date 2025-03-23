from database_service import DatabaseService
from vote import Vote
from encryption_service import EncryptionService

class Ballot:
    _db_service = DatabaseService()
    _encryption_service = EncryptionService()

    def __init__(self, ballot_id: str = None):
        self.__ballot_id = ballot_id if ballot_id else self.__generate_ballot_id()
        self.__votes = []  
        self.__encrypted_ballot_id = self._encryption_service.encrypt(self.__ballot_id)

    def __generate_ballot_id(self) -> str:
        last_ballot = self._db_service.get_last_ballot()

        if last_ballot:
            last_id = last_ballot["ballot_id"]
            if last_id.startswith("baid") and last_id[4:].isdigit():
                return f"baid{int(last_id[4:]) + 1:02d}"  

        return "baid01"  

    def add_vote(self, vote: Vote):
        self.__votes.append(vote)

    def is_complete(self, required_positions: int) -> bool:
        return len(self.__votes) == required_positions
   
    def get_candidates_by_position(self, candidates: list):
        grouped_candidates = {}
        for candidate in candidates:
            position = candidate["position"]
            if position not in grouped_candidates:
                grouped_candidates[position] = []
            grouped_candidates[position].append((candidate["candidate_id"], candidate["name"]))
        return grouped_candidates

    def get_ballot_id(self) -> str:
        return self.__ballot_id

    def get_votes(self) -> list:
        return self.__votes

    def get_encrypted_ballot_id(self) -> str:
        return self.__encrypted_ballot_id
   
    def get_decrypt_ballot_id(self, encrypted_ballot_id: str) -> str:
        return self._encryption_service.decrypt(encrypted_ballot_id)
