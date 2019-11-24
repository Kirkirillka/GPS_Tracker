from abc import ABC, abstractmethod
from typing import Any

import datetime, time

from placement.solvers.utils import OptimizationScenario
from placement.solvers.models import UAVPositionSolver

from storage.models import MongoDBStorageAdapter


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

    TARGET = "uav"
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

    BASE_WAIT_TIME = 0.5

    @property
    def wait_time(self):
        # Analyze each 1 second
        return self.BASE_WAIT_TIME

    def __init__(self, analyzer: UAVLocationAnalyzer):

        # Init connection to a DB
        self.store = MongoDBStorageAdapter()
        self.analyzer = analyzer

    def loop(self):

        # Enter loop
        while True:

            # Phase 1. Fetch and prepare the client's UE last positions
            records = self.store.get_last_coords()

            # Prepare data in format [(x1,y1)]
            only_positions = [(record['latitude'], record['longitude']) for record in records]

            # Phase 2. Ask solver to optimize
            optimized_results = self.analyzer.analyze(only_positions)

            # Phase 3. Save bulk into Storage

            # Anchor to the current time
            estimation_time = datetime.datetime.now()

            # Enrich data with clients (device) ID and time for estimation
            databulk = [{
                "time": estimation_time,
                "message_type": self.MESSAGE_TYPE,
                "payload": {
                    "method": self.analyzer.scenario.method,
                    "target": self.analyzer.TARGET,
                    "latitude": r[0],
                    "longitude": r[1]
                }
            } for r in optimized_results]


            for estimation in databulk:
                self.store.add_estimation(estimation)

            # Phase 4. Sleep
            time.sleep(self.analyzer.wait_time)