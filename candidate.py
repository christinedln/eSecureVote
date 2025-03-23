from utils import generate_candidate_id

class Candidate:
    def __init__(self, name: str, position: str, is_independent: bool, political_party: str, candidate_id: str = None):
        self.__name = name
        self.__position = position
        self.__is_independent = is_independent
        self.__political_party = political_party
        self.__candidate_id = candidate_id if candidate_id else generate_candidate_id()
        self.__vote_count = 0

    def get_name(self) -> str:
        return self.__name

    def get_position(self) -> str:
        return self.__position

    def set_name(self, name: str):
        self.__name = name

    def get_candidate_id(self) -> str:
        return self.__candidate_id

    def set_position(self, position: str):
        self.__position = position

    def get_is_independent(self) -> bool:
        return self.__is_independent
   
    def set_is_independent(self, is_independent: bool):
        self.__is_independent = is_independent
   
    def get_political_party(self) -> str:
        return self.__political_party

    def set_political_party(self, political_party: str):
        self.__political_party = political_party

    def get_vote_count(self) -> int:
        return self.__vote_count

    def increment_vote_count(self):
        self.__vote_count += 1