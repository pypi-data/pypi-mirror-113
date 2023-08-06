'''Library to use for Panda Caching.'''

from abc import abstractmethod
from datetime import datetime
from typing import Any, Tuple


# Interval after which data is determined as outdated (if newer data arrives)
INTERVAL_OUTDATE_SEC = 60


class Cache():
    """General caching functions that allow to buffer data to a datastore.
    Note that this is an abstract baseclass, so that all datastore and file-type handling functions
    need to be implemented by child functions.
    Args:
        keep_history (bool): Defines if the cache should keep all history of the data (usually only prefered for file stores).
            If this is not set, all functions will always return the newest datepoint.
        outdated_interval (int): Defines the time overlap values are allowed to have before they are deemed outdated
            if new values arrive.
    """
    def __init__(self, keep_history: bool = False, outdated_interval: int = None):
        self.keep_history = keep_history
        if outdated_interval is None:
            outdated_interval = INTERVAL_OUTDATE_SEC
        self.outdated_interval = outdated_interval

    def __getitem__(self, key: str) -> Any:
        '''Retrieves a current item based on the given key.'''
        value, _ = self.get(key)
        return value

    def __setitem__(self, key: str, value: Any):
        '''Sets a current item based on the key.'''
        self.set(key, value)

    def get(self, key: str, closest_date: datetime = None, outdate_sec: int = None) -> Tuple[Any, datetime]:
        """Retrieves and item from the store.
        Args:
            key (str): The key to retrieve
            closest_date (datetime, optional): The closest date to retrieve data from (if None return newest). Defaults to None.
            outdate_sec (int, optional): If set makes sure that the data is at most X seconds old. Defaults to None.
        Returns:
            Tuple[Any, datetime]: The data that is returned. If no matching data is found, will be None
        """
        value, date = self._retrieve(key, closest_date)

        # check if value exsist
        if value is None:
            return None, None

        # check if outdated
        if outdate_sec is not None and (datetime.now() - date).total_seconds() > outdate_sec:
            return None, None

        return value, date

    def set(self, key: str, value: Any, date: datetime = None, newer_only: bool = True) -> bool:
        """Updates the data in the datastore with the given values.
        Args:
            key (str): Key used to store the data
            value (Any): Value that should be stored
            date (datetime, optional): Optional datetime for the data (otherwise current date). Defaults to None.
            newer_only (bool, optional): Defines if the data should only be stored if the date is newer. Defaults to True.
        Returns:
            bool: True if storing is successful, otherwise False.
        """
        # check if date should be checked for newer
        if date is not None and newer_only:
            # retrieve current value
            old_value, old_date = self.get(key)
            # check if value is set at all and if the date is newer
            if old_value is not None and old_date > date:
                return False

        # update the date
        if date is None:
            date = datetime.now()

        # update the data
        return self._store(key, date, value)

    @abstractmethod
    def _store(self, key: str, date: datetime, value: Any) -> bool:
        """Stores the given item in the datastore
        Args:
            key (str): The key to store the item under
            date (datetime): The date attached to the item version
            value (Any): The actual value to store
        Returns:
            bool: True if store was successful, otherwise false.
        """
        raise NotImplementedError("This should be implemented in child classes!")

    @abstractmethod
    def _retrieve(self, key: str, date: datetime = None) -> Tuple[Any, datetime]:
        """Retrieves the request item from the datastore.
        Args:
            key (str): The key to retrieve for
            date (datetime, optional): The closest datetime to retrieve for (not used if None). Defaults to None.
        Returns:
            Tuple[Any, datetime]: Returns a dataframe and a datetime of the key item (both can be None if no item exists).
        """
        raise NotImplementedError("This should be implemented in child classes!")

    def _check_outdated(self, key_date: datetime, check_date: datetime, strict: bool = False) -> bool:
        '''Checks if the key_date is outdated compared to the checkdate.
        Args:
            key_date (datetime): Datetime of the key to check
            check_date (datetime): Reference datetime to check if newer
            strict (bool): Defines if no interval is allowed
        Return:
            True if check_date is newer and False if the key_date is newer
        '''
        interval = self.outdated_interval if not strict else 0
        return (key_date - check_date).total_seconds() < interval

    def is_outdated(self, key, date=None):
        '''Checks if the item at the given key is outdated.
        Args:
            key (str): Key to check against
            date (datetime): Optional datetime to check the key_date against (if None will use current time).
        Returns:
            True if key is outdated or does not exist. Otherwise False.
        '''
        # retrieve the date for the key
        _, key_date = self.get(key)
        if key_date is None:
            return True

        # check date
        if date is None:
            date = datetime.now()

        # perform check
        return self._check_outdated(key_date, date)
