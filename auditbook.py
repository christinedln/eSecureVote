from database_service import DatabaseService
from utils import generate_auditlog_id

class AuditBook:
    _db_service = DatabaseService()  

    def __init__(self, auditlog_id=None, user_id=None, action=None, timestamp=None):
        self.__auditlog_id = auditlog_id if auditlog_id else generate_auditlog_id()
        self.__user_id = user_id  
        self.__action = action
        self.__timestamp = timestamp

    def get_auditlog_id(self):
        return self.__auditlog_id

    def get_user_id(self):
        return self.__user_id

    def get_action(self):
        return self.__action

    def get_timestamp(self):
        return self.__timestamp

    def _create_log(self):

        audit_data = {
            "auditlog_id": self.get_auditlog_id(),  
            "user_id": self.get_user_id(),
            "action": self.get_action(),
            "timestamp": self.get_timestamp()
        }

        self._db_service.save_log(audit_data)

    def view_logs(self):
        return self._db_service.get_all_logs()