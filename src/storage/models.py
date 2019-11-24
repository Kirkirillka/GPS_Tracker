# Python library import
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any

# 3-td party libraries
import pymongo
from pymongo.errors import ConnectionFailure

# Project modules
from config.utils import get_project_config

# Logging section
import logging.config
from utils.logs.tools import read_logging_config
logging.config.dictConfig(read_logging_config())
logger = logging.getLogger(__name__)

# Project configuration
CONFIG = get_project_config()


class AbstractStorageAdapter(ABC):
    """
        Class AbstractStorageAdapter is an abstract class to define the interface to access Storage, however of what
        exactly DB is used.


        Members
        ======
            * get_all_msgs - return a list of saved messages in <key-value> format.
            * get_last_msgs - return the last received messages (sort by time arrived) from clients in <key-value> format.
            * get_coords_by_client_id - get all messages for specific client_id, return a path of coordinates.
            * get_last_coords - get the last received messages from clients, return their coordinates.
            * get_clients - find all unique clients ID in messages and return them.
            * save - take and store a message in DB.
            * delete - take an item by a Record Identification (may be different, either built-in, like _id, or manually added.

    """

    @abstractmethod
    def get_all_msgs(self) -> List[dict]:

        raise NotImplementedError

    @abstractmethod
    def get_last_msgs(self) -> List[dict]:

        raise NotImplementedError

    @abstractmethod
    def get_coords_by_client_id(self) -> List[Tuple[float, float]]:

        raise NotImplementedError

    @abstractmethod
    def get_last_coords(self) -> Dict[str, List[Tuple[float, float]]]:

        raise NotImplementedError

    @abstractmethod
    def save(self, message: dict) -> bool:

        raise NotImplementedError

    @abstractmethod
    def delete(self, ident: Any) -> bool:

        raise NotImplementedError

    @abstractmethod
    def get_clients(self) -> List[str]:

        raise NotImplementedError


class MongoDBStorageAdapter(AbstractStorageAdapter):
    """
        Class StorageAdapter

        This class to contain convenient interface to access MongoDB Database.

        To connect to MongoDB instance, **StorageAdapter** uses configuration parameters under *[storage]* section in
        default *config.ini*

        Examples
        =======

        Perform connection to DB:

        >>> adapter = MongoDBStorageAdapter()

        Add a record:

        >>> record_to_save  = {"username":"Max"}
        >>> saved_id = adapter.save({"username":"Max"})

        Delete the added record:

        >>> record_to_delete = {"username":"Max"}
        >>> record_by_id = {"_id": saved_id}

        >>> del_id = adapter.delete(record_to_delete)
        >>> del2_id = adapter.delete(record_by_id)

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

        # Setup connection to DB
        self._connect()

    def _connect(self) -> None:

        """
            Establish connection to MongoDB instance with provided parameters.

        :returns:
         :return: None if no errors occurred.
        :raises:
         :raise ConnectionFailure if connection is timed out.
        """

        try:

            logger.info(f"Try to establish connection to MongoDB instance on {self.host}:{self.port} as "
                        f"'{self._username}' ")

            connection = pymongo.MongoClient("mongodb://%s:%s@%s:%s" % (
                self._username,
                self._password,
                self.host,
                self.port,
            ))

            # Ensure that we connected
            _data = connection.server_info()
            logger.debug(f"Connected to {_data}", )

        except ConnectionFailure as e:
            raise ConnectionError(f"Cannot connect to MongoDB instance at {self.host}:{self.port}!") from e
        else:
            # Save our connection if try block went without errors
            self._db_conn = connection[self.db_name]

    def get_last_coords(self) -> Dict[str, List[Tuple[float, float]]]:

        raise NotImplementedError

    def get_coords_by_client_id(self) -> List[Tuple[float, float]]:

        raise NotImplementedError

    def get_all_msgs(self) -> List[Dict]:

        """
            Fetch all records in database for connection_name.

        :return: A list of Python dictionaries
        """

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Convert from cursor iterator to list
        records = list(collection.find({}))

        logger.debug(f"Fetched {len(records)} records from {self.collection_name}.")

        return records

    def get_last_msgs(self) -> dict:

        """
            Return the last saved message (with the newest date) for each of clients.

            Example
            ======

            There are three clients with "device.id" = [1,2,3]. There are three records for each of clients in the
            time points:

            - 2019-11-12T15:30:09.510003
            - 2019-11-12T15:30:10.2341
            - 2019-11-12T15:30:10.344

            The returned value must be something like:

            [
                {
                ...
                date: "2019-11-12T15:30:10.344",
                    "device": {
                        "id" = 1
                        ...
                    }
                    ...
                },
                {
                ...
                date: "2019-11-12T15:30:10.344",
                    "device": {
                        "id" = 2
                        ...
                    }
                    ...
                },
                {
                ...
                date: "2019-11-12T15:30:10.344",
                    "device": {
                        "id" = 3
                        ...
                    }
                    ...
                }
            ]

        Where "..." means there are other fields contained in the scheme.


        :return: A saved JSON Python dictionary
        """

        # TODO: Implement MongoDBStorageAdapter.get_last_message

        raise NotImplementedError

    def get_clients(self) -> List[str]:

        """
            Returns "device.id" from all stored messages
        :return:
        """

        collection = self._db_conn[self.collection_name]

        clients = collection.find({}, {"device.id": 1})

        # Fetch 'device.id' field and trasform into list
        clients = [r['device']['id'] for r in clients]

        return list(clients)

    def save(self, message: dict) -> str:

        """
            Add a JSON Python dictionary in MongoDB database

        :param message: A Python dictionary
        :return: An ID of saved record. If _id is not presented in the record, then it will be Tuple
         automatically by MongoDB.
        """

        # Check if message indeed is dictionary
        if not isinstance(message, dict):
            raise TypeError('Message must be dictionary')

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Save record and return ID of the saved record
        res_id = collection.insert_one(message).inserted_id

        logger.debug(f"Saved a record with id '{res_id} in collection '{self.collection_name}'")

        return res_id

    def delete(self, message: dict) -> str:

        """
            Delete a record by record itself.

        :param message: A Python dictionary which represent either the record itself or fields to first find the record
            and delete it.
        :return: An ID of deleted record. if not fould, then return None
        """

        # Check if message indeed is dictionary
        if not isinstance(message, dict):
            raise TypeError('Message must be dictionary')

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Find, delete and return _id of
        res_id = collection.find_one_and_delete(message).get("_id", None)
        if res_id is not None:
            logger.debug(f"Delete a record with ID '{res_id}' in collection '{self.collection_name}'")
        else:
            logger.debug(f"A record with ID '{res_id}'  to be deleted in collection '{self.collection_name}' is "
                         f"not found.")
        return res_id

    def add_estimation(self, record: dict) -> bool:

        """
            Save an estimation generated from Analyzers classes (inherited from AbstractAnalyzer).

            // TODO: 24.11.2019. Describe the requirement for the function and implement this.

        :param record:
        :return:
        """

        raise NotImplementedError
