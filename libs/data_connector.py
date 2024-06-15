from abc import ABC, abstractmethod

class DataConnector(ABC):
    """
    An abstract base class that represents a data connector.

    This class defines the interface for a data connector, which is responsible for connecting to a data source, fetching data from it, and closing the connection.

    The methods of this class should be overridden by any concrete class that inherits from this class.

    Methods:
    connect(): Connects to the data source.
    fetch_data(): Fetches data from the data source.
    close(): Closes the connection to the data source.
    """

    @abstractmethod
    def connect(self):
        """
        Connects to the data source.

        This method should be overridden by any concrete class that inherits from this class.
        """
        pass

    @abstractmethod
    def fetch_data(self):
        """
        Fetches data from the data source.

        This method should be overridden by any concrete class that inherits from this class.

        Returns:
        The data fetched from the data source.
        """
        pass

    @abstractmethod
    def close(self):
        """
        Closes the connection to the data source.

        This method should be overridden by any concrete class that inherits from this class.
        """
        pass