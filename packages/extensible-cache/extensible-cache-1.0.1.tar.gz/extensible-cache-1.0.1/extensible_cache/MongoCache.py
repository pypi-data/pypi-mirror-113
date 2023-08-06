'''
Caching Object that will store objects in a MongoDB.

Used to buffer documents into a mongo db store
'''

from datetime import datetime, timedelta
from typing import Tuple, Any
import pickle

# make import optional
try:
    import pymongo as mongo
except Exception:
    mongo = None

from .Cache import Cache


DEFAULT_COLLECTION = "cache"
INTERVAL_TIMECHECK_SEC = 60


class MongoCache(Cache):
    """Cache that buffers data into a mongo db database

    Args:
        handler (MongoClient): Connection to the MongoDB Database
        database (str): Name of the database to use
    """
    def __init__(self, handler: Any, database: str, keep_history: bool = True, outdated_interval: int = None):
        super().__init__(keep_history=keep_history, outdated_interval=outdated_interval)

        # check if mongo is loaded
        if mongo is None:
            raise RuntimeError("Please make sure that pymongo is installed!")

        # retrieve the handler to the mongo connection
        if isinstance(handler, mongo.MongoClient):
            raise ValueError(f"Expected handler to be a MongoClient, but got {type(handler).__name__}")
        self.handler = handler
        self.db_name = database

        # retrieve database (to trigger creation)
        self.database = self.handler[database]
        # check if database exists
        ls_dbs = self.handler.list_database_names()
        if database not in ls_dbs:
            raise RuntimeError("Could not find the specified mongo-db database")

    def _serialize(self, value: Any) -> dict:
        '''Serializes the given data to be stored in the mongo db.

        Note: Overwrite this in child classes to adjust to your data structure.
        '''
        pickled = pickle.dumps(value, 0).decode()
        return {
            "data": pickled
        }

    def _deserialize(self, value: dict) -> Any:
        '''Deserialized data from the mongo db to the original format.

        Note: Overwrite this in child classes to adjust to your data structure.
        '''
        item = pickle.loads(value["data"].encode())
        return item

    def _store(self, key: str, date: datetime, value: Any) -> bool:
        # generate the item
        item = {
            "_key": key,
            "_time": date.timestamp(),
            "item": self._serialize(value)
        }

        # check if only newest data should be stored
        if self.keep_history is False:
            # delete old data
            self.database[DEFAULT_COLLECTION].delete_many({"_key": key})
            key = DEFAULT_COLLECTION

        # insert the item
        self.database[key].insert(item)
        return True

    def _retrieve(self, key: str, date: datetime) -> Tuple[Any, datetime]:
        # update the database
        db = key if self.keep_history else DEFAULT_COLLECTION

        # build the query (add additional datetime check)
        query = {"_key": key}
        if date is not None:
            query = {'$and': [
                query,
                {'$and': [
                    {"_time": {"$gte": date - timedelta(seconds=INTERVAL_TIMECHECK_SEC)}},
                    {"_time": {"$lte": date + timedelta(seconds=INTERVAL_TIMECHECK_SEC)}}
                ]}
            ]}

        # find the data
        data = self.database[db].find(query).sort("_time", -1).limit(1)

        # check if found
        if data is None:
            return None, None

        # parse the data
        item = self._deserialize(data["item"])
        time = datetime.fromtimestamp(data["_time"])

        return item, time
