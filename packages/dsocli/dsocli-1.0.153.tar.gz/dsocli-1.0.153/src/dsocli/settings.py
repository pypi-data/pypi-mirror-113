import os
COLORIZE_LOGS = os.getenv('DSO_COLORIZE_LOGS') or True
BOLD_LOGS = os.getenv('DSO_BOLD_LOGS') or True
TIMESTAMP_LOGS = os.getenv('DSO_TIMESTAMP_LOGS') or True
LABEL_LOG_LEVELS = os.getenv('DSO_LABEL_LOG_LEVELS') or True
USE_PAGER = os.getenv('DSO_USE_PAGER') or True
ALLOW_STAGE_TEMPLATES = os.getenv('DSO_ALLOW_STAGE_TEMPLATES') or False

