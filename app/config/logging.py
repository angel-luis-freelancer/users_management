import json
import logging
import logging.config
from pathlib import Path

class CustomJSONFormatter(logging.Formatter):
    """Formatter personalizado para generar logs en formato JSON"""
    def format(self, record):
        log_data = {
            'timestamp': self.formatTime(record),
            'logger': record.name,
            'level': record.levelname,
            'message': record.getMessage(),
        }
        
        if hasattr(record, 'exception_type'):
            log_data['exception_type'] = record.exception_type
        if hasattr(record, 'error_message'):
            log_data['error_message'] = record.error_message
        if hasattr(record, 'status_code'):
            log_data['status_code'] = record.status_code
        if hasattr(record, 'details'):
            log_data['details'] = record.details
        if hasattr(record, 'timestamp') and record.timestamp != log_data['timestamp']:
            log_data['exception_timestamp'] = record.timestamp
            
        excluded_fields = {
            'name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
            'filename', 'module', 'lineno', 'funcName', 'created', 
            'msecs', 'relativeCreated', 'thread', 'threadName', 
            'processName', 'process', 'message', 'exc_info', 'exc_text', 
            'stack_info', 'getMessage', 'exception_type', 'error_message', 
            'status_code', 'details', 'timestamp'
        }
        
        for key, value in record.__dict__.items():
            if key not in excluded_fields and not key.startswith('_'):
                log_data[key] = value
        
        return json.dumps(log_data, ensure_ascii=False, default=str)

def setup_logging(app):
    """Configura el sistema de logging"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    LOGGING_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'detailed': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            },
            'json': {
                '()': CustomJSONFormatter,
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'detailed',
                'stream': 'ext://sys.stdout'
            },
            'file_error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'WARNING',
                'formatter': 'json',
                'filename': 'logs/errors.log',
                'maxBytes': 10485760,
                'backupCount': 5
            },
            'file_app': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'json',
                'filename': 'logs/app.log',
                'maxBytes': 10485760,
                'backupCount': 5
            }
        },
        'loggers': {
            'app.errors': {
                'level': 'WARNING',
                'handlers': ['console', 'file_error'],
                'propagate': False
            },
            'app': {
                'level': 'INFO',
                'handlers': ['console', 'file_app'],
                'propagate': False
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console']
        }
    }
    
    logging.config.dictConfig(LOGGING_CONFIG)