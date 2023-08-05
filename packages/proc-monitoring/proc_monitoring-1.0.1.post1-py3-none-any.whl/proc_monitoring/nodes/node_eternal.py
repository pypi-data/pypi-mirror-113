import time

from proc_monitoring.nodes.node import Node

_PROP_NAME = "name"
_PROP_EXECUTION_INTERVAL = "execution_interval"


class NodeEternal(Node):
    """Node that takes a lot of of time in the execution state (an hour)."""

    def __init__(self, args):
        """
        Instantiates a new Eternal node.

        :param dict args: The arguments for the node. Check documentation for more details.
        """
        name = args[_PROP_NAME]
        exec_interval = float(args[_PROP_EXECUTION_INTERVAL])
        Node.__init__(self, thread_name=name, execution_time=exec_interval)

    def _execute_run(self):
        try:
            for i in range(3600):
                self._logger.debug("Running for %i seconds" % i)
                time.sleep(1)
        except SystemExit:
            self._logger.info("Node Eternal refuses to die!")
            for i in range(30):
                self._logger.debug("Running wild for %i seconds" % i)
                time.sleep(1)
