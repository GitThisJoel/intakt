from parsers import swish_parser, zettle_parser

parser_map = {
    "s": swish_parser,
    "swish": swish_parser,
    "z": zettle_parser,
    "zettle": zettle_parser,
}


def find_parser(source):
    return parser_map[source]
