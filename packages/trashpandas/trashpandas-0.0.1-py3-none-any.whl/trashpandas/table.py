import pandas as pd
from interfaces import IDataLayer


class Table:
    def __init__(self, name: str, datalayer: IDataLayer) -> None:
        self.name = name
        self.datalayer = datalayer
        self.pull()

    def pull(self) -> None:
        self.df: pd.DataFrame = self.datalayer.pull(self.name)

    def push(self) -> None:
        self.datalayer.push(self.name, self.df)

    