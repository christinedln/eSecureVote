from database_service import DatabaseService
from Crypto.Cipher import AES
import base64


class Vote:
    _db_service = DatabaseService()  
    _key = b'Sixteen byte key'  


    def __init__(self, position: str = None, candidate_id: str = None, election_id: str = None):
        if position and candidate_id and election_id:
            self.__position = position
            self.__candidate_id = candidate_id
            self.__election_id = election_id
            self.__encrypted_vote = self.__encrypt_vote()
            self.__decrypted_vote = None


    def set_encrypted_vote(self, encrypted_vote: str):
        self.__encrypted_vote = encrypted_vote
        self.__decrypted_vote = self.__decrypt_vote()


    def __encrypt_vote(self):
        vote_data = f"{self.__position}:{self.__candidate_id}"
        cipher = AES.new(self._key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(vote_data.encode())
        return base64.b64encode(cipher.nonce + tag + ciphertext).decode()


    def __decrypt_vote(self):
        if not self.__encrypted_vote:
            raise ValueError("Encrypted vote is not set!")
       
        encrypted_data = base64.b64decode(self.__encrypted_vote)
       
        nonce = encrypted_data[:16]  
        tag = encrypted_data[16:32]  
        ciphertext = encrypted_data[32:]


        cipher = AES.new(self._key, AES.MODE_EAX, nonce=nonce)
        decrypted_vote = cipher.decrypt_and_verify(ciphertext, tag).decode('utf-8')


        return decrypted_vote


    def get_encrypted_vote(self) -> str:
        return f"{self.__encrypted_vote} - {self.__election_id}"
   
    def get_decrypted_vote(self) -> str:
        if not self.__decrypted_vote:
            raise ValueError("Decrypted vote is not available. Please set the encrypted vote first.")
        return self.__decrypted_vote


    def get_election_id(self) -> str:
        return self.__election_id
   
    def get_position(self) -> str:
        return self.__position
   
    def get_candidate_id(self) -> str:
        return self.__candidate_id

