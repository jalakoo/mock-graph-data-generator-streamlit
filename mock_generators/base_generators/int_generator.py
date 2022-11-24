from abc import ABC, abstractmethod

class IntGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, *args)->int:
        pass