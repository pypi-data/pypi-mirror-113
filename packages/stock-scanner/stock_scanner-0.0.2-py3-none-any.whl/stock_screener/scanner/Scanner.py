# Parent class
from abc import ABC, abstractmethod

# Data IO
from ..data_reader.CSVReader import CSVReader
from ..data_reader.DataReader import DataReader
from ..data_fetcher.DataFetcher import DataFetcher
from ..data_fetcher.YahooDataFetcher import YahooDataFetcher

# Condition validation
from ..validator.Validator import Validator
from ..validator.BasicValidator import BasicValidator

# Misc.
from ..Stock import Stock
from typing import List
from ..condition.Condition import Condition


class Scanner(ABC):
    """
    Abstract scanner class all scanners should inherit from. The abstract methods need to be implemented.
    """
    def __init__(self, conditions: List[Condition],
                data_fetcher: DataFetcher = YahooDataFetcher, data_reader: DataReader = CSVReader,
                validator: Validator = BasicValidator) -> None:
        """
        Parameters
        ----------
        conditions: List[Condition]
            List of conditions stocks returned from scan should fulfill.
        data_fetcher: DataFetcher, optional
            An instance of DataFetcher, default is YahooDataFetcher.
        data_reader: DataReader, optional
            An instance of DataReader, the default is CSVReader and is compatible with
            files saved by YahooDataFetcher.
        validator: Validator, optional
            An instance of Validator, the default is BasicValidator.
        """
        self.conditions: List[Condition] = conditions
        self.data_fetcher: DataFetcher = data_fetcher
        self.data_reader: DataReader = data_reader
        self.validator: Validator = validator

    @abstractmethod
    def loadData(self, period: int = 365, verbose: bool = False) -> None:
        """
        Loads all stock data required for the scan.

        Parameters
        ----------
        period: int
            How many days back you want data for each stock
        verbose: bool, optional
            Whether the download should be verbose, IE show progress or what
            stock is currently being downloaded.
        """
        return self

    @abstractmethod
    def getCandidates(self, verbose: bool = False) -> List[Stock]:
        """
        Return candidate stocks from the scan.

        Parameters
        ----------
        verbose: bool, optional
            Whether the process should be verbose, IE show progress or what
            stock is currently being analyzed.
        """
        pass