import ctypes
import logging
import sys
import threading
import time
import traceback
from random import randint


class Node(threading.Thread):
    """
    Simple node that implements a threading logic to schedule regular jobs and execute them in separate threads. The
    class uses timers to avoid hogging the computer resources. If the node is currently in execution, the node will not
    stop until execution is finished.
    """

    __CHECK_TIME = 1.0
    """Minimum time in seconds before the node checks if it should be closed"""

    __EXECUTION_TIME = 0.5
    """Minimum time in seconds before the node executes the next monitoring job"""

    def __init__(self, execution_time=__EXECUTION_TIME, thread_name=None, resources=None, reset_on_error=False):
        """
        Creates a new node.

        :param float execution_time: The desired time between monitoring job execution in seconds.
        :param str thread_name: The name that will be used for the thread and the node.
        :param list[Any] resources: Resources that should be opened once for all the lifetime of the node. Resources
                                    that are set here will be opened in all 3 execution methods.
        :param bool reset_on_error: If set to True, the node will try to relaunch itself if an exception is caught.
        """
        self._name = thread_name if thread_name is not None else "Monitoring Node %s" % randint(10000, 99999)
        """The name of the node and the thread"""

        self._logger = logging.getLogger(self._name)
        """The default logger for the node"""

        self.__persistent_resources = resources if resources is not None else []
        self.__reset_on_error = reset_on_error
        self.__active = threading.Event()
        self.__active.set()
        try:
            self.__run_time = float(execution_time)
        except ValueError:
            self._logger.warn("Could not parse execution time of node [%s], \"%s\"" % (self._name, execution_time))
            self.__run_time = Node.__EXECUTION_TIME
        self.__check_time = Node.__CHECK_TIME if Node.__CHECK_TIME < self.__run_time else self.__run_time
        self.__min_run_time = self.__run_time / 2.0
        self.__min_check_time = self.__check_time / 2.0

        threading.Thread.__init__(self, name=self._name, target=self.__node_execution)

    def stop(self):
        """Marks the node as not active, so that it will stop and end at the next check."""
        self.__active.clear()

    def force_stop(self):
        """
        Launches an exception to return from any processing being made. This may cause resources to break, or processes
        that should be atomic, to suddenly stop. Threads should not be closed this way unless they are stuck.

        A thread may catch a SystemExit exception to try to handle force exit, but it should never take too long to
        close. This exception however should always result in the closing of the thread.
        """
        self.__active.clear()
        thread_id = self.__get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            self._logger.error("Could not generate the System Exit exception to stop the thread. "
                               "Please close the process manually or wait for it to end.")

    def _execute_before(self):
        """Overridable method that will be executed before the first execution of the job."""
        pass

    def _execute_run(self):
        """Overridable method that defines the job of the node."""
        raise NotImplementedError("Node [%s] must implement a job in the \"_execute_run\" method")

    def _execute_after(self):
        """Overridable method that will be executed after the last execution of the job."""
        pass

    def __get_id(self):
        """
        Retrieves the ID of the thread that has been launched to execute the node

        :return: The id of the thread.
        """
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for thread_id, thread in threading._active.items():
            if thread is self:
                return thread_id

    def __node_execution(self):
        """
        Main execution of the node. Ensures that the program executes the job at a regular pace without hogging the
        resources of the computer or blocking the execution of other tasks.
        """
        # Set current time and timers
        time_last = time.time()
        timer_check = 0.0
        timer_run = 0.0

        try:
            # Load persistent resources and execute the method that executes before the main execution loop
            self._logger.debug("Executing preparation for node [%s]" % self._name)
            for resource in self.__persistent_resources:
                resource.__enter__()
            self._execute_before()

            while self.__active.is_set():
                # Execute the job if the run timer is done
                if timer_run <= 0.0:
                    timer_run += self.__run_time
                    self._logger.debug("Executing job for node [%s]" % self._name)
                    self._execute_run()

                # Update the check timer and limit it to the run timer
                time_now = time.time()
                timer_run -= time_now - time_last
                timer_check -= time_now - time_last
                timer_run = timer_run if timer_run > -self.__min_run_time else -self.__min_run_time
                timer_check = timer_check if timer_check > -self.__min_check_time else -self.__min_check_time
                timer_check = timer_run if timer_run < timer_check else timer_check
                time_last = time_now

                # Sleep until the check timer is done
                if timer_check > 0.0:
                    time.sleep(timer_check)
                    timer_check -= timer_check
                    timer_run -= timer_check
                timer_check = self.__check_time

            # Execute the method that executes after the main execution loop
            self._logger.debug("Executing cleanup for node [%s]" % self._name)
            self._execute_after()

        except Exception as e:
            # Close the resources
            for resource in self.__persistent_resources:
                try:
                    resource.__exit__(*sys.exc_info())
                except Exception as e:
                    self._logger.error("Could not close resource [%s]. "
                                       "(%s): %s" % (resource.__class__.__name__, e.__class__.__name__, e))

            # If reset on error is set, log the exception and reset the node. If not, just elevate the error.
            if self.__active.is_set():
                if self.__reset_on_error:
                    self._logger.error("Restarting stopped Node [%s]. "
                                       "(%s): %s. %s" % (self._name, e.__class__.__name__, e, traceback.print_exc()))
                    self.__node_execution()
                else:
                    raise e
