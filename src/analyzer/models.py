from abc import ABC, abstractmethod
import yaml
import datetime

from analyzer.placement_algorithm_example.solvers.utils import OptimizationScenario
from analyzer.placement_algorithm_example.solvers.models import UAVPositionSolver

from storage.models import MongoDBStorageAdapter

class AbstractAnalyzer(ABC):

    """
    Class **AbstractAnalyzer** defines main methods and attributes that will have every Analyzer.

    Every *Analyzer* is a object that gets information from Storage via StorageAdapter, process the data somehow, and saves
    the result into Storage back.

    Properties
    ----------

    wait_time: int
        returns a time in seconds to wait after each processing step.


    Methods
    ----------

    - loop: None
        Start a continuous loop in which it fetches data, makes an analysis, and saves the result.

    """

    @property
    @abstractmethod
    def wait_time(self):
        """
            returns a time in seconds to wait after each processing step.

        :return: int
        """

        raise NotImplementedError

    @abstractmethod
    def loop(self):

        """
            Start a continuous loop in which it fetches data, makes an analysis, and saves the result

        :return: None
        """

        raise  NotImplementedError


class BestLocationAnalyser(AbstractAnalyzer):

    MESSAGE_TYPE = "estimation"

    def __init__(self):

        # Read config from YAML
        with open("config.yml") as file:
            config = yaml.safe_load(file)

            scenario = OptimizationScenario(**config)

            self.scenario = scenario

        # Init connection to a DB
        self.store = MongoDBStorageAdapter()

    @property
    def wait_time(self):
        # Analyze each 1 second
        return 1

    def analyze_uavs_pos(self, last_coords: dict):

        # Prepare data in format [(x1,y1)]
        only_positions = [(record['latitude'], record['longitude']) for record in last_coords]

        # update local copy of optimization scenario
        current_scenario = self.scenario.copy()
        current_scenario.nodes_locations = only_positions

        # ask solver to estimate the optimum position for UAVs
        solver = UAVPositionSolver(**self.scenario)
        optimized_uavs_pos = solver.solve()

        # Enrich data with clients (device) ID and time for estimation
        databulk = [{
            "time": datetime.datetime.now(),
            "type": self.MESSAGE_TYPE,
            "payload":{
                "method": self.scenario.method,
                "target": "uav",
                "latitude": r[0],
                "longitude": r[1]
            }
        } for r in optimized_uavs_pos]

        return databulk




    def loop(self):

        # Enter loop
        while True:

            # Phase 1. Fetch and prepare the client's UE last positions
            records = self.store.get_last_coords()

            ## Phase 2. Ask solver to optimize
            bulk = self.analyze_uavs_pos(records)

            ## Phase 3. Save bulk into Storage
            for estimation in bulk:

                self.store.add_estimation
