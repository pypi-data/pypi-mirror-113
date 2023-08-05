from core_commons.exceptions import BaseError

# MONITORING_ERROR_CODES
MONITOR_ERROR = "MNTR000"
KAFKA_ERROR = "MNTR100"


class MonitorError(BaseError):
    """General monitoring error."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, MONITOR_ERROR, caused_by)


class KafkaError(BaseError):
    """General monitoring error."""

    def __init__(self, message, caused_by=None):
        BaseError.__init__(self, message, KAFKA_ERROR, caused_by)
