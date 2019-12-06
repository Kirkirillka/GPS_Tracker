import sys

from analyzer.models import AnalyzerRunner, UAVLocationAnalyzer

if __name__ == '__main__':

    try:
        analyzer = UAVLocationAnalyzer()

        runner: AnalyzerRunner = AnalyzerRunner(analyzer)

        runner.loop()
    except KeyboardInterrupt:
        sys.exit(0)