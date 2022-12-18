from abc import ABC, abstractmethod
from dataclasses import dataclass

class BoolGenerator(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def generate(self, *args)->bool:
        pass