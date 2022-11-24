from abc import ABC, abstractmethod

class FloatGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, *args)->float:
        pass