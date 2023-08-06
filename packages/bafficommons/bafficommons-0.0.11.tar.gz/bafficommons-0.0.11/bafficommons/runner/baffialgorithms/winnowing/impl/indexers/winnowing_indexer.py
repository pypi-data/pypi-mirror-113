import hashlib


def index(tokens, options):
    """
    Given a list of tokens indexes the whole document into a set of them
    :param tokens:
    :return:
    """
    k = options.get("k_value", 50)
    window_size = options.get("window_size_value", 20)

    k_grams = generate_n_grams(tokens, k)
    hash_list = [hash_k_gram(k_gram) for k_gram in k_grams]
    windows = generate_n_grams(hash_list, window_size)
    fingerprints = select_fingerprints(windows)

    return fingerprints


def generate_n_grams(items, n):
    n_grams = []
    for i in range(len(items) - n + 1):
        n_gram = tuple(items[i:i + n])
        n_grams.append(n_gram)
    return n_grams


def hash_k_gram(k_gram):
    start_line = k_gram[0][1]
    end_line = k_gram[-1][1]
    concat_tokens = " ".join(map(lambda x: x[0], k_gram))
    hash_value = int(hashlib.sha512(concat_tokens.encode()).hexdigest(), 16)
    return hash_value, start_line, end_line


def select_fingerprints(windows):
    fingerprints = []
    previous_min_hash = None
    i = 0
    for window in windows:
        current_min_hash = min(window, key=lambda x: x[0])
        if current_min_hash != previous_min_hash:
            rindex = len(window) - window[-1::-1].index(current_min_hash) - 1
            fingerprint_position = i + rindex
            fingerprints.append((current_min_hash, fingerprint_position))
            previous_min_hash = current_min_hash
        i += 1
    return fingerprints
