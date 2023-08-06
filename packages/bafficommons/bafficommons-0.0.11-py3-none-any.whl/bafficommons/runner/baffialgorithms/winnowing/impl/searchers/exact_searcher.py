import uuid


def build_matches_dict(matches_1, matches_2):
    matches_dict = {}
    for index, match in enumerate(matches_1):
        matches_dict[match] = matches_dict.get(match, set())
        matches_dict[match].add(matches_2[index])
    return matches_dict


def merge_matches(matches):
    matches = list(set(matches))
    matches.sort()
    if len(matches) == 0:
        return []
    merged_matches = []
    current_match = matches[0]
    current_end = current_match[1]
    for match in matches[1:]:
        start, end = match
        if start <= current_end + 1:
            current_end = max(end, current_end)
        else:
            merged_matches.append((current_match[0], current_end))
            current_match = match
            current_end = current_match[1]
    merged_matches.append((current_match[0], current_end))
    return merged_matches


def get_merged_match_from_match(match, merged_matches):
    match_start_line, match_end_line = match
    for merged_match in merged_matches:
        start_line, end_line = merged_match
        if start_line <= match_start_line and end_line >= match_end_line:
            return merged_match


def map_matches(matches_1, matches_2):
    matches_dict = build_matches_dict(matches_1, matches_2)
    merged_matches_1 = merge_matches(matches_1)
    merged_matches_2 = merge_matches(matches_2)

    identified_matches_1 = {}
    identified_matches_2 = {}

    for match_file_1, matches_list_file_2 in matches_dict.items():
        merged_match_file_1 = get_merged_match_from_match(
            match_file_1, merged_matches_1)
        match_identifier = identified_matches_1.get(
            merged_match_file_1, str(uuid.uuid4()))
        identified_matches_1[merged_match_file_1] = match_identifier

        for match_file_2 in matches_list_file_2:
            merged_match_file_2 = get_merged_match_from_match(
                match_file_2, merged_matches_2)

            if merged_match_file_2 in identified_matches_2:
                identified_matches_1[merged_match_file_1] = identified_matches_2[merged_match_file_2]
            else:
                identified_matches_2[merged_match_file_2] = match_identifier

    mapped_matches_1 = []
    mapped_matches_2 = []

    for match, match_identifier in identified_matches_1.items():
        start_line, end_line = match
        mapped_matches_1.append((match_identifier, start_line, end_line))

    for match, match_identifier in identified_matches_2.items():
        start_line, end_line = match
        mapped_matches_2.append((match_identifier, start_line, end_line))

    return mapped_matches_1, mapped_matches_2


def search(fingerprints_1, fingerprints_2):
    matches_1 = []
    matches_2 = []
    for fingerprint_1 in fingerprints_1:
        for fingerprint_2 in fingerprints_2:
            if fingerprint_1[0][0] == fingerprint_2[0][0]:
                start_line_1 = fingerprint_1[0][1]
                end_line_1 = fingerprint_1[0][2]
                start_line_2 = fingerprint_2[0][1]
                end_line_2 = fingerprint_2[0][2]
                matches_1.append((start_line_1, end_line_1))
                matches_2.append((start_line_2, end_line_2))
    return map_matches(matches_1, matches_2)
