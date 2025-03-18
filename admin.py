from user import User
from database_service import DatabaseService
from election import Election

class Admin(User):
    def __init__(self, user_id: str):
        self.db_service = DatabaseService()
        user_data = self.db_service.get_user_data(user_id)

        if user_data and user_data.get("role") == "Admin":
            super().__init__(
                user_id=user_id,
                name=user_data.get("name"),
                province=user_data.get("province"),
                municipality=user_data.get("municipality"),
                email=user_data.get("email"),
                password=user_data.get("password"), #hashed
                role="Admin"
            )
            self.__admin_level = user_data.get("admin_level", 0)
        else:
            raise ValueError("User is not an admin or does not exist.")

    def get_admin_level(self) -> int:
        return self.__admin_level

    def set_admin_level(self, admin_level: int):
        self.__admin_level = admin_level

    def create_election(self, election: Election):
        election_data = {
            "election_id": election.get_election_id(),
            "date": election.get_date(),
            "time": election.get_time(),
            "location": election.get_location(),
            "is_open": election.get_is_open()
        }
        self.db_service.save_election(election_data)

    def start_election(self, election_id: str):
        Election.start_election(election_id)

    def close_election(self, election_id: str):
        Election.close_election(election_id)
        
    def decrypt_results(self, election_id: str) -> dict:
        """
        Decrypt the election results for a specified election.
        Only admins with level 2 or higher can decrypt results.
        
        Args:
            election_id: The ID of the election to decrypt results for
            
        Returns:
            A dictionary containing the decrypted election results
            
        Raises:
            PermissionError: If the admin doesn't have the required admin level
        """
        if self.__admin_level < 2:
            raise PermissionError("Admin level 2 or higher required to decrypt election results")
            
        # Get the encrypted results from the database
        encrypted_results = self.db_service.get_election_results(election_id)
        
        if not encrypted_results:
            return {"message": "No results found for this election"}
            
        # In a real implementation, this would use proper cryptographic methods
        decrypted_results = self._perform_decryption(encrypted_results)
        
        # Log the decryption activity
        self.db_service.log_activity(
            user_id=self.get_user_id(),
            action=f"Decrypted results for election {election_id}",
            timestamp=self.db_service.get_current_timestamp()
        )
        
        return decrypted_results
    
    def _perform_decryption(self, encrypted_data: dict) -> dict:
        """
        Private method to perform the actual decryption of election data.
        In a real implementation, this would use cryptographic libraries.
        
        Args:
            encrypted_data: The encrypted election results
            
        Returns:
            The decrypted election results
        """
        # This is a placeholder for actual decryption logic
        # In a real implementation, you would use proper cryptographic methods
        decrypted_data = {}
        
        for candidate_id, encrypted_count in encrypted_data.items():
            # Simulating decryption
            decrypted_data[candidate_id] = encrypted_count  # Replace with actual decryption
            
        return decrypted_data
