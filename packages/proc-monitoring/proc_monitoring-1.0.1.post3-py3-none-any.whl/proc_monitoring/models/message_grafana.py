import time


class MessageGrafana:
    """Class that defines the general structure for a Grafana message. Only to be used as a data model for Kafka or
    other message systems. Must not contain logic for any specific message broker."""

    def __init__(self, key, tags, data, ts=None):
        """
        Creates a new message.

        :param str key: The main tag that will represent the data .
        :param dict[str, Any] tags: The tags that identify and categorize the data of the message.
        :param dict[str, Any] data: The actual data that the message contains.
        :param str ts: The timestamp in epoch seconds. If not provided the timestamp will be automatically generated.
        """
        self.key = key
        self.tags = tags
        self.data = data
        self.timestamp = ts if ts is not None else str(int(round(time.time())))

    def serialize(self):
        """Serializes the message into a string.

        :return: A string serialization of the message.
        :rtype: str
        """
        flat_tags = ["%s=%s" % (key, value) for key, value in self.tags.items()]
        flat_data = ["%s=%s" % (key, value) for key, value in self.data.items()]
        return "%s,%s %s %s" % (self.key, ",".join(flat_tags), ",".join(flat_data), self.timestamp)

    @classmethod
    def deserialize(cls, serialized_message):
        """
        Returns a message object from a serialized string.

        :param str serialized_message: The serialized message string
        :return: The message object
        :rtype: MessageGrafana
        :raise ValueError: If the string could not be parsed into a message.
        """
        try:
            flat_key_tags, flat_data, ts = serialized_message.split(" ")
            separated_key_tags = flat_key_tags.split(",")
            key = separated_key_tags[0]
            tags = {tag_item.split("=")[0]: tag_item.split("=")[1] for tag_item in separated_key_tags[1:]}
            data = {data_item.split("=")[0]: data_item.split("=")[1] for data_item in flat_data.split(",")}
            return cls(key, tags, data, ts)
        except (TypeError, OverflowError, ValueError, KeyError) as e:
            raise ValueError("Could not generate a valid message from the serialized string: \"%s\"\n"
                             "(%s): %s" % (serialized_message, e.__class__.__name__, e))
