from database_service import DatabaseService
from encryption_service import EncryptionService  

class Vote:
    _db_service = DatabaseService()
    encryption_service = EncryptionService()  

    def __init__(self, position: str = None, candidate_id: str = None, election_id: str = None):
        if position and candidate_id and election_id:
            self.__position = position
            self.__candidate_id = candidate_id
            self.__election_id = election_id
            self.__encrypted_vote = self.encrypt_vote()
            self.__decrypted_vote = None

    def set_encrypted_vote(self, encrypted_vote: str):
        self.__encrypted_vote = encrypted_vote
        self.__decrypted_vote = self.decrypt_vote()

    def encrypt_vote(self):
        vote_data = f"{self.__position}:{self.__candidate_id}"
        return self.encryption_service.encrypt_vote(vote_data)  
    
    def decrypt_vote(self):
        if not self.__encrypted_vote:
            raise ValueError("Encrypted vote is not set!")
        return self.encryption_service.decrypt_vote(self.__encrypted_vote)  

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
