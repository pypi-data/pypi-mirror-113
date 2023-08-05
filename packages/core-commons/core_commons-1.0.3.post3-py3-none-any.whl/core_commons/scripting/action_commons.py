import argparse
import logging
import sys

__LOG_FORMAT = "[%(asctime)s] %(levelname)s - %(name)s: %(message)s"


def check_version(version_map):
    """
    Triggers an exit if the installed python version is not compatible with the specified version map. Exits with code
    1 if version restriction is not matched.

    :param dict[int, (int, int, int)] version_map: Major and version limit dictionary.
    """
    for python_version, required_version in version_map.items():
        if sys.version_info[0] == python_version and sys.version_info < required_version:
            version_check = python_version, required_version[0], required_version[1], required_version[2]
            sys.stderr.write("For python %i, minimum version %i.%i.%i is required\n" % version_check)
            sys.exit(1)


def configure_logger(info_flag, debug_flag, silence_loggers=None):
    """
    Configures the logger and the package loggers

    :param bool info_flag: If true, log level will be set to INFO unless debug_flag is set.
    :param bool debug_flag: If true, log level will be set to DEBUG.
    :param list[str] silence_loggers: The name of the loggers that should be always set to ERROR .
    """
    log_level = logging.DEBUG if debug_flag else logging.INFO if info_flag else logging.ERROR
    logging.basicConfig(level=log_level, format=__LOG_FORMAT)

    only_error_loggers = silence_loggers if silence_loggers is not None else []
    for logger_name in only_error_loggers:
        logging.getLogger(logger_name).setLevel(logging.WARNING)
        if logger_name == "requests":
            try:
                import requests
                import urllib3
                requests.packages.urllib3.disable_warnings()
                urllib3.disable_warnings()
            except ImportError:
                pass


def get_default_parser(config_file=False):
    """
    Will generate and return a default argument parser.

    :param bool config_file: If set to true, the config file argument will be required.
    :return: A argparse argument parser with the default, `whatif`, `info`, `debug` and `help` commands.
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("-w", "--whatif", action="store_true",
                        help="If set, the script will execute normally but won't change any persistent data.")
    parser.add_argument("-i", "--info", action="store_true",
                        help="If set, will output the general script steps and information.")
    parser.add_argument("-d", "--debug", action="store_true",
                        help="If set, will increase the action logging verbosity, usually only used for debugging.")
    parser.add_argument("-cf", "--config-file", action="store", required=config_file,
                        help="The configuration file that defines data and behavior of the action.")
    parser.add_argument("-h", "--help", action='help', default=argparse.SUPPRESS,
                        help="Show this help message and exit.")
    return parser
