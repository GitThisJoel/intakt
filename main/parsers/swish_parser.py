# Used to generate the JSON-object from a swish report.
from parsers.parser import Parser


class SwishParser(Parser):
    @staticmethod
    def intakt_type():
        return "Swish"

    def parse(cls, data, time_delta):
        pass

    def get_data(cls, data):
        pass
