from proc_monitoring.models import MessageGrafana
from proc_monitoring.nodes.node import Node
from proc_monitoring.services import KafkaProducer

_PROP_NAME = "name"
_PROP_EXECUTION_INTERVAL = "execution_interval"
_PROP_TOPIC = "topic"
_PROP_CONNECTION = "connections"
_PROP_CONNECTION_KAFKA = "kafka"
_PROP_CONNECTION_BROKERS = "brokers"


class NodeGatherer(Node):
    """
    This node is a base node that should be deployed to gather data and send it to Kafka. It presents itself as a
    template node with methods that take care of most common actions: _gather_metrics and _build_message.

    Messages should be added to the queue through the _queue_data method. The messages are then sent to the Kafka topic
    specified, in the Grafana format.
    """

    def __init__(self, args, resources=None, reset_on_error=True):
        """
        Instantiates a new Gatherer node. It should never be called on it's own, only as a parent class.

        :param dict[str, Any] args: The arguments for the node. Check documentation for more details.
        :param list[Any] resources: Resources that should be opened once for all the lifetime of the node. Resources
                                    that are set here will be opened in all 3 execution methods.
        :param bool reset_on_error: If set to True, the node will try to relaunch itself if an exception is caught.
        """
        name = args[_PROP_NAME]
        exec_interval = float(args[_PROP_EXECUTION_INTERVAL])
        brokers = args[_PROP_CONNECTION][_PROP_CONNECTION_KAFKA][_PROP_CONNECTION_BROKERS]

        self.__kafka_topic = args[_PROP_TOPIC]
        self.__producer = KafkaProducer(client_id=name, bootstrap_servers=brokers)
        self.__message_queue = {}

        node_resources = [self.__producer] + resources if resources is not None else [self.__producer]
        Node.__init__(self, exec_interval, name, node_resources, reset_on_error)

    def _execute_run(self):
        self._gather_metrics()

        for key, messages in self.__message_queue.items():
            for message in messages:
                self._logger.debug("Sending message to topic [%s]: %s" % (self.__kafka_topic, message.serialize()))
                self.__producer.send(self.__kafka_topic, message.serialize())
        self.__message_queue = {}

    def _gather_metrics(self):
        """Overridable method that will be called each execution cycle to gather all the required data to then send."""
        raise NotImplementedError("Gatherer node must implement a _gather_metrics method")

    def _queue_data(self, key, tags, data):
        """
        Takes the parameters and metrics from the arguments and builds a Kafka message that will be relayed to the
        specified brokers with the specified topics. The messages will be sent after the execution.

        :param str key: The key of the message, to group the messages according to type of data gathered.
        :param dict[str, Any] tags: An dictionary with tags that will be added to the message.
        :param dict[str, Any] data: A dictionary containing the data that should be sent in the message.
        """
        if key not in self.__message_queue:
            self.__message_queue[key] = []
        self.__message_queue[key].append(MessageGrafana(key, tags, data))
