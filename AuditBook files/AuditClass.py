import datetime

class AuditBook:
    def __init__(self, logId=""):
        """
        Initialize an AuditBook instance.
        
        Args:
            logId (str): The ID of the log book
        """
        self.logId = logId
        self.logs = []
    
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
    
    def getLogs(self):
        """
        Display all logs in the audit book.
        """
        for log in self.logs:
            print(f"User: {log['userId']}, Action: {log['action']}, Time: {log['timestamp']}")