from database_service import DatabaseService


class AuditBook:
    _db_service = DatabaseService()  


    def __init__(self, auditlog_id=None, user_id=None, action=None, timestamp=None):
        self.__auditlog_id = auditlog_id if auditlog_id else self.__generate_auditlog_id()
        self.__user_id = user_id  
        self.__action = action
        self.__timestamp = timestamp


    def __generate_auditlog_id(self) -> str:
        last_auditlog = self._db_service.get_last_auditlog()


        if last_auditlog:
            last_id = last_auditlog["auditlog_id"]
            if last_id.startswith("alid") and last_id[4:].isdigit():
                return f"alid{int(last_id[4:]) + 1:02d}"


        return "alid01"


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

