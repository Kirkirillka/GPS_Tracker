import pymongo
from pymongo.errors import ConnectionFailure

import logging

from typing import List, Dict
from config.utils import get_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG = get_config()


class StorageAdapter:

    def __init__(self):

        self.host = CONFIG['storage']['host']
        self.port = int(CONFIG['storage']['port'])

        self._username = CONFIG['storage']['db_user']
        self._password = CONFIG['storage']['db_password']

        self.db_name = CONFIG['storage']['db_name']
        self.collection_name = CONFIG['storage']['connection_name']

        self.is_initialized = False

    def _connect(self) -> bool:
        try:

            logger.info(f"Establish connection to MongoDB instance on {self.host}:{self.port} as '{self._username}' ")

            connection = pymongo.MongoClient("mongodb://%s:%s@%s:%s" % (
                self._username,
                self._password,
                self.host,
                self.port,
            ))

        except ConnectionFailure as e:

            logger.error("Connection to MongoDB failed! Timed out.")

            raise e
        else:
            self._db_conn = connection[self.db_name]

            self.is_initialized = True

            return True

    def setup(self) -> bool:

        logger.info("Setting up StorageAdapter")

        res = self._connect()

        if res:
            self.is_initialized = True

        return res

    def save_message(self, message: dict) -> str:

        # Check if message indeed is dictionary
        if not isinstance(message,dict):
            raise TypeError('Message must be dictionary')

        # Check if not initialized yet
        if not self.is_initialized:
            raise EnvironmentError("Please, setup StorageAdapter before first usage!")

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        res = collection.insert_one(message).inserted_id

        logger.debug(f"Saved a record with id '{res} in collection '{self.collection_name}'")

        return res

    def del_message(self, message):

        # Check if message indeed is dictionary
        if not isinstance(message,dict):
            raise TypeError('Message must be dictionary')

        # Check if not initialized yet
        if not self.is_initialized:
            raise EnvironmentError("Please, setup StorageAdapter before first usage!")

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        res_id = collection.find_one_and_delete(message).get("_id",None)

        logger.debug(f"Delete a record with id '{res_id}' in collection '{self.collection_name}'")

        return res_id

    def get_all_messages(self) -> List[Dict]:

        # Check if not initialized yet
        if not self.is_initialized:
            raise EnvironmentError("Please, setup StorageAdapter before first usage!")

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Return all found messages
        return collection.find()

