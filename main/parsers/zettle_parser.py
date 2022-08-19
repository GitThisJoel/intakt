# Used to generate the JSON-object from the Zettle API respnose.
import sys, os

from datetime import datetime
from datetime import timedelta
from requests_oauthlib import OAuth2Session
import json
import dateutil.parser
from flatten_dict import unflatten

from parsers.parser import Parser
from helpers.asset_loader import AssetLoader

al = AssetLoader()


class ZettleParser(Parser):
    @staticmethod
    def __str__():
        return "Zettle"

    @staticmethod
    def parse(data, time_delta):
        sales = {}
        for purchase in data["purchases"]:
            # amount = purchase["amount"]  # in öre
            timestamp = purchase["timestamp"]
            date = dateutil.parser.isoparse(timestamp).strftime("%Y-%m-%d")

            for product in purchase["products"]:
                product_name = product["name"]

                product_name.replace("\u00e5", "å")
                product_name.replace("\u00c5", "Å")

                product_name.replace("\u00e4", "ä")
                product_name.replace("\u00c4", "Ä")

                product_name.replace("\u00f6", "ö")
                product_name.replace("\u00D6", "Ö")

                unit_price = product["unitPrice"]
                quantity = int(product["quantity"])

                short_utskott = product_name.split("-")[0]
                if "donation" in product_name and not short_utskott == "c1":
                    short_utskott = "c1"

                if not short_utskott in al.utskott_accounts:
                    print(f"No utskott found for\n{product}\t{quantity=}\t{unit_price=}")
                    continue

                product_name = "".join(product_name.split("-")[1:])
                utskott_account = al.utskott_accounts[short_utskott]
                account = utskott_account["account"]
                utskott_name = utskott_account["name"]

                product_name_index = product_name + str(unit_price)

                sale_key = "_".join([utskott_name, date, product_name_index])

                if sale_key in sales:
                    sales[sale_key]["quantity"] += quantity
                else:
                    sales[sale_key] = {
                        "name": product_name,
                        "quantity": quantity,
                        "unit_price": unit_price,
                        "account": account,
                    }

        def delimiter_splitter(key):
            return key.split("_")

        return unflatten(sales, splitter=delimiter_splitter)

    @staticmethod
    def get_data(start_date: datetime, end_date: datetime):
        access_file = os.path.dirname(os.path.realpath(__file__)) + "/../credentials/access.json"
        with open(access_file) as f:
            access_cred = json.load(f)
            f.close()

        client_id = access_cred["client_id"]
        client_secret = access_cred["client_secret"]
        redirect_uri = "https://httpbin.org/get"

        authorization_base_url = "https://oauth.zettle.com/authorize"
        token_url = "https://oauth.zettle.com/token"
        scope = ["READ:PURCHASE"]

        zettle = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
        authorization_url, _ = zettle.authorization_url(authorization_base_url)

        # TODO: can this be done without human interaction?
        redirect_response = input(authorization_url + "\n")

        zettle.fetch_token(
            token_url,
            include_client_id=True,
            client_secret=client_secret,
            authorization_response=redirect_response,
        )

        if end_date is None:
            end_date = start_date + timedelta(days=1)

        r = zettle.get(
            f"https://purchase.izettle.com/purchases/v2?startDate={start_date.isoformat()}&endDate={end_date.isoformat()}&descending=true"
        )

        return r.json(encoding="utf-16")
