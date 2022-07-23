from parsers.swish_parser import SwishParser
from parsers.zettle_parser import ZettleParser

parser_map = {
    "s": SwishParser,
    "swish": SwishParser,
    "z": ZettleParser,
    "zettle": ZettleParser,
}


def parser_finder(source):
    return parser_map[source]
