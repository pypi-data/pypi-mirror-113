import logging
import uuid

from .config import fingerprints_cache
from .indexers.winnowing_indexer import index
from .preprocessors.preprocesser import preprocess
from .searchers.exact_searcher import search

logger = logging.getLogger(__name__)

K_VALUE = 15
W_VALUE = 10


def calculate_file_lines(file_content):
    lines = file_content.split('\n')
    return len(lines)


def calculate_file_matched_lines(matches):
    matched_lines = 0
    for match in matches:
        _, start_line, end_line = match
        matched_lines += end_line - start_line + 1
    return matched_lines


def calculate_match_percentage(file_content, matches):
    file_lines = calculate_file_lines(file_content)
    matched_lines = calculate_file_matched_lines(matches)
    return matched_lines / file_lines


def get_fingerprints(file):

    index_options = {
        "k_value": K_VALUE,
        "window_size_value": W_VALUE
    }

    preprocess_options = {
        "extension": file.extension
    }

    cached_fingerprints = fingerprints_cache.get(file.id)

    if cached_fingerprints:
        return cached_fingerprints

    preprocessed_file = preprocess(
        file.content, preprocess_options)
    fingerprints = index(preprocessed_file, index_options)
    fingerprints_cache[file.id] = fingerprints

    return fingerprints


def build_result(file, matches):
    match_percentage = calculate_match_percentage(file.content, matches)
    total_lines_matched = calculate_file_matched_lines(matches)

    return {
        "id": file.id,
        "path": file.path,
        "name": file.name,
        "extension": file.extension,
        "match_percentage": match_percentage,
        "total_lines_matched": total_lines_matched,
        "lines_matched": matches
    }


def compare_files(source_file, target_file, _):

    logger.info("Comparing files (id, name): '({}, {})' vs. '({},{})'".format(
        source_file.id, source_file.name, target_file.id, target_file.name))

    source_fingerprints = get_fingerprints(source_file)
    target_fingerprints = get_fingerprints(target_file)

    source_matches, target_matches = search(
        source_fingerprints, target_fingerprints)

    source_file_results = build_result(source_file, source_matches)
    target_file_results = build_result(target_file, target_matches)

    return {
        "id": str(uuid.uuid4()),
        "source_file": source_file_results,
        "target_file": target_file_results
    }
