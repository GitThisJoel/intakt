#! /usr/bin/env python3
import sys
from helpers.path_handler import main_dir

sys.path.append(main_dir())

import pytz
import argparse
import json

from datetime import datetime

from parser_finder import parser_finder
from parsers.zettle_parser import ZettleParser
from tex_compiler.tex_compiler import TexCompiler


def swe_to_utc(dt: datetime):
    return pytz.timezone("Europe/Stockholm").localize(dt).astimezone(pytz.utc)


def handle_date(date, args):
    return (
        swe_to_utc(datetime.fromisoformat(args[date]))
        if args[date] is not None
        else None
    )


def args_handler(args):
    source = args["source"]
    start_date = handle_date("start_date", args)
    end_date = handle_date("end_date", args)
    time_delta = args["time_delta"]
    input_fp = args["input_fp"]
    output_fp = args["combine_output_fp"]
    keep_tex = args["keep"]
    utskott_filter = args["utskott"]

    print(start_date, end_date)

    if "fee" in source:
        parser_cls = ZettleParser()
        return (
            "Zettle fees",
            parser_cls.get_fees(
                start_date,
                end_date,
            ),
            output_fp,
            keep_tex,
        )

    parser_cls = parser_finder(source)()
    if parser_cls.intakt_type() == "Zettle":
        if start_date is None:
            print("error, need to specify start date")
            return "", {}

        return (
            parser_cls.intakt_type(),
            parser_cls.get_sales(
                time_delta,
                start_date,
                end_date,
                utskott_filter,
            ),
            output_fp,
            keep_tex,
        )
    elif parser_cls.intakt_type() == "Swish":
        if input_fp is None:
            print("error, need to specify input file path")
            return "", {}

        return (
            parser_cls.intakt_type(),
            parser_cls.get_sales(
                input_fp,
                time_delta,
                utskott_filter,
            ),
            output_fp,
            keep_tex,
        )


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
        default=None,
        nargs="?",
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

    parser.add_argument(
        "-inp",
        "--input-fp",
        default=None,
        nargs="?",
        help="Input file path",
    )

    parser.add_argument(
        "-o",
        "--combine-output-fp",
        default=None,
        nargs="?",
        help="The output file path for output PDFs if they are to be combined",
    )

    parser.add_argument(
        "--keep",
        default=False,
        action="store_true",
        help="Keep the tex files after compilation",
    )

    parser.add_argument(
        "--utskott",
        default="",
        nargs="?",
        help="Which utskott to generate for. If not specified, all utskott will be generated",
    )

    args = vars(parser.parse_args())
    print(args)
    intakt_type, parsed_data, output_fp, keep_tex = args_handler(args)

    if intakt_type == "" or len(parsed_data) == 0:
        return

    outfile = "response.json"
    with open(outfile, "w") as f:
        json.dump(parsed_data, f, indent=2)

    tc = TexCompiler(
        outfile,
        intakt_type,
        output_fp,
        keep_tex,
        zettle_fee_mode=("fees" in args["source"]),
    )
    tc.compile_all()
    return


if __name__ == "__main__":
    main()
