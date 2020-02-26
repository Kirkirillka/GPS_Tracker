# Python library import
import os
from abc import ABC, abstractmethod
from typing import List, Dict, Any

import datetime
from datetime import datetime as DateTimeClass
from utils.tools import datetime_parse

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
DEFAULT_CONFIG = get_project_config()


class AbstractStorageAdapter(ABC):
    """
        Class AbstractStorageAdapter is an abstract class to define the interface to access Storage, however of what
        exactly DB is used.


        Members
        ======
            * save - take and store a message in DB.
            * delete - take an item by a Record Identification (may be different, either built-in, like _id, or manually
            added.

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

        To connect to MongoDB instance, :py:class:`StorageAdapter` uses configuration parameters
        provided by :py:attr:`DEFAULT_CONFIG` or by OS environment.

        The class takes parameters from the config provided by **DEFAULT_CONFIG**. Other way is to define OS environment
        variables to adjust the behaviour.

        :param string MONGODB_HOST: An address of MongoDB instance. Can use FQDN or IP-address.
        :param int MONGODB_PORT: A port of MongoDB instance.
        :param string MONGODB_DB_USER:  An username to connect.
        :param string MONGODB_DB_USERPASS: A password to authenticate the user.
        :param string MONGODB_DB_NAME: A default name of Database collection.
        :param string MONGODB_DEFAULT_COLLECTION: Default collection name to store data from sensors.

        Examples:

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

        Attributes:

        :param host: An address of MongoDB instance. Can use FQDN or IP-address.
        :param port: port A port of MongoDB instance.
        :param db_user: An username to connect.
        :param db_password: A password to authenticate the user.
        :param db_name: A default name of Database collection.
        :param collection_name: Default collection name to store data from sensors.

    """

    def __init__(self):

        # Use connection parameters from default configuration

        self.host = os.environ.get('MONGODB_HOST') or DEFAULT_CONFIG['mongodb']['host']
        self.port = int(os.environ.get('MONGODB_PORT') or DEFAULT_CONFIG['mongodb']['port'])

        self._username = os.environ.get('MONGODB_DB_USER') or DEFAULT_CONFIG['mongodb']['db_user']
        self._password = os.environ.get('MONGODB_DB_USERPASS') or DEFAULT_CONFIG['mongodb']['db_password']

        self.db_name = os.environ.get('MONGODB_DB_NAME') or DEFAULT_CONFIG['mongodb']['db_name']
        self.collection_name = os.environ.get('MONGODB_DEFAULT_COLLECTION') or DEFAULT_CONFIG['mongodb']['collection_name']

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
        records = list(collection.find({}, {"_id": 0}))

        logger.debug(f"Fetched {len(records)} records from {self.collection_name}.")

        return records

    def get_last_raw_msgs(self) -> List[Dict]:

        """
        Return the last saved message (with the newest date) for each of clients.
        Records are returned as they stored in the DB, e.g. in 'raw' format.

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

        :param record: a dict structure which must fit a JSON Schema for that type of message.
        :return:
        """

        # Use custom name to save estimation in a different collection
        collection_name = 'estimations'

        return self.save(record, collection_name)

    def get_all_estimations(self, *args, **kwargs) -> List[Dict]:

        """
            Return all computed estimations

        :raises:
            :raise ValueError: the provided start_date or end_date couldn't be parsed.

        :return: estimations as they are stored in the DB.
        """

        # Use custom name to fetch estimation
        collection_name = 'estimations'

        # Get collection to read from
        collection = self._db_conn[collection_name]

        # Convert from cursor iterator to list
        records = collection.find({}).sort('time', -1)

        return list(records)

    def get_recent_estimation(self, *args, **kwargs):

        """
            Return the most recent estimation
        :param args: list of arguments
        :param kwargs: dict of arguments
        :return: a Python dictionary
        """

        # Fetch all estimations
        all_estimation = self.get_all_estimations(*args, **kwargs)

        # Check if we have any estimations
        if len(all_estimation) > 0:
            # Then return only the first one
            recent_estimation = all_estimation.pop(0)
        else:
            recent_estimation = {}

        return recent_estimation

    def get_aggr_per_client(self, start_date: DateTimeClass = None, end_date: DateTimeClass = None, limits=20,
                            *args, **kwargs) -> List[Dict]:

        """
        Returns records aggregated per a client.

        Records are filtered to be "wifi" message_type. For each of clients there is the information contains:

        - time of record
        - received RSSI signal
        - longitude
        - latitude
        - downlink speed estimation
        - uplink speed estimation


        :param start_date: the leftmost boundary for fetching data from DB. if not specified, the current datetime - 1
        day is used.
        :param end_date: the rightmost boundary for fetching data from DB. if not specified, the current datetime.
        :param limits: set the maximum number of records for a client is returned. If -1, then all records will
            be returned.

        :raises:
            :raise ValueError: the provided start_date or end_date couldn't be parsed.

        :return: a list of coordinates, united in dictionaries => List[Dict]

        """

        # Parse time boundaries if possible
        if start_date is not None and end_date is not None:
            start_date = datetime_parse(start_date)
            end_date = datetime_parse(end_date)
        else:
            logger.error("The start and end dates are not specified. Use the default parameters.")
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
                                                                   "downlink": "$payload.downSpeed",
                                                                   "uplink": "$payload.upSpeed"
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

    def get_db_stats(self) -> List[Dict[str, int]]:

        """
        Returns information about the number of received messages for each collection, specified in 'collections'.

        Example
        =======

        A command **adapter.get_db_stats()** may return:
        
        - {'messages' : 23, 'estimations': 4}

        :return: a Python dictionary
        """

        # collection to calculate statistics for
        collections = self._db_conn.list_collection_names({})

        msg_counts = []

        for col_name in collections:
            collection = self._db_conn[col_name]

            count = collection.count_documents({})

            new_record = {"name": col_name, 'count': count}

            msg_counts.append(new_record)

        return msg_counts
