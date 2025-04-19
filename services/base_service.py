from abc import ABC, abstractmethod

class BaseService(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs):
        """Execute the service's main functionality"""
        pass 