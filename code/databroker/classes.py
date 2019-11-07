import paho

from typing import List, Callable


class BrokerAdapter:
    """
        Class **BrokerAdapter** is responsible for providing an interface to fetch data from MQTT Message broker and
            pass data to DataBroker.
    """

    def __init__(self):

        """
            1. _conn - a real connection to MQTT broker
            2. _topics - a list of topics BrokerAdapter will be listening to
        """

        self._conn = None
        self._topics = {}

    def _connect(self) -> bool:

        """
            Initialize connection to MQTT Message Broker server
        :return: True if connection was established successfully, otherwise raise ConnectionError
        :raise: ConnectionError if connection is not established
        """

        raise NotImplementedError

    def setup(self) -> None:

        """
            Configure connection parameters and instruct a private _connect how to be executed.
            Then perform all subscriptions and callback function bindings.

            If a ConnectionError raises at _connect, it pass the exception further, so, the program may fail.

        :return: None if connection is established, pass ConnectionError from _connect otherwise
        :raise: ConnectionError
        """

        raise NotImplementedError

    def get_topics(self) -> List[str]:

        """
            Returns a list of topics which the BrokerAdapter was subscribed and listen messages from MQTT Broker.
            Internally, the list of topics is presented by _topics variable. This function should take care of
            the right formatting and checking.

        :return: A list of topics which were subscribed
        """

        raise NotImplementedError

    def add_topic(self, topic: str, callback: Callable[[str, str, object], None]) -> bool:

        """
            Perform subscription on specific **topic**. A **callback** function will be executed
            with provided parameters each time a new message is arrived on the topic.

            Steps:

                1. Execute subscribe function on MQTT connection object.
                2. Add the new topic to _topics dictionary with values {topic: callback}.

        :param topic: A string specified a topic path
        :param callback:  A function or a callable object, which takes three parameters (four in case of class methods).
        :return: return True if subscription was made successfully.
        """

        raise NotImplementedError

    def del_topic(self, topic: str) -> bool:
        """
            Exclude the specified topic to be NOT listened from MQTT Broker.
            If the specified topic is not seen to be listened in _topics, then
            topic is ignored, returns True.

            Steps:

                1. Delete subscription on the topic to MQTT Connection
                1. Delete the topic from _topics variable

        :param topic: a string specifies a topic (format : "/my/format/for/any/*")
        :return: True if unsubscription made successfully, False otherwise

        """

        raise NotImplementedError

    def serve(self) -> bool:

        """
            Run internal loop_forever function. This function is blocking, so function won't return
            until disconnect is executed on MQTT connection object
        :return: True if loop is stopped
        """

        raise NotImplementedError
