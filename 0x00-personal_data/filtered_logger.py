#!/usr/bin/env python3
"""0x00. Personal data"""
import re
from typing import List


def filter_datum(
    fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """Write a function called filter_datum that returns the log message obfuscated:"""
    for field in fields:
        message = re.sub(
            f"{field}=.*?{separator}", f"{field}={redaction}{separator}", message
        )
    return message


import logging

PII_FIELDS = ("name", "email", "phone", "password", "ssn")


def get_logger() -> logging.Logger:
    """Implement a get_logger function that takes no arguments and returns a logging.Logger object."""
    logger = logging.Logger("user_data", level=logging.INFO)
    handler = logging.StreamHandler()
    formatter = RedactingFormatter()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.propagate = False
    return logger


class RedactingFormatter(logging.Formatter):
    """Redacting Formatter class"""

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum"""
        record.msg: str = filter_datum(
            self.fields,
            redaction=self.REDACTION,
            message=record.msg,
            separator=self.SEPARATOR,
        )
        return super(RedactingFormatter, self).format(record)
