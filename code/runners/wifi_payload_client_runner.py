from utils.clients.models import WIFIClientAppMock
from time import sleep


DELAY = 2

if __name__ == '__main__':

    client = WIFIClientAppMock()

    while True:

        client.gen_and_send()
        sleep(DELAY)