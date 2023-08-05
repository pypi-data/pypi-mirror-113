import os

from kafka import KafkaConsumer as KPKafkaConsumer

from proc_monitoring.exceptions import KafkaError

if os.name == "nt":
    try:
        import win_inet_pton
    except ImportError:
        pass


class KafkaConsumer:
    """Kafka producer from kafka-python with a basic UTF-8 encoder. Should be called using With statements."""

    def __init__(self, client_id, group_id, bootstrap_servers, regex=None, topics=None):
        """
        Instantiates a new producer. To actually connect to kafka use the with statement.

        :param list[str] topics: Topics that this consumer should listen to. Takes priority over regex
        :param str regex: The regex pattern that this consumer will use to search for valid topics.
        :param str client_id: The unique ID or name for this consumer.
        :param str group_id: Group of the Kafka consumer. Messages are received by at least one consumer in a group.
        :param list[str] bootstrap_servers: The servers that this producer should connect to.
        :return: Connected Kafka consumer.
        :rtype: KafkaConsumer
        """
        self.__regex = regex
        self.__topics = topics if topics is not None else []
        self.__client_id = client_id
        self.__group = group_id
        self.__bootstrap_servers = bootstrap_servers
        self.consumer = None

        if self.__regex is None and len(self.__topics) == 0:
            raise KafkaError("Kafka consumer must specify a list of topics or a regex.")

    def __enter__(self):
        """Generates the kafka-python consumer with a basic UTF-8 decoder and connects to the required topics."""
        if self.__regex is not None:
            self.consumer = KPKafkaConsumer(pattern=self.__regex, client_id=self.__client_id, group_id=self.__group,
                                            bootstrap_servers=self.__bootstrap_servers,
                                            value_deserializer=lambda x: x.decode("utf-8"))
        else:
            self.consumer = KPKafkaConsumer(*self.__topics, client_id=self.__client_id, group_id=self.__group,
                                            bootstrap_servers=self.__bootstrap_servers,
                                            value_deserializer=lambda x: x.decode("utf-8"))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures that the kafka-python consumer is correctly closed."""
        if self.consumer is not None:
            self.consumer.close()
            self.consumer = None

    def retrieve_messages(self):
        """
        Retrieves all available messages from kafka that this consumer is subscribed to.

        :return: All messages available in the consumer.
        :rtype: list[str]
        """
        if self.consumer is None:
            raise KafkaError("Consumer should be opened before retrieving messages. Use the with statement to open it.")
        else:
            return [record.value for topic, records in self.consumer.poll().items() for record in records]
