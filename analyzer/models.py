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

    def run_estimation(self, start_time: datetime, end_time: datetime, expected_uavs_number = 2, ):

        """
        Executes one optimization step and save the result in the DB.

        The function will prepare all required data for running the specified solver with initial parameters.

        :param start_time: The left bound datetime for initial data fetching
        :param end_time: The right bound datetime for initial data fetching
        :param expected_uavs_number: The number of UAVs' optimized locations to create. Implicitly means to *n_clusters*.

        :return: None
        """

        # Fetch and prepare only the last positions in the specified time range
        records = self.store.get_aggr_per_client(start_time, end_time)
        logging.info(f"Received info for {len(records)} UEs ")

        # Check if we have data to process
        if records and len(records)>0:

            # Prepare data in format [(x1,y1)]
            data_rows = []

            for record in records:
                last_record = record['data'].pop()

                only_last_position = (last_record['latitude'], last_record['longitude'])

                data_rows.append(only_last_position)

            # Ask solver to estimate the location for UAVs
            logger.info("Start the estimation process for UAVs' locations.")
            optimized_results = self.solver.solve(
                nodes_locations=data_rows,
                # May be the case that you have n_clusters more than available data
                n_clusters=min(len(data_rows), expected_uavs_number)
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
                    } for x in optimized_results]
                }
            }

            logger.debug("The saved record will be:")
            logger.debug(estimation)

            self.store.add_estimation(estimation)

        pass
