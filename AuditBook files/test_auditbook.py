import unittest
from unittest.mock import patch, MagicMock
from AuditClass import AuditBook

# Import the AuditBook class using absolute import since parent directory is a namespace package

class TestGetLogsFromFirebase(unittest.TestCase):
    
    @patch('firebase_admin.initialize_app')
    @patch('firebase_admin.credentials.Certificate')
    @patch('firebase_admin.firestore.client')
    def setUp(self, mock_firestore_client, mock_certificate, mock_initialize_app):
        # Set up mocks
        self.mock_db = MagicMock()
        self.mock_collection = MagicMock()
        self.mock_db.collection.return_value = self.mock_collection
        mock_firestore_client.return_value = self.mock_db
        
        # Create test instances
        self.audit_book_custom = AuditBook("test_log")
        self.audit_book_default = AuditBook()
        
        # Reset firebase mock calls for clean tests
        mock_firestore_client.reset_mock()
        self.mock_db.reset_mock()
        self.mock_collection.reset_mock()

    def test_getLogsFromFirebase_custom_logId(self):
        """Test retrieving logs with a custom logId"""
        # Mock data from Firestore
        mock_doc1 = MagicMock()
        mock_doc1.to_dict.return_value = {
            "userId": "user1", 
            "action": "login", 
            "timestamp": "2023-01-01 12:00:00"
        }
        
        mock_doc2 = MagicMock()
        mock_doc2.to_dict.return_value = {
            "userId": "user2", 
            "action": "logout", 
            "timestamp": "2023-01-01 13:00:00"
        }
        
        # Set up the mock to return our fake documents
        self.mock_collection.stream.return_value = [mock_doc1, mock_doc2]
        
        # Call the method
        result = self.audit_book_custom.getLogsFromFirebase()
        
        # Verify the collection name is correct for custom logId
        self.mock_db.collection.assert_called_once_with("audit_logs_test_log")
        
        # Verify stream method was called
        self.mock_collection.stream.assert_called_once()
        
        # Check the result
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["userId"], "user1")
        self.assertEqual(result[0]["action"], "login")
        self.assertEqual(result[1]["userId"], "user2")
        self.assertEqual(result[1]["action"], "logout")

    def test_getLogsFromFirebase_default_logId(self):
        """Test retrieving logs with default logId"""
        # Mock data from Firestore
        mock_doc = MagicMock()
        mock_doc.to_dict.return_value = {
            "userId": "user1", 
            "action": "view", 
            "timestamp": "2023-01-01 15:00:00"
        }
        
        # Set up the mock to return our fake document
        self.mock_collection.stream.return_value = [mock_doc]
        
        # Call the method
        result = self.audit_book_default.getLogsFromFirebase()
        
        # Verify the default collection name is used
        self.mock_db.collection.assert_called_once_with("audit_logs")
        
        # Verify stream method was called
        self.mock_collection.stream.assert_called_once()
        
        # Check the result
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["userId"], "user1")
        self.assertEqual(result[0]["action"], "view")
        self.assertEqual(result[0]["timestamp"], "2023-01-01 15:00:00")

    def test_getLogsFromFirebase_empty_results(self):
        """Test retrieving logs when no logs exist"""
        # Set up the mock to return empty results
        self.mock_collection.stream.return_value = []
        
        # Call the method
        result = self.audit_book_custom.getLogsFromFirebase()
        
        # Verify collection was called
        self.mock_db.collection.assert_called_once_with("audit_logs_test_log")
        
        # Verify stream method was called
        self.mock_collection.stream.assert_called_once()
        
        # Check that result is an empty list
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    def test_getLogsFromFirebase_multiple_entries(self):
        """Test retrieving multiple log entries"""
        # Create multiple mock entries
        mock_docs = []
        for i in range(5):
            mock_doc = MagicMock()
            mock_doc.to_dict.return_value = {
                "userId": f"user{i}", 
                "action": f"action{i}", 
                "timestamp": f"2023-01-01 1{i}:00:00"
            }
            mock_docs.append(mock_doc)
        
        # Set up the mock to return our fake documents
        self.mock_collection.stream.return_value = mock_docs
        
        # Call the method
        result = self.audit_book_custom.getLogsFromFirebase()
        
        # Verify correct collection and method calls
        self.mock_db.collection.assert_called_once_with("audit_logs_test_log")
        self.mock_collection.stream.assert_called_once()
        
        # Check the result
        self.assertEqual(len(result), 5)
        for i in range(5):
            self.assertEqual(result[i]["userId"], f"user{i}")
            self.assertEqual(result[i]["action"], f"action{i}")
            self.assertEqual(result[i]["timestamp"], f"2023-01-01 1{i}:00:00")

if __name__ == '__main__':
    unittest.main()