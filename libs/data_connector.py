from abc import ABC, abstractmethod


class DataConnector(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def fetch_data(self):
        pass

    @abstractmethod
    def close(self):
        pass
