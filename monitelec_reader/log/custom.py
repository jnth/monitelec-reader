import datetime
import logging.handlers
from logging import Formatter
from typing import Optional


class FilterOnePerMinutes(logging.Filter):
    """Only log the first message of each minutes."""
    def __init__(self):
        super(FilterOnePerMinutes, self).__init__(name=self.__class__.__name__.lower())
        self.__t_from_rounded_minute = self.get_t_from_rounded_minute()

    @staticmethod
    def get_t_from_rounded_minute() -> int:
        now = datetime.datetime.now()
        rounded_minute = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, 0)
        return int((now - rounded_minute).total_seconds())

    def filter(self, record: logging.LogRecord) -> bool:
        t_from_rounded_minute = self.get_t_from_rounded_minute()
        ret = True if t_from_rounded_minute < self.__t_from_rounded_minute else False
        self.__t_from_rounded_minute = t_from_rounded_minute
        return ret


class DataLogger(logging.handlers.MemoryHandler):
    def __init__(self, *args, **kwargs):
        fh = logging.FileHandler(kwargs.pop('filename', 'records.log'))
        super(DataLogger, self).__init__(*args, **kwargs)
        self.setTarget(target=fh)

    def setFormatter(self, fmt: Optional[Formatter]) -> None:
        # Apply formatter to target
        self.target.setFormatter(fmt)
        super(DataLogger, self).setFormatter(fmt)
