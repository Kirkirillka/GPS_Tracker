from databroker.models import DataBroker

if __name__ == '__main__':

    broker = DataBroker()
    broker.initialize()
    broker.run_loop()