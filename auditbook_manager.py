from database_service import DatabaseService
from auditbook import AuditBook

class AuditBookManager:
    def __init__(self):
        self._db_service = DatabaseService()

    def create_log(self, auditlog):
        audit_data = {
            "auditlog_id": auditlog.get_auditlog_id(),
            "user_id": auditlog.get_user_id(),
            "action": auditlog.get_action(),
            "timestamp": auditlog.get_timestamp(),
        }
        self._db_service.save_log(audit_data)

    def view_logs(self):
        return self._db_service.get_all_logs()
