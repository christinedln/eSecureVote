from database_service import DatabaseService
from candidate import Candidate
from ballot import Ballot

class Election:
    _db_service = DatabaseService()  

    def __init__(self, election_id: str = None, election_date: str = None, election_time: str = None, location: str = "", is_open: bool = False):
        self.__election_id = election_id if election_id else self.__generate_election_id()
        self.__election_date = election_date
        self.__election_time = election_time
        self.__election_location = location
        self.__is_open = is_open

    def __generate_election_id(self) -> str:
        """Generates a unique election ID based on the last election ID stored in the database."""
        last_election = self._db_service.get_last_election()

        if last_election:
            last_id = last_election["election_id"]
            if last_id.startswith("elid") and last_id[4:].isdigit():
                return f"elid{int(last_id[4:]) + 1:02d}"

        return "elid01"  

    def get_election_id(self) -> str:
        return self.__election_id

    def get_date(self) -> str:
        return self.__election_date

    def get_time(self) -> str:
        return self.__election_time

    def get_location(self) -> str:
        return self.__election_location

    def get_is_open(self) -> bool:
        return self.__is_open

    def set_date(self, election_date: str):
        self.__election_date = election_date

    def set_time(self, election_time: str):
        self.__election_time = election_time

    def set_location(self, location: str):
        self.__election_location = location

    def set_is_open(self, is_open: bool):
        self.__is_open = is_open

    def add_candidate(self, election_id: str, candidate: Candidate):
        """Adds a candidate to the election."""
        candidate_data = {
            "candidate_id": candidate.get_candidate_id(),
            "name": candidate.get_name(),
            "position": candidate.get_position(),
            "is_independent": candidate.get_is_independent(),
            "political_party": candidate.get_political_party(),
        }
        self._db_service.save_candidate(election_id, candidate_data)

    @classmethod
    def start_election(cls, election_id: str):
        """Opens the election for voting."""
        cls._db_service.set_election_status_to_open(election_id, True)

    @classmethod
    def close_election(cls, election_id: str):
        """Closes the election and stops voting."""
        cls._db_service.set_election_status_to_close(election_id, False)

    @classmethod
    def has_voter_voted(cls, user_id: str) -> bool:
        """Checks if a voter has already voted in the election."""
        vote_record = cls._db_service.get_voter_vote_status(user_id)
        return vote_record is not None and vote_record.get("has_voted", False)
    
    def submit_ballot(self, ballot: Ballot):
        """Submits the ballot by passing its data to the DatabaseService."""
        ballot_id = ballot.get_encrypted_ballot_id() 
        print(ballot_id)
        encrypted_votes = [vote.get_encrypted_vote() for vote in ballot.get_votes()]  

        self._db_service.record_encrypted_ballot(ballot_id,  encrypted_votes)
    
    @classmethod
    def decrypt_results(cls, election_id: str):
        """Decrypts the encrypted ballots for vote counting."""
        encrypted_ballots = cls._db_service.get_all_encrypted_ballots(election_id)
        decrypted_results = {}
        
        for ballot in encrypted_ballots:
            for encrypted_vote in ballot.get("encrypted_votes", []):
                # In a real implementation, this would use proper cryptographic methods
                # to decrypt the votes using the election's private key
                candidate_id = cls._db_service.decrypt_vote(encrypted_vote)
                if candidate_id in decrypted_results:
                    decrypted_results[candidate_id] += 1
                else:
                    decrypted_results[candidate_id] = 1
        
        # Store the decrypted results in the database
        cls._db_service.store_election_results(election_id, decrypted_results)
        return decrypted_results
    
    @classmethod
    def post_winners(cls, election_id: str):
        """Determines the winners of the election and posts the results."""
        # Get the results, either from database or by decrypting if not already done
        results = cls._db_service.get_election_results(election_id)
        if not results:
            results = cls.decrypt_results(election_id)
        
        # Get all candidates for this election
        candidates = cls._db_service.get_candidates_by_election(election_id)
        
        # Group candidates by position
        positions = {}
        for candidate in candidates:
            position = candidate.get("position")
            if position not in positions:
                positions[position] = []
            positions[position].append(candidate)
        
        # Determine the winner for each position
        winners = {}
        for position, candidates_list in positions.items():
            max_votes = 0
            position_winner = None
            
            for candidate in candidates_list:
                candidate_id = candidate.get("candidate_id")
                votes = results.get(candidate_id, 0)
                
                if votes > max_votes:
                    max_votes = votes
                    position_winner = candidate
            
            if position_winner:
                winners[position] = {
                    "candidate": position_winner,
                    "votes": max_votes
                }
        
        # Post the winners to the database
        cls._db_service.save_election_winners(election_id, winners)
        return winners


