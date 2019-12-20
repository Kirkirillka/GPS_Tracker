import datetime, time

from analyzer.placement.solvers.models import UAVPositionSolver
from storage.models import MongoDBStorageAdapter

# Logging section
import logging.config
from utils.logs.tools import read_logging_config

logging.config.dictConfig(read_logging_config())
logger = logging.getLogger(__name__)


class UAVSolverRunner:
    """
        Class UAVSolverRunner is responsible for running Analyzers in production.

        Having an Analyzer instance, AnalyzeRunner supply all necessary params for .analyze
        method, save the result in the DB.

        Besides, is responsible for continuous running of algorithm in order to provide stream-based
        analysis pipeline.

        Strictly dependent on concrete MongoDBStorageAdapter logic.

    """

    # For what kind of objects analysis is made
    TARGET = "uav"

    # What the Analyzer tries to do
    MESSAGE_TYPE = "estimation"

    def __init__(self, method_name='clustering', n_clusters = 2):

        # How long to wait between each analysis steps
        self.base_wait_time = 10

        # Init connection to a DB
        self.store = MongoDBStorageAdapter()
        self.solver = UAVPositionSolver(method_name)

        # Default params
        self.__methods = method_name
        self.__n_clusters = n_clusters

    def loop(self):

        # Enter loop
        logging.info(f"Starting loop in {__class__}")
        while True:

            # Phase 1. Fetch and prepare the client's UE last positions
            records = self.store.get_aggr_per_client()
            logging.info(f"Received info for {len(records)} UEs ")

            # Check if we have data to process
            if records:

                # Prepare data in format [(x1,y1)]
                data_rows = []

                for record in records:
                    last_record = record['data'].pop()

                    only_last_position = (last_record['latitude'], last_record['longitude'])

                    data_rows.append(only_last_position)

                # Phase 2. Ask solver to optimize
                logging.info("Start optimization ")
                optimized_results = self.solver.solve(
                    nodes_locations=data_rows,
                    # May be the case that you have n_clusters more than available data
                    n_clusters = min(len(data_rows),self.__n_clusters)
                )

                # Phase 3. Save bulk into Storage
                logging.info("Analysis is done. Now preparing the result to be stored in the Storage.")

                # Anchor to the current time
                estimation_time = datetime.datetime.now()

                # Enrich data with clients (device) ID and time for estimation
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

                logging.debug("The analysis result is:")
                logging.debug(estimation)

                self.store.add_estimation(estimation)

            # Phase 4. Sleep
            logging.info(f"The cycle is ended. Sleep for {self.base_wait_time} seconds.")
            time.sleep(self.base_wait_time)
