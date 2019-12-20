import sys

from analyzer.models import UAVSolverRunner

if __name__ == '__main__':

    try:

        runner: UAVSolverRunner = UAVSolverRunner()

        runner.loop()
    except KeyboardInterrupt:
        sys.exit(0)