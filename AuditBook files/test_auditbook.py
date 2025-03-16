import unittest
import io
import sys
from AuditClass import AuditBook  # Adjust this import based on your file structure

class TestAuditBook(unittest.TestCase):

    def setUp(self):
        # Create a fresh AuditBook instance for each test
        self.audit_book = AuditBook("test_log")
        # Store the original stdout to restore it later
        self.original_stdout = sys.stdout

    def tearDown(self):
        # Restore the original stdout after each test
        sys.stdout = self.original_stdout

    def test_get_logs_empty(self):
        """Test getLogs with an empty log list."""
        # Redirect stdout to capture printed output
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the method
        self.audit_book.getLogs()

        # Check that nothing was printed
        self.assertEqual(captured_output.getvalue(), "")

    def test_get_logs_single_entry(self):
        """Test getLogs with a single log entry."""
        # Add a log entry using the private method
        self.audit_book._AuditBook__createLog("user1", "login")

        # Redirect stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the method
        self.audit_book.getLogs()

        # Check the output format (note: we can't check the exact timestamp)
        output = captured_output.getvalue().strip()
        self.assertIn("User: user1", output)
        self.assertIn("Action: login", output)
        self.assertIn("Time:", output)

    def test_get_logs_multiple_entries(self):
        """Test getLogs with multiple log entries."""
        # Add multiple log entries
        self.audit_book._AuditBook__createLog("user1", "login")
        self.audit_book._AuditBook__createLog("user2", "view_ballot")
        self.audit_book._AuditBook__createLog("user1", "cast_vote")

        # Redirect stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the method
        self.audit_book.getLogs()

        # Check for all entries in the output
        output = captured_output.getvalue()
        self.assertIn("User: user1, Action: login", output)
        self.assertIn("User: user2, Action: view_ballot", output)
        self.assertIn("User: user1, Action: cast_vote", output)

        # Count number of lines to verify all entries were printed
        lines = output.strip().split('\n')
        self.assertEqual(len(lines), 3)

    def test_get_logs_special_characters(self):
        """Test getLogs with special characters in user IDs and actions."""
        # Add log entries with special characters
        self.audit_book._AuditBook__createLog("user@example.com", "login-attempt#1")
        self.audit_book._AuditBook__createLog("admin_123", "system: restart")

        # Redirect stdout
        captured_output = io.StringIO()
        sys.stdout = captured_output

        # Call the method
        self.audit_book.getLogs()

        # Check output
        output = captured_output.getvalue()
        self.assertIn("User: user@example.com, Action: login-attempt#1", output)
        self.assertIn("User: admin_123, Action: system: restart", output)

if __name__ == '__main__':
    unittest.main()
