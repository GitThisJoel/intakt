# Used to generate the JSON-object from the Zettle API respnose.

from datetime import datetime
import argparse

from get_zettle_purchases import get_sales


def parse(data):
    # TODO:
    return


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--start",
        help="The start date for the fetch of Zettle sales. Date is on ISO format: yy-mm-ddThh:mm:ss, time is default to zero",
    )

    parser.add_argument(
        "-e",
        "--end",
        default=None,
        nargs="?",
        help="The end date for the fetch of Zettle sales, same format as start_date",
    )

    args = vars(parser.parse_args())

    start_date = datetime.fromisoformat(args["start"])
    end_date = datetime.fromisoformat(args["end"])

    sales = get_sales(start_date, end_date)
    return parse(sales)


if __name__ == "__main__":
    main()
