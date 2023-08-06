import pygments.token
from pygments import lexers

EMPTY_LINE = ""
NEW_LINE = '\n'

PYTHON_EXTENSION = "py"
C_EXTENSION = "c"

EXTENSION_NAME = "extension_name"
LEXER_NAME_KEY = "lexer_name"
SINGLE_COMMENT_STR_KEY = "single_comment"
SINGLE_COMMENT_SPECIAL_STR_KEY = "single_comments_special"
OPEN_MULTI_COMMENT_STR_KEY = "open_multi_comment"
CLOSE_MULTI_COMMENT_STR_KEY = "close_multi_comment"

_extension_map = {
    PYTHON_EXTENSION: {
        EXTENSION_NAME: PYTHON_EXTENSION,
        LEXER_NAME_KEY: "python",
        SINGLE_COMMENT_STR_KEY: "#",
        SINGLE_COMMENT_SPECIAL_STR_KEY: "\"",
        OPEN_MULTI_COMMENT_STR_KEY: "\"\"\"",
        CLOSE_MULTI_COMMENT_STR_KEY: "\"\"\""
    },
    C_EXTENSION: {
        EXTENSION_NAME: C_EXTENSION,
        LEXER_NAME_KEY: "c",
        SINGLE_COMMENT_STR_KEY: "//",
        OPEN_MULTI_COMMENT_STR_KEY: "/*",
        CLOSE_MULTI_COMMENT_STR_KEY: "*/"
    }
}


def process_tokens(tokens):
    processed_tokens = []
    line_count = 1
    for token in tokens:
        token_value, raw_code = token
        processed_tokens.append((token_value, line_count, raw_code))
        line_count += raw_code.count(NEW_LINE)
    return processed_tokens


def filter_tokens(tokens):
    stop_tokens = [pygments.token.Text, pygments.token.Comment,
                   pygments.token.Literal.String.Doc, pygments.token.Comment.Single, pygments.token.Literal.String.Doc]
    return list(filter(lambda token: token[0] not in stop_tokens, tokens))


def format_tokens(tokens):
    return list(map(lambda token: (str(token[0]), token[1]), tokens))


def preprocess(raw_code, options):
    """
    Preprocess a given raw code.
    :param raw_code: Raw source code to be preprocessed
    :return: A filtered list in which each item is a tuple with the following data (token, line)
    """
    extension = _extension_map.get(options.get("extension"))
    lexer_name = extension.get(LEXER_NAME_KEY)
    lexer = lexers.get_lexer_by_name(lexer_name)
    tokens = process_tokens(lexer.get_tokens(raw_code))
    filtered_tokens = filter_tokens(tokens)

    return format_tokens(filtered_tokens)
