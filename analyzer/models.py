import datetime

from placement.solvers.models import UAVPositionSolver
from storage.models import MongoDBStorageAdapter

# Logging section
import logging
logger = logging.getLogger(__name__)


class UAVEstimator:
    """
        Class UAVEstimator is responsible to provide an API to run and save the result of optimization of
        *UAVPositionSolver*. Strictly dependent on concrete *MongoDBStorageAdapter* logic.

        Attributes:

            TARGET: the name of current estimator aim used for generation the estimation result message.
            MESSAGE_TYPE: the name used for *target* in the payload field in MQTT messages.

        :param method_name: an optimization method used to run an estimater. Default is `clustering`. The methods
            must be registered in the module properly.

    """

    # For what kind of objects analysis is made
    TARGET = "uav"

    # What the Analyzer tries to do
    MESSAGE_TYPE = "estimation"

    def __init__(self, method_name='clustering'):

        # Init connection to a DB
        self.store = MongoDBStorageAdapter()

        # Main solver
        self.solver = UAVPositionSolver(method_name)

        # Estimation parameters
        # We expect to receive only one position for each UE
        self.window_size = 1

    def run_estimation(self, start_time: datetime, end_time: datetime, expected_uavs_number = 2, **kwargs):

        """
        Executes one optimization step and save the result in the DB.

        The function will prepare all required data for running the specified solver with initial parameters.

        :param start_time: The left bound datetime for initial data fetching
        :param end_time: The right bound datetime for initial data fetching
        :param expected_uavs_number: The number of UAVs' optimized locations to create. Implicitly means to *n_clusters*.

        :keyword explicit_ues_locations: a list of predefined locations for UES in format [(x,y),(x,y)...]

        :return: None
        """

        # Check if ues last position are defined explicitly
        records = kwargs.get("explicit_ues_locations", None )
        # If not, then use last known position from the database for the specified date range
        if records is None:
            # Fetch and prepare only the last positions in the specified time range
            records = self.store.get_aggr_per_client(start_time, end_time)

            # Prepare data in format [(x1,y1)]
            data_rows = []

            for record in records:
                last_record = record['data'].pop()

                only_last_position = (last_record['latitude'], last_record['longitude'])

                data_rows.append(only_last_position)

            records = data_rows

        # Check if we have data to process
        if isinstance(records, list) and len(records)>0:

            logging.info(f"Received info for {len(records)} UEs ")
            logger.info("Start the estimation process for UAVs' locations.")

            # Ask solver to estimate the location for UAVs
            ues_num = len(records)

            logger.info(f"Available number of UEs' records: '{ues_num}'")
            logger.info(f"Expected number of UAVs: '{expected_uavs_number}'")

            # Check if required num_clusters in higher than possible UEs clients
            if expected_uavs_number > ues_num :
                logger.info(f"The provided number of expected UAVs '{expected_uavs_number}' is higher than available "
                            f"UEs' records - '{ues_num}'! Use the minimal possible value. ")
            optimized_results = self.solver.solve(
                nodes_locations=records,
                # May be the case that you have n_clusters more than available data
                n_clusters=min(ues_num, expected_uavs_number)
            )

            # Save bulk into the storage
            logger.info("Estimation is done.")
            logger.info("Preprocess the result to be stored in the storage.")

            # Anchor to the current time
            estimation_time = datetime.datetime.now()

            # Extend the returning data with clients (device) ID and time for estimation
            estimation = {
                "time": estimation_time,
                "message_type": self.MESSAGE_TYPE,
                "payload": {
                    "method": self.solver.optimization_method,
                    "target": self.TARGET,
                    "suggested": [{
                        "latitude": x[0],
                        "longitude": x[1],
                    } for x in optimized_results],
                    "ues_location": records
                }
            }

            logger.debug("The saved record will be:")
            logger.debug(estimation)

            self.store.add_estimation(estimation)

            return True

        else:
            logger.error("Problems with input location data  for UEs for estimation!")
            return False
