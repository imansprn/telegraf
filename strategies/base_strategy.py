from abc import ABC, abstractmethod

class BaseStrategy(ABC):
    @abstractmethod
    def build_prompt(self, problem_data):
        """Build a prompt based on the problem data"""
        pass 