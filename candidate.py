from database_service import DatabaseService
class Candidate:
    def __init__(self, name: str, position: str, is_independent: bool, political_party: str, candidate_id: str = None):
        self.__name = name
        self.__position = position
        self.__is_independent = is_independent
        self.__political_party = political_party
        self.__candidate_id = candidate_id if candidate_id else self.__generate_candidate_id()
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


    def __generate_candidate_id(self) -> str:
        db_service = DatabaseService()
        last_candidate = db_service.get_last_candidate()


        if last_candidate:
            last_id = last_candidate["candidate_id"]
            if last_id.startswith("caid") and last_id[4:].isdigit():
                num = int(last_id[4:]) + 1
                new_id = f"caid{num:02d}"
                return new_id


        return "caid01"

