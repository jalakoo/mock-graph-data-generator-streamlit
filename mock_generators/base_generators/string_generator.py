from abc import ABC, abstractmethod

class StringGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, *args)->str:
        pass