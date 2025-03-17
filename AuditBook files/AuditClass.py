import datetime
import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

class AuditBook:
    def __init__(self, logId=""):
        """
        Initialize an AuditBook instance.
        
        Args:
            logId (str): The ID of the log book
        """
        self.logId = logId
        self.logs = []
        
        # Initialize Firebase if not already initialized
        if not firebase_admin._apps:
            # Get the path to the Firebase config file
            config_path = os.path.join(os.path.dirname(__file__), 'FirebaseConfig.json')
            cred = credentials.Certificate(config_path)
            firebase_admin.initialize_app(cred)
        
        # Initialize Firestore client
        self.db = firestore.client()
        
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
        self.logs.append(log_entry)
        
        # Save to Firebase
        self.saveLogToFirebase(log_entry)
    
    #Success or Failure Response:
    def saveLogToFirebase(self, log_entry):
        try:
            collection_name = f"audit_logs_{self.logId}" if self.logId else "audit_logs"
            self.db.collection(collection_name).add(log_entry)
            return {"status": "success", "message": "Log saved successfully"}
        except Exception as e:
            return {"status": "failure", "message": str(e)}

    
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
        for log in self.logs:
            print(f"User: {log['userId']}, Action: {log['action']}, Time: {log['timestamp']}")
    
    def getLogsFromFirebase(self):
        """
        Retrieve logs from Firebase and return them.
        
        Returns:
            list: List of log entries from Firebase
        """
        # Use logId as collection name if provided, otherwise use 'audit_logs'
        collection_name = f"audit_logs_{self.logId}" if self.logId else "audit_logs"
        
        # Get all documents from the collection
        docs = self.db.collection(collection_name).stream()
        
        # Convert to list of dictionaries
        firebase_logs = [doc.to_dict() for doc in docs]
        
        return firebase_logs
    
    def checkAdminAccess(self, userId):
    logs = self.getLogsFromFirebase()
    # Example: Block admin if there are too many failed login attempts
    failed_attempts = sum(1 for log in logs if log["userId"] == userId and "failed" in log["action"].lower())
    if failed_attempts >= 3:
        return False  # Block admin
    return True  # Allow admin
