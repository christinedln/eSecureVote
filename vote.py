from database_service import DatabaseService
from Crypto.Cipher import AES
import base64
import json
import os

class Vote:
    _db_service = DatabaseService()
    _key = b'Sixteen byte key'  

    def __init__(self, position: str, candidate_id: str):
        self.__position = position  
        self.__candidate_id = candidate_id
        self.__encrypted_vote = self.__encrypt_vote() 

    def __encrypt_vote(self):
        """Encrypts the vote using AES."""
        vote_data = f"{self.__position}:{self.__candidate_id}"
        cipher = AES.new(self._key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(vote_data.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()
    
    def get_encrypted_vote(self) -> str:
        return self.__encrypted_vote
    
    def get_position(self) -> str:
        return self.__position
    
    def get_candidate_id(self) -> str:
        return self.__candidate_id

    @staticmethod
    def decrypt_vote(encrypted_vote: str) -> dict:
        """
        Decrypts a vote from its encrypted format.
        
        Args:
            encrypted_vote: The encrypted vote string
            
        Returns:
            A dictionary containing position and candidate_id
            
        Raises:
            ValueError: If decryption fails
        """
        try:
            # Decode from base64
            data = base64.b64decode(encrypted_vote)
            
            # Extract components (nonce is 16 bytes, tag is 16 bytes)
            nonce = data[:16]
            tag = data[16:32]
            ciphertext = data[32:]
            
            # Create cipher with same key and decrypt
            cipher = AES.new(Vote._key, AES.MODE_EAX, nonce=nonce)
            vote_data = cipher.decrypt_and_verify(ciphertext, tag).decode()
            
            # Split into position and candidate_id
            position, candidate_id = vote_data.split(":")
            
            return {
                "position": position,
                "candidate_id": candidate_id
            }
        except Exception as e:
            raise ValueError(f"Failed to decrypt vote: {str(e)}")