import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

class FirebaseHandler:
    def __init__(self):
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            # Get the path to the Firebase config file
            config_path = os.path.join(os.path.dirname(__file__), 'FirebaseConfig.json')
            cred = credentials.Certificate(config_path)
            firebase_admin.initialize_app(cred)
        
        # Initialize Firestore client
        self.db = firestore.client()

    def save_log(self, collection_name, log_entry):
        try:
            self.db.collection(collection_name).add(log_entry)
            return {"status": "success", "message": "Log saved successfully"}
        except Exception as e:
            return {"status": "failure", "message": str(e)}

    def get_logs(self, collection_name):
        docs = self.db.collection(collection_name).stream()
        return [doc.to_dict() for doc in docs]

class AuditBook:
    def __init__(self, logId=""):
        """
        Initialize an AuditBook instance.
        
        Args:
            logId (str): The ID of the log book
        """
        self.logId = logId
        self.__logs = []
        self.firebase_handler = FirebaseHandler()
        
    def __createLog(self, userId, action):
        """
        Private method to create a log entry.
        
        Args:
            userId (str): The ID of the user performing the action
            action (str): Description of the action performed
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = {
            "userId": userId,
            "action": action,
            "timestamp": timestamp
        }
        self.__logs.append(log_entry)
        
        # Save to Firebase
        self.saveLogToFirebase(log_entry)
    
    def saveLogToFirebase(self, log_entry):
        collection_name = f"audit_logs_{self.logId}" if self.logId else "audit_logs"
        return self.firebase_handler.save_log(collection_name, log_entry)
    
    def addLog(self, userId, action):
        """
        Add a log entry to the audit book.
        
        Args:
            userId (str): The ID of the user performing the action
            action (str): Description of the action performed
        """
        self.__createLog(userId, action)
    
    def getLogs(self):
        """
        Display all logs in the audit book.
        """
        for log in self.__logs:
            print(f"User: {log['userId']}, Action: {log['action']}, Time: {log['timestamp']}")
    
    def getLogsFromFirebase(self):
        """
        Retrieve logs from Firebase and return them.
        
        Returns:
            list: List of log entries from Firebase
        """
        collection_name = f"audit_logs_{self.logId}" if self.logId else "audit_logs"
        return self.firebase_handler.get_logs(collection_name)
    
    def checkAdminAccess(self, userId):
        """
        Check if the admin has access based on log entries.
        
        Args:
            userId (str): The ID of the admin user
        
        Returns:
            bool: True if admin has access, False otherwise
        """
        logs = self.getLogsFromFirebase()
        # Example: Block admin if there are too many failed login attempts
        failed_attempts = sum(1 for log in logs if log["userId"] == userId and "failed" in log["action"].lower())
        if failed_attempts >= 3:
            return False  # Block admin
        return True  # Allow admin
