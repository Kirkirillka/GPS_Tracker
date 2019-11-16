import sys

from databroker.models import DataBroker

if __name__ == '__main__':

    try:
        broker = DataBroker()
        broker.initialize()
        broker.run_loop()
    except KeyboardInterrupt:

        broker.stop_loop()
        sys.exit(0)

