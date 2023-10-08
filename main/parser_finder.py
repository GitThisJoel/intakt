from enum import Enum, EnumMeta

from parsers.swish_parser import SwishParser
from parsers.zettle_parser import ZettleParser


class EnumGetitem(EnumMeta):
    def __getitem__(self, name: str):
        name = name.strip().upper()
        return super().__getitem__(name)


class ParserType(Enum, metaclass=EnumGetitem):
    ZETTLE = Z = ZettleParser
    ZETTLE_FEE = ZF = ZettleParser
    SWISH = S = SwishParser


def parser_finder(source):
    return ParserType[source].value
