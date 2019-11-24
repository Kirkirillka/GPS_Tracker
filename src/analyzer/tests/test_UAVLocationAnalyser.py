from unittest import TestCase

from analyzer.models import UAVLocationAnalyzer
from analyzer.placement.solvers.utils import OptimizationScenario


class TestUAVLocationAnalyser(TestCase):

    def test_analyze_uavs_pos(self):

        test_scenario = OptimizationScenario()
        test_scenario.random_init(num_nodes=2, num_uavs=1, base_num=1, method="simplex")

        analyzer = UAVLocationAnalyzer()
        res = analyzer.analyze(test_scenario)

        self.assertTrue(isinstance(res, list))

