# Python library import
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Tuple, Any
import dateutil.parser
import datetime

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
            * save - take and store a message in DB.
            * delete - take an item by a Record Identification (may be different, either built-in, like _id, or manually added.

    """

    @abstractmethod
    def save(self, message: dict) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete(self, ident: Any) -> bool:
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

        self.host = os.environ.get('MONGODB_HOST') or CONFIG['mongodb']['host']
        self.port = int( os.environ.get('MONGODB_PORT') or CONFIG['mongodb']['port'])

        self._username = os.environ.get('MONGODB_DB_USER') or CONFIG['mongodb']['db_user']
        self._password = os.environ.get('MONGODB_DB_USERPASS') or CONFIG['mongodb']['db_password']

        self.db_name = os.environ.get('MONGODB_DB_NAME') or CONFIG['mongodb']['db_name']
        self.collection_name = os.environ.get('MONGODB_DEFAULT_COLLECTION') or CONFIG['mongodb']['collection_name']

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

            logger.debug(f"Try to establish connection to MongoDB instance on {self.host}:{self.port} as "
                         f"'{self._username}' ")

            connection = pymongo.MongoClient("mongodb://%s:%s@%s:%s" % (
                self._username,
                self._password,
                self.host,
                self.port,
            ))

            # Ensure that we connected
            _data = connection.server_info()
            logger.info(f"Connected to {_data}", )

        except ConnectionFailure as e:
            raise ConnectionError(f"Cannot connect to MongoDB instance at {self.host}:{self.port}!") from e
        else:
            # Save our connection if try block went without errors
            self._db_conn = connection[self.db_name]

    def save(self, message: dict, collection_name: str = None) -> str:

        """
            Add a JSON Python dictionary in MongoDB database

        :param message: A Python dictionary
        :param collection_name: A name of collection to write a message to. Default is None. if None,
        then use default collection_name.
        :return: An ID of saved record. If _id is not presented in the record, then it will be Tuple
         automatically by MongoDB.
        """

        # Check if message indeed is dictionary
        if not isinstance(message, dict):
            raise TypeError('Message must be dictionary')

        # Get collection to write to
        if collection_name is None:
            collection_name = self.collection_name

        collection = self._db_conn[collection_name]

        # Save record and return ID of the saved record
        res_id = collection.insert_one(message).inserted_id

        logger.debug(f"Saved a record with id '{res_id} in collection '{self.collection_name}'")

        return str(res_id)

    def delete(self, message: dict, collection_name: str = None) -> str:

        """
            Delete a record by record itself.

        :param message: A Python dictionary which represent either the record itself or fields to first find the record
            and delete it.
        :param collection_name: A name of collection to delete a message from. Default is None.
        if None, then use default collection_name.
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
        return str(res_id)

    def get_raw_msgs(self) -> List[Dict]:

        """
            Fetch all records in database for connection_name.
            Records are returned as they stored in the DB, e.g. in 'raw' format.

        :return: A list of Python dictionaries
        """

        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Convert from cursor iterator to list
        records = list(collection.find({}))

        logger.debug(f"Fetched {len(records)} records from {self.collection_name}.")

        return records

    def get_last_raw_msgs(self) -> dict:

        """
            Return the last saved message (with the newest date) for each of clients.
            Records are returned as they stored in the DB, e.g. in 'raw' format.

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

        >>> db.data
        >>> .aggregate([
        >>>     {"$sort": {"time": -1}},
        >>>     {
        >>> $group: {
        >>>     _id: "$device.id",
        >>>     device: { $first: "$$ROOT"}
        >>>
        >>> }
        >>> }])

        :return: A saved JSON Python dictionary
        """
        # Get collection to write to
        collection = self._db_conn[self.collection_name]

        # Convert from cursor iterator to list
        records = list(collection.aggregate([{"$sort": {"time": -1}},
                                             {"$group": {"_id": "$device.id", "device": {"$first": "$$ROOT"}}}]))
        records = [r['device'] for r in records]

        logger.debug(f"Fetched {1} records from {self.collection_name}.")

        return records

    def get_clients_list(self) -> List[str]:

        """
            Returns ID for all registered clients.

            Registration for an ID means there is at least one message is received with the ID.

        :return: list of str
        """

        collection = self._db_conn[self.collection_name]

        # Convert from cursor iterator to list
        clients = collection.aggregate([
            {"$sort": {"time": -1}},
            {"$group": {"_id": "$device.id"}},
            {"$project": {"_id": 0, "device.id": "$_id"}}
        ])

        return list(clients)

    def add_estimation(self, record: dict) -> str:

        """
            Save an estimation generated from Analyzers classes (inherited from AbstractAnalyzer).

            .add_estimation implicitly uses .save() method with different collection_name.

        :param record:
        :return:
        """

        # Use custom name to save estimation in a different collection
        collection_name = 'estimations'

        return self.save(record, collection_name)

    def get_raw_estimations(self, start_date=None, end_date=None, *args, **kwargs) -> List[Dict]:

        """
            Return all computed estimations
        :return: estimations as they are stored in the DB.
        """

        # Parse time boundaries if possible
        try:
            start_date = dateutil.parser.parse(start_date)
            end_date = dateutil.parser.parse(end_date)
        except:
            start_date = datetime.datetime.now() - datetime.timedelta(days=1)
            end_date = datetime.datetime.now()

        # Use custom name to fetch estimation
        collection_name = 'estimations'

        # Get collection to read from
        collection = self._db_conn[collection_name]

        # Convert from cursor iterator to list
        records = collection.find({
            "time": {
                "$lt": end_date,
                "$gte": start_date

            }
        }).sort('time', -1)

        return list(records)

    def get_aggr_per_client(self, limits=20, start_date=None, end_date=None, *args, **kwargs) -> List[Dict]:

        """
            Returns records aggregated per a client.
            Records are filtered to be "wifi" message_type.

            For each of clients there is information

            - time of record
            - received RSSI signal
            - longitude
            - latitude

        :param limits: set the maximum number of records for a client is returned. If -1, then all records will be returned.
        :return:
        """

        # Parse time boundaries if possible
        try:
            start_date = dateutil.parser.parse(start_date)
            end_date = dateutil.parser.parse(end_date)
        except:
            start_date = datetime.datetime.now() - datetime.timedelta(days=1)
            end_date = datetime.datetime.now()

        # Get collection to read from
        collection = self._db_conn[self.collection_name]

        # Convert from cursor iterator to list

        records = collection.aggregate([{"$sort": {"time": -1}},
                                        {"$match": {"message_type": "wifi",
                                                    "time": {
                                                        "$gte": start_date,
                                                        "$lt": end_date
                                                    }
                                                    }},
                                        {"$group": {"_id": "$device.id",
                                                    "data":
                                                        {"$push": {"time": "$time",
                                                                   "latitude": "$latitude",
                                                                   "longitude": "$longitude",
                                                                   "signal": "$payload.signal.rssi",
                                                                   "ap": "$payload.bssi",

                                                                   },
                                                         },

                                                    }
                                         },
                                        {"$project": {
                                            "_id": 0,
                                            "device.id": "$_id",
                                            "data": {"$slice": ["$data", limits]}
                                        }},
                                        {"$sort": {"device.id": 1, "device.data.time": 1}},
                                        ])

        return list(records)
