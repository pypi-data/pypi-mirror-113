import abc
import pandas as pd

class IDataLayer(metaclass=abc.ABCMeta):
    
    @abc.abstractmethod
    def pull(self, name:str) -> pd.DataFrame:
        raise NotImplementedError

    @abc.abstractmethod
    def push(self, name: str, df: pd.DataFrame) -> None:
        raise NotImplementedError