from abc import ABC, abstractmethod

class Connector(ABC):
    @abstractmethod
    def fetch_balances(self):
        """Must return a list of scales in internal format"""
        pass