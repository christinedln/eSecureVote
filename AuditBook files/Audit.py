# class AuditBook:
#     def __init__(self):
#         """
#         Initialize the AuditBook to track votes and election results.
#         """
#         self.vote_counts = {}  # Dictionary to store candidate vote counts
#         self.total_votes = 0
#         self.is_election_active = False
#         self.election_results = None

#     def start_tracking(self, candidate_list):
#         """
#         Start tracking an election with the provided candidates.
        
#         Args:
#             candidate_list (list): List of candidate names
#         """
#         self.vote_counts = {candidate: 0 for candidate in candidate_list}
#         self.total_votes = 0
#         self.is_election_active = True
#         self.election_results = None
#         print("AuditBook: Started tracking election results")

#     def record_vote(self, candidate):
#         """
#         Record a vote for a specific candidate.
        
#         Args:
#             candidate (str): The candidate receiving the vote
            
#         Returns:
#             bool: True if vote was recorded successfully, False otherwise
#         """
#         if not self.is_election_active:
#             print("Error: Election is not active")
#             return False
            
#         if candidate not in self.vote_counts:
#             print(f"Error: Candidate '{candidate}' not found")
#             return False
            
#         self.vote_counts[candidate] += 1
#         self.total_votes += 1
#         return True

#     def get_current_results(self):
#         """
#         Get the current vote count status.
        
#         Returns:
#             dict: Current results with vote counts and percentages
#         """
#         results = {
#             'total_votes': self.total_votes,
#             'candidates': {}
#         }
        
#         for candidate, votes in self.vote_counts.items():
#             percentage = (votes / self.total_votes) * 100 if self.total_votes > 0 else 0
#             results['candidates'][candidate] = {
#                 'votes': votes,
#                 'percentage': round(percentage, 2)
#             }
            
#         return results
    
#     def display_current_results(self):
#         """Display the current election results."""
#         if self.total_votes == 0:
#             print("No votes recorded yet.")
#             return
            
#         print("\n--- Current Election Results ---")
#         print(f"Total Votes: {self.total_votes}")
        
#         for candidate, votes in self.vote_counts.items():
#             percentage = (votes / self.total_votes) * 100
#             print(f"{candidate}: {votes} votes ({percentage:.2f}%)")
#         print("-----------------------------\n")
    
#     def finalize_election(self):
#         """
#         End the election and calculate final results.
        
#         Returns:
#             dict: Final election results
#         """
#         if not self.is_election_active:
#             print("Error: No active election to finalize")
#             return None
            
#         self.is_election_active = False
        
#         # Find the winner(s) - handling potential ties
#         max_votes = max(self.vote_counts.values()) if self.vote_counts else 0
#         winners = [c for c, v in self.vote_counts.items() if v == max_votes]
        
#         self.election_results = {
#             'total_votes': self.total_votes,
#             'candidates': {},
#             'winner': winners[0] if len(winners) == 1 else "Tie between " + ", ".join(winners),
#             'is_tie': len(winners) > 1
#         }
        
#         for candidate, votes in self.vote_counts.items():
#             percentage = (votes / self.total_votes) * 100 if self.total_votes > 0 else 0
#             self.election_results['candidates'][candidate] = {
#                 'votes': votes,
#                 'percentage': round(percentage, 2)
#             }
            
#         return self.election_results
    
#     def publish_results(self):
#         """
#         Publish the final election results.
#         """
#         if self.is_election_active:
#             print("Error: Election is still active. Finalize the election first.")
#             return
            
#         if not self.election_results:
#             print("Error: No election results to publish")
#             return
            
#         print("\n===== OFFICIAL ELECTION RESULTS =====")
#         print(f"Total votes cast: {self.total_votes}")
#         print("\nVote Distribution:")
        
#         # Sort candidates by number of votes (descending)
#         sorted_candidates = sorted(
#             self.vote_counts.items(),
#             key=lambda x: x[1],
#             reverse=True
#         )
        
#         for candidate, votes in sorted_candidates:
#             percentage = (votes / self.total_votes) * 100 if self.total_votes > 0 else 0
#             print(f"{candidate}: {votes} votes ({percentage:.2f}%)")
            
#         print("\nRESULT:")
#         if self.election_results['is_tie']:
#             print(f"TIE ELECTION: {self.election_results['winner']}")
#         else:
#             print(f"WINNER: {self.election_results['winner']}")
#         print("====================================\n")


# # Example usage
# if __name__ == "__main__":
#     # Simple demonstration
#     audit = AuditBook()
#     audit.start_tracking(["Candidate A", "Candidate B", "Candidate C"])
    
#     # Simulate some votes
#     for _ in range(5):
#         audit.record_vote("Candidate A")
#     for _ in range(3):
#         audit.record_vote("Candidate B")
#     for _ in range(2):
#         audit.record_vote("Candidate C")
    
#     # Show current results during the election
#     audit.display_current_results()
    
#     # End the election and publish results
#     audit.finalize_election()
#     audit.publish_results()