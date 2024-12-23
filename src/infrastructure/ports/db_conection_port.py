from abc import ABC, abstractmethod

class DBConnectionPort(ABC):
    @abstractmethod
    def get_connection(self):
        """_summary_
        *args, **kwargs
        """
        pass