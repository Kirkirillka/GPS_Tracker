import pymongo
from pymongo.errors import ConnectionFailure

import logging

from typing import List, Dict
from config.utils import get_config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

CONFIG = get_config()


class StorageAdapter:

    """
        Class StorageAdapter

        This class to contain convenient interface to access MongoDB Database.

        As other adapters, **StorageAdapter** requires initialization after an object of that class is instantiated.
        However, it's not guaranteed that the requirement will be still preserved.

        To connect to MongoDB instance, **StorageAdapter** uses configuration parameters under *[storage]* section in
        default *config.ini*

        If during the initialization connection to MongoDB is not possible, default *pymongo.ConnectionFailure* is
        raised.

        Examples
        =======

        Perform connection to DB:

        >>> adapter = StorageAdapter()
        >>> adapter.setup()

        Add a record:

        >>> record_to_save  = {"username":"Max"}
        >>> saved_id = adapter.save_message({"username":"Max"})

        Delete the added record:

        >>> record_to_delete = {"username":"Max"}
        >>> record_by_id = {"_id": saved_id}

        >>> del_id = adapter.del_message(record_to_delete)
        >>> del2_id = adapter.del_message(record_by_id)

        >>> assert del_id == del2_id

        Configuration Parameters
        ======

        - **host** - An address of MongoDB instance. Can use FQDN or IP-address.
        - **port** - A port of MongoDB instance.
        - **db_user** - An username to connect.
        - **db_password** - A password to authenticate the user.
        - **db_name** - A default name of Database collection
        - **collection_name** - Default collection name to store data from sensors

    """

    def __init__(self):

        # Use connection parameters from default configuration

        self.host = CONFIG['storage']['host']
        self.port = int(CONFIG['storage']['port'])

        self._username = CONFIG['storage']['db_user']
        self._password = CONFIG['storage']['db_password']

        self.db_name = CONFIG['storage']['db_name']
        self.collection_name = CONFIG['storage']['collection_name']

        self.is_initialized = False

    def _connect(self) -> bool:

        """
            Establish connection to MongoDB instance with provided parameters.

        :returns:
         :return: True if connection is successful.
        :raises:
         :raise ConnectionFailure if connection is timed out.
        """

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
            # Save our connection if try block went without errors
            self._db_conn = connection[self.db_name]
            self.is_initialized = True

            return True

    def setup(self) -> bool:

        logger.info("Setting up StorageAdapter")
        # Try to establish connection to MongoDB.
        res = self._connect()

        # If established, then mark itself as successfully initialized.
        if res:
            self.is_initialized = True

        return res

    def save_message(self, message: dict) -> str:

        """
            Add a JSON Python dictionary in MongoDB database

        :param message: A Python dictionary
        :return: An ID of saved record. If _id is not presented in the record, then it will be set
         automatically by MongoDB.
        """

        # Check if message indeed is dictionary
        if not isinstance(message,dict):
            raise TypeError('Message must be dictionary')

        # Check if not initialized yet
        if not self.is_initialized:
            raise EnvironmentError("Please, setup StorageAdapter before first usage!")

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Save record and return ID of the saved record
        res_id = collection.insert_one(message).inserted_id

        logger.debug(f"Saved a record with id '{res_id} in collection '{self.collection_name}'")

        return res_id

    def del_message(self, message: dict) -> str:

        """
            Delete a record by specified filter.

        :param message: A Python dictionary which represent either the record itself or fields to first find the record
            and delete it.
        :return: An ID of deleted record. if not fould, then return None
        """

        # Check if message indeed is dictionary
        if not isinstance(message,dict):
            raise TypeError('Message must be dictionary')

        # Check if not initialized yet
        if not self.is_initialized:
            raise EnvironmentError("Please, setup StorageAdapter before first usage!")

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Find, delete and return _id of
        res_id = collection.find_one_and_delete(message).get("_id",None)
        if res_id is not None:
            logger.debug(f"Delete a record with ID '{res_id}' in collection '{self.collection_name}'")
        else:
            logger.debug(f"A record with ID '{res_id}'  to be deleted in collection '{self.collection_name}' is "
                         f"not found.")
        return res_id

    def get_all_messages(self) -> List[Dict]:

        """
            Fetch all records in database for connection_name.

        :return: A list of Python dictionaries
        """

        # Check if not initialized yet
        if not self.is_initialized:
            raise EnvironmentError("Please, setup StorageAdapter before first usage!")

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Convert from cursor iterator to list
        records = list(collection.find({}))

        logger.debug(f"Fetched {len(records)} records from {self.collection_name}.")

        return records

