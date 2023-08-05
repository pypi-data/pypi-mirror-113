from proc_monitoring.nodes.node import Node
from proc_monitoring.services import KafkaConsumer

_PROP_NAME = "name"
_PROP_EXECUTION_INTERVAL = "execution_interval"
_PROP_TOPICS = "topics"
_PROP_CONNECTION = "connections"
_PROP_CONNECTION_KAFKA = "kafka"
_PROP_CONNECTION_BROKERS = "brokers"


class NodeReceiver(Node):
    """Receiver node used to debug the messages sent to the Kafka brokers. Simply consumes all messages from Kafka."""

    def __init__(self, args):
        """
        Instantiates a new Receiver node.

        :param dict[str, Any] args: The arguments for the node. Check documentation for more details.
        """
        name = args[_PROP_NAME]
        exec_interval = float(args[_PROP_EXECUTION_INTERVAL])
        brokers = args[_PROP_CONNECTION][_PROP_CONNECTION_KAFKA][_PROP_CONNECTION_BROKERS]
        topics = args[_PROP_TOPICS]

        self.__consumer = KafkaConsumer(client_id=name, group_id=name, bootstrap_servers=brokers, topics=topics)
        Node.__init__(self, execution_time=exec_interval, thread_name=name, resources=[self.__consumer])

    def _execute_run(self):
        raw_messages = self.__consumer.retrieve_messages()
        for raw_msg in raw_messages:
            self._logger.debug("Received: \"%s\"" % raw_msg)
