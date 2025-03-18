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
    
    @classmethod
    def decrypt_ballot_id(cls, encrypted_ballot_id: str) -> str:
        """Decrypts an encrypted ballot ID back to its original form."""
        try:
            # Add padding if needed
            padded_encrypted_id = encrypted_ballot_id + '=' * (-len(encrypted_ballot_id) % 4)
            
            # Decode the base64 encrypted data
            encrypted_data = base64.urlsafe_b64decode(padded_encrypted_id)
            
            # Extract nonce, tag and ciphertext
            nonce = encrypted_data[:16]  # First 16 bytes are the nonce
            tag = encrypted_data[16:32]  # Next 16 bytes are the tag
            ciphertext = encrypted_data[32:]  # Rest is the ciphertext
            
            # Create a cipher using the nonce and key
            cipher = AES.new(cls._key, AES.MODE_EAX, nonce=nonce)
            
            # Decrypt and verify the data
            ballot_id = cipher.decrypt_and_verify(ciphertext, tag)
            
            return ballot_id.decode()
        except Exception as e:
            print(f"Error decrypting ballot ID: {e}")
            return None
    
    def count_votes(self) -> dict:
        """
        Counts votes by position and candidate ID.
        
        Returns:
            dict: A dictionary with positions as keys and dicts of candidate_id:count as values
        """
        vote_counts = {}
        
        for vote in self.__votes:
            position = vote.get_position()
            candidate_id = vote.get_candidate_id()
            
            if position not in vote_counts:
                vote_counts[position] = {}
                
            if candidate_id not in vote_counts[position]:
                vote_counts[position][candidate_id] = 0
                
            vote_counts[position][candidate_id] += 1
            
        return vote_counts
    
    def encrypt_result(self, result: dict) -> str:
        """
        Encrypts the voting result using AES.
        
        Args:
            result (dict): Vote count results to encrypt
            
        Returns:
            str: Encrypted result as a base64 string
        """
        # Convert result to JSON string
        result_json = json.dumps(result)
        
        # Create new cipher
        cipher = AES.new(self._key, AES.MODE_EAX)
        
        # Encrypt the result
        ciphertext, tag = cipher.encrypt_and_digest(result_json.encode())
        
        # Combine nonce, tag, and ciphertext and encode as base64
        encrypted_data = cipher.nonce + tag + ciphertext
        encrypted_result = base64.urlsafe_b64encode(encrypted_data).decode().rstrip("=")
        
        return encrypted_result
