import sys

import time
import datetime

from analyzer.models import UAVEstimator

SLEEP_TIME = 5
UAVS_NUM = 10

if __name__ == '__main__':

    try:

        runner: UAVEstimator = UAVEstimator()

        start_date = datetime.datetime.now() - datetime.timedelta(hours=1)
        end_date = datetime.datetime.now()

        while True:

            runner.run_estimation(start_date,end_date,UAVS_NUM)
            time.sleep(SLEEP_TIME)

    except KeyboardInterrupt:
        sys.exit(0)