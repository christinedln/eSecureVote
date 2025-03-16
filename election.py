from database_service import DatabaseService
from candidate import Candidate

class Election:
    def __init__(self, election_id: str = None, election_date: str = None, election_time: str = None, location: str = "", is_open: bool = False):
        self.__election_id = election_id if election_id else self.__generate_election_id()
        self.__election_date = election_date
        self.__election_time = election_time
        self.__election_location = location
        self.__is_open = is_open

    def __generate_election_id(self) -> str:

        db_service = DatabaseService()
        last_election = db_service.get_last_election()

        if last_election:
            last_id = last_election["election_id"]

            if last_id.startswith("elid") and last_id[4:].isdigit():
                num = int(last_id[4:]) + 1  
                new_id = f"elid{num:02d}"

                return new_id  

        return "elid01"
    
    def get_election_id(self) -> str:
        return self.__election_id

    def get_date(self) -> str:
        return self.__election_date

    def get_time(self) -> str:
        return self.__election_time

    def get_location(self) -> str:
        return self.__election_location

    def set_date(self, election_date: str):
        self.__election_date = election_date

    def set_time(self, election_time: str):
        self.__election_time = election_time

    def set_location(self, location: str):
        self.__election_location = location

    def get_is_open(self) -> bool:
        return self.__is_open

    def set_is_open(self, is_open: bool):
        self.__is_open = is_open

    def add_candidate(self, election_id: str, candidate: Candidate):
        db_service = DatabaseService()
        candidate_data = {
            "candidate_id" : candidate.get_candidate_id(),
            "name": candidate.get_name(),
            "position": candidate.get_position(),
            "is_independent": candidate.get_is_independent(),
            "political_party": candidate.get_political_party()
        }
        db_service.save_candidate(election_id, candidate_data)

    @staticmethod
    def start_election(election_id: str):
        db_service = DatabaseService()
        db_service.set_election_status_to_open(election_id, True)

    @staticmethod
    def close_election(election_id: str):
        db_service = DatabaseService()
        db_service.set_election_status_to_close(election_id, False)
