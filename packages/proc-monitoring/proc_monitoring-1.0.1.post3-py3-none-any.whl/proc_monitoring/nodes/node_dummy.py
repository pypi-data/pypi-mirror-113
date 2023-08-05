from proc_monitoring.nodes.node import Node

_PROP_NAME = "name"
_PROP_EXECUTION_INTERVAL = "execution_interval"


class NodeDummy(Node):
    """Dummy node that logs each time the execution is called. Used for debugging."""

    def __init__(self, args):
        """
        Instantiates a new Dummy node.

        :param dict args: The arguments for the node. Check documentation for more details.
        """
        name = args[_PROP_NAME]
        exec_interval = float(args[_PROP_EXECUTION_INTERVAL])

        Node.__init__(self, thread_name=name, execution_time=exec_interval)

    def _execute_before(self):
        self._logger.info("Before task called!")

    def _execute_run(self):
        self._logger.info("Execution task called!")

    def _execute_after(self):
        self._logger.info("After task called!")
