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