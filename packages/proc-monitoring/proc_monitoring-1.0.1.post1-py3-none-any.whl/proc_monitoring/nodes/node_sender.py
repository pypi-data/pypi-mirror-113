from proc_monitoring.nodes.node import Node
from proc_monitoring.services import KafkaProducer

_PROP_NAME = "name"
_PROP_EXECUTION_INTERVAL = "execution_interval"
_PROP_MESSAGE = "message"
_PROP_TOPIC = "topic"
_PROP_CONNECTION = "connections"
_PROP_CONNECTION_KAFKA = "kafka"
_PROP_CONNECTION_BROKERS = "brokers"


class NodeSender(Node):
    """Sender node used to test sending a test message to a topic."""

    def __init__(self, args):
        """
        Instantiates a new Sender node.

        :param dict[str, Any] args: The arguments for the node. Check documentation for more details.
        """
        name = args[_PROP_NAME]
        exec_interval = float(args[_PROP_EXECUTION_INTERVAL])
        brokers = args[_PROP_CONNECTION][_PROP_CONNECTION_KAFKA][_PROP_CONNECTION_BROKERS]

        self.__topic = args[_PROP_TOPIC]
        self.__message = args[_PROP_MESSAGE]
        self.__producer = KafkaProducer(client_id=name, bootstrap_servers=brokers)
        Node.__init__(self, execution_time=exec_interval, thread_name=name, resources=[self.__producer])

    def _execute_run(self):
        self._logger.debug("Sending to [%s]: \"%s\"" % (self.__topic, self.__message))
        self.__producer.send(self.__topic, self.__message)
