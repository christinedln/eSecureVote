from database_service import DatabaseService
from vote import Vote
import hashlib
import json
from Crypto.Cipher import AES
import base64

class Ballot:
    __db_service = DatabaseService()  
    _key = b'Sixteen byte key'

    def __init__(self, ballot_id: str = None):
        self.__ballot_id = ballot_id if ballot_id else self.__generate_ballot_id()
        self.__votes = []  
        self.__encrypted_ballot_id = self.__encrypt_ballot_id(self.__ballot_id)

    def __generate_ballot_id(self) -> str:
        last_ballot = self.__db_service.get_last_ballot()

        if last_ballot:
            last_id = last_ballot["ballot_id"]
            if last_id.startswith("baid") and last_id[4:].isdigit():
                return f"baid{int(last_id[4:]) + 1:02d}"  

        return "baid01"  

    def add_vote(self, vote: Vote):
        self.__votes.append(vote)

    def is_complete(self, required_positions: int) -> bool:
        """Checks if all positions have been voted for."""
        return len(self.__votes) == required_positions
    
    def get_candidates_by_position(self, candidates: list):
        """Groups candidates by position."""
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
    
    def __encrypt_ballot_id(self, ballot_id: str) -> str:
        """Encrypts the ballot ID using AES and encodes it in a Firestore-safe format."""
        cipher = AES.new(self._key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(ballot_id.encode())

        encrypted_data = cipher.nonce + tag + ciphertext

        return base64.urlsafe_b64encode(encrypted_data).decode().rstrip("=")
        
    def get_encrypted_ballot_id(self) -> str:
        """Returns the encrypted ballot ID."""
        return self.__encrypted_ballot_id
