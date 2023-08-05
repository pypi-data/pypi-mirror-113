from kafka import KafkaProducer as KPKafkaProducer

from proc_monitoring.exceptions import KafkaError


class KafkaProducer:
    """Kafka producer from kafka-python with a basic UTF-8 encoder. Should be called using With statements."""

    def __init__(self, client_id, bootstrap_servers):
        """
        Instantiates a new producer. To actually connect to kafka use the with statement.

        :param str client_id: The unique ID or name for this producer.
        :param list[str] bootstrap_servers: The servers that this producer should connect to.
        """
        self.__client_id = client_id
        self.__bootstrap_servers = bootstrap_servers
        self.producer = None

    def __enter__(self):
        """Generates the kafka-python producer with a basic UTF-8 encoder."""
        self.producer = KPKafkaProducer(client_id=self.__client_id, bootstrap_servers=self.__bootstrap_servers,
                                        value_serializer=lambda x: x.encode("utf-8"))

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Ensures that the kafka-python producer is correctly closed."""
        if self.producer is not None:
            self.producer.close()
            self.producer = None

    def send(self, topic, message):
        """
        Sends a message to Kafka.

        :param str topic: Topic of the message. Consumers will read only messages from topics they are subscribed to.
        :param str message: Message to send. Should be a plain string.
        :raises KafkaError: If the producer is not open.
        """
        if self.producer is None:
            raise KafkaError("Producer should be opened before sending a message. Use the with statement to open it.")
        else:
            self.producer.send(topic, value=message)
