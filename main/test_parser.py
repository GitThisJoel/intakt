from parsers.zettle_parser import ZettleParser
from datetime import datetime, timedelta, time
import json

test_req = True
if test_req:
    f = open("test_response_2.json", "w")
    f2 = open("test_response_3.json", "w")

    start_date = datetime.fromisoformat("2022-05-06")
    end_date = datetime.fromisoformat("2022-05-06")

    data = ZettleParser().get_data(start_date, end_date)
    data2 = ZettleParser().get_data(
        start_date,
        end_date,
        last_pur_hash=data["lastPurchaseHash"],
    )

    # d = ZettleParser().get_data(start_date, end_date)
    json.dump(data, f, indent=2)
    json.dump(data2, f2, indent=2)
    f.close()
    f2.close()
