# Used to generate the JSON-object from the Zettle API respnose.

from datetime import datetime
import argparse
import get_zettle_purchases
from parser import Parser


class ZettleParser(Parser):
    def parse(data, time_delta):
        pass

    def get_data(data):
        pass
