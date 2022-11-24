from abc import ABC, abstractmethod

class BoolGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, *args)->bool:
        pass