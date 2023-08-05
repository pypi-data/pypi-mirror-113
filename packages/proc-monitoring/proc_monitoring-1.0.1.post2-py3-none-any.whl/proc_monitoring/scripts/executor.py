import logging
import os
import pkgutil
import time

from core_commons.handlers import configuration_handler
from core_commons.scripting import action_commons

all_modules = [(ldr, name, is_pkg) for ldr, name, is_pkg in pkgutil.walk_packages() if is_pkg and "nodes" in name]
node_module_pool = [ldr.find_module(name).load_module(name) for ldr, name, is_pkg in all_modules]


def get_node_class(node_name):
    for module in node_module_pool:
        if node_name in module.__dict__:
            return module.__dict__[node_name]

    raise NameError("No node found with name [%s]" % node_name)


def main():
    """Executes a controlled pool of nodes."""

    # Basic script version and arg check.
    action_commons.check_version({2: (2, 7, 5), 3: (3, 6, 0)})
    cl_args = action_commons.get_default_parser(config_file=True).parse_args()

    # Setup the logger and configuration
    silence_loggers = ["kafka", "paramiko", "requests", "urllib3", "yaml", "win_inet_pton"]
    action_commons.configure_logger(cl_args.info, cl_args.debug, silence_loggers)

    logging.info("Loading monitoring configuration...")
    ref_map = {"connections": "connection_refs"}
    monitoring_config = configuration_handler.get_configuration(cl_args.config_file, type_reference_map=ref_map)

    logging.info("Creating monitoring nodes...")
    node_pool = [get_node_class(node["type"])(node["args"]) for node in monitoring_config["nodes"]]

    logging.info("Starting NSX-T monitoring...")
    try:
        # Launch the monitoring nodes and wait for a close command.
        [node.start() for node in node_pool]
        while True:
            time.sleep(1)

    # When the script exits, gracefully stop the node execution.
    except KeyboardInterrupt:
        logging.info("Gracefully stopping monitoring...")
        [node.stop() for node in node_pool]

        # When the script exits, gracefully stop the node execution.
        try:
            logging.info("Waiting for all nodes to shut down...")
            logging.info("Press Ctrl+C again to forcefully kill monitoring nodes (not recommended).")
            while len(node_pool) > 0:
                for node in node_pool:
                    node.join(0.2)
                node_pool = [node for node in node_pool if node.isAlive()]

        # If user forces exit, stop the node execution immediately.
        except KeyboardInterrupt:
            logging.info("Forcefully stopping monitoring nodes...")
            for node in node_pool:
                logging.info("Forcefully stopping [%s]..." % node.name)
                node.force_stop()
                node.join(5)
            if any([node.isAlive() for node in node_pool]):
                logging.warn("Could not stop all monitoring nodes.")
                logging.info("Force exiting root...")
                os._exit(1)


if __name__ == '__main__':
    main()
