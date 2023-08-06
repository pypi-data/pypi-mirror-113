import os
import pandas as pd
from interfaces import IDataLayer


class DataLayer(IDataLayer):
    def __init__(self, path: str):
        """path is the folder all the DataFrames are stored as pickles"""
        self.path = path
    
    def pull(self, name: str) -> pd.DataFrame:
        return pd.read_pickle(os.path.join(self.path, name))

    def push(self, name: str, df: pd.DataFrame):
        df.to_pickle(os.path.join(self.path, name))

        

    

    