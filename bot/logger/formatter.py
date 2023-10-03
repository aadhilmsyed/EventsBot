import logging
import logging.handlers
import json

class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'name': record.name,
            'levelname': record.levelname,
            'message': record.msg,
        }
        return json.dumps(log_data)
