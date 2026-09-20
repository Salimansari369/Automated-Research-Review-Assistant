import logging
import sys
import re

class SensitiveFilter(logging.Filter):
    """Filters out potential API keys and tokens from log output."""
    PATTERNS = [
        re.compile(r'(sk-[a-zA-Z0-9]{20,})'),
        re.compile(r'(key-[a-zA-Z0-9]{20,})'),
        re.compile(r'(Bearer\s+[a-zA-Z0-9_\-\.]{20,})'),
    ]

    def filter(self, record):
        msg = record.getMessage()
        for p in self.PATTERNS:
            msg = p.sub("[REDACTED_SECRET]", msg)
        record.msg = msg
        return True

def setup_logger(name: str = "LiteratureAI") -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        handler.addFilter(SensitiveFilter())
        logger.addHandler(handler)
    return logger

logger = setup_logger()
