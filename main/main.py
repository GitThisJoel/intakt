import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from datetime import datetime
import argparse
import json

from parser_finder import parser_finder


def args_handler(args):
    source = args["source"]
    start_date = datetime.fromisoformat(args["start_date"])
    end_date = datetime.fromisoformat(args["end_date"]) if args["end_date"] is not None else None
    time_delta = args["time_delta"]

    parser_cls = parser_finder(source)
    sales = parser_cls.get_data(start_date, end_date)
    return parser_cls.parse(sales, time_delta)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--source",
        default="zettle",
        help="Where the data is supposed to be retrieved from [z(ettle)|s(wish)]",
    )

    parser.add_argument(
        "-sd",
        "--start-date",
        help="The start date for the fetch of Zettle sales. Date is on ISO format: yy-mm-ddThh:mm:ss, time is default to zero",
    )

    parser.add_argument(
        "-ed",
        "--end-date",
        default=None,
        nargs="?",
        help="The end date for the fetch of Zettle sales, same format as start_date",
    )

    parser.add_argument(
        "-td",
        "--time-delta",
        default="daily",
        nargs="?",
        help="The time of which each report spans",
    )

    args = vars(parser.parse_args())
    parsed_data = args_handler(args)
    outfile = "response.json"
    with open(outfile, "w") as f:
        json.dump(parsed_data, f, indent=2)

    return


if __name__ == "__main__":
    main()
