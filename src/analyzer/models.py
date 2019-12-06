from abc import ABC, abstractmethod
from typing import Any

import datetime, time

from analyzer.placement.solvers.utils import OptimizationScenario
from analyzer.placement.solvers.models import UAVPositionSolver

from storage.models import MongoDBStorageAdapter

# Logging section
import logging.config
from utils.logs.tools import read_logging_config
logging.config.dictConfig(read_logging_config())
logger = logging.getLogger(__name__)


class AbstractAnalyzer(ABC):
    """
    Class **AbstractAnalyzer** defines main methods and attributes that will have every Analyzer.

    Every *Analyzer* is a object that gets information from Storage via StorageAdapter, process the data somehow, and saves
    the result into Storage back.



    Methods
    ----------

    - analyze (data: OptimizationScenario): Perform one analysis step.

    """

    @abstractmethod
    def analyze(self, data: Any):
        raise NotImplementedError


class UAVLocationAnalyzer(AbstractAnalyzer):
    """
    Performs analysis on the best placement for UAVs.
    As optimization technique, use the power of UAVPositionSolver's optimization interface.
    """

    # For what kind of objects analysis is made
    TARGET = "uav"

    # What the Analyzer tries to do
    MESSAGE_TYPE = "estimation"

    def analyze(self, scenario: OptimizationScenario):
        # ask solver to estimate the optimum position for UAVs
        solver = UAVPositionSolver(scenario)
        optimized_uavs_pos = solver.solve()

        return optimized_uavs_pos


class AnalyzerRunner:
    """
        Class AnalyzerRunner is responsible for running Analyzers in production.

        Having an Analyzer instance, AnalyzeRunner supply all necessary params for .analyze
        method, save the result in the DB.

        Besides, is responsible for continuous running of algorithm in order to provide stream-based
        analysis pipeline.

        Strictly dependent on concrete MongoDBStorageAdapter logic.

    """



    @property
    def wait_time(self):
        # Analyze each 1 second
        return self.base_wait_time

    def __init__(self, analyzer: UAVLocationAnalyzer):

        # How long to wait between each analysis steps
        self.base_wait_time = 10

        # Init connection to a DB
        self.store = MongoDBStorageAdapter()
        self.analyzer = analyzer

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

                # Phase 3. Prepare OptimizationScenario
                logging.info("Starting preparing an optimization scenario")
                scenario = OptimizationScenario()
                scenario.random_init(
                    num_nodes=len(data_rows),
                    num_uavs=min(len(data_rows),2),
                    base_num=1)

                scenario.nodes_locations = data_rows
                logging.debug("The optimization scenario is:")
                logging.debug(scenario)

                # Phase 2. Ask solver to optimize
                logging.info("Start analysis of the formed scenario.")
                optimized_results = self.analyzer.analyze(scenario)

                # Phase 3. Save bulk into Storage
                logging.info("Analysis is done. Now preparing the result to be stored in the Storage.")

                # Anchor to the current time
                estimation_time = datetime.datetime.now()

                # Enrich data with clients (device) ID and time for estimation
                estimation = {
                    "time": estimation_time,
                    "message_type": self.analyzer.MESSAGE_TYPE,
                    "payload": {
                        "method": scenario.method,
                        "target": self.analyzer.TARGET,
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
            logging.info(f"The cycle is ended. Sleep for {self.wait_time} seconds.")
            time.sleep(self.wait_time)
