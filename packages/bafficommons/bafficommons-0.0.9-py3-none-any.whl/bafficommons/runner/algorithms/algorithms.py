import logging

from .winnowing.impl.winnowing import compare_files as winnowing_compare_files

logger = logging.getLogger(__name__)

algorithm_functions = {
    "winnowing": winnowing_compare_files
}


def compare_files(algorithm_name, source_file, target_file, check_options):
    compare_function = algorithm_functions.get(algorithm_name)
    return compare_function(source_file, target_file, check_options)
