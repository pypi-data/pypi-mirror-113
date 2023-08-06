'''Library to use for Panda Caching.'''

from datetime import datetime
import os
from glob import glob
from typing import Tuple

import pandas as pd

from .Cache import Cache


TIME_FORMAT = '%Y-%m-%d_%H-%M-%S'


class PandasFileCache(Cache):
    """Cache that stores pandas dataframes in files.
    Args:
        Cache ([type]): [description]
    """
    def __init__(self, storage_folder, keep_history=False, outdated_interval=None):
        super().__init__(keep_history=keep_history, outdated_interval=outdated_interval)

        # set folder and make sure it exists
        self.folder = storage_folder
        os.makedirs(self.folder, exist_ok=True)

    def _encode_key(self, key: str) -> str:
        """Additional function to encode the key in a safe manner
        Args:
            key (str): The key to encode
        Returns:
            str: The encoded key
        """
        return key

    def _store(self, key: str, date: datetime, value: pd.DataFrame) -> bool:
        # make sure data is pandas
        if not isinstance(value, pd.DataFrame):
            raise ValueError(f"PandaCache expects DataFrame, but got {type(value).__name__}")

        # check for key folder
        enc_key = self._encode_key(key)
        key_path = os.path.join(self.folder, enc_key)
        os.makedirs(key_path, exist_ok=True)

        # delete old data if history should not be kept
        if not self.keep_history:
            items = glob(os.path.join(key_path, "*.csv"))
            for item in items:
                os.remove(item)

        # store the data
        value.to_csv(os.path.join(key_path, f"{date.strftime(TIME_FORMAT)}.csv"), header=True, index=False)
        return True

    def _retrieve(self, key: str, date: datetime = None) -> Tuple[pd.DataFrame, datetime]:
        # find key folder
        enc_key = self._encode_key(key)
        key_path = os.path.join(self.folder, enc_key)

        # check if folder exists
        if not os.path.exists(key_path):
            return None, None

        # load all data items
        items = glob(os.path.join(key_path, "*.csv"))
        # parse dates accordingly
        dates = [datetime.strptime(os.path.splitext(os.path.basename(item))[0], TIME_FORMAT) for item in items]

        # check if there are no items
        if len(items) == 0:
            return None, None

        # check if closest should be retrieved
        idx = None
        if date is None:
            # find newest
            for i, d in enumerate(dates):
                if idx is None or d > dates[idx]:
                    idx = i
        else:
            # find closest
            best_distance = None
            for i, d in enumerate(dates):
                distance = abs((date - d).total_seconds())
                if best_distance is None or distance < best_distance:
                    idx = i
                    best_distance = distance

        # check if None
        if idx is None:
            return None, None

        # load the resulting file
        try:
            value = pd.read_csv(items[idx], header="infer")
        except pd.errors.EmptyDataError:
            value = pd.DataFrame()
        except Exception as ex:
            raise ex
        return value, dates[idx]
