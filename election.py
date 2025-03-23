from utils import generate_election_id
from candidate import Candidate
from database_service import DatabaseService

class Election:
    def __init__(self, election_id: str = None, date: str = None, time: str = None, location: str = "", is_open: bool = False):
        self.__election_id = election_id if election_id else generate_election_id()
        self.__date = date
        self.__time = time
        self.__location = location
        self.__is_open = is_open

    def get_election_id(self) -> str:
        return self.__election_id

    def get_date(self) -> str:
        return self.__date

    def get_time(self) -> str:
        return self.__time

    def get_location(self) -> str:
        return self.__location

    def get_is_open(self) -> bool:
        return self.__is_open

    def set_date(self, election_date: str):
        self.__date = election_date

    def set_time(self, election_time: str):
        self.__time = election_time

    def set_location(self, location: str):
        self.__location = location

    def set_is_open(self, is_open: bool):
        self.__is_open = is_open

    def create_election(self):
        db_service = DatabaseService()
        election_data = {
            "election_id": self.__election_id,
            "date": self.__date,
            "time": self.__time,
            "location": self.__location,
            "is_open": self.__is_open
        }
        db_service.save_election(election_data)

    def add_candidate(self, election_id, candidate: Candidate):
        db_service = DatabaseService()
        candidate_data = {
            "candidate_id": candidate.get_candidate_id(),
            "name": candidate.get_name(),
            "position": candidate.get_position(),
            "is_independent": candidate.get_is_independent(),
            "political_party": candidate.get_political_party(),
        }
        db_service.save_candidate(election_id, candidate_data)
