from abc import ABC, abstractmethod
import datetime

class DatetimeGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, *args)->datetime:
        pass