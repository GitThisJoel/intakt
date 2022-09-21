# Use to generate the JSON-object from the Zettle API respnose.
from pkgutil import get_data
import sys, os

from datetime import datetime
from datetime import timedelta, time
from requests_oauthlib import OAuth2Session
import json
import dateutil.parser
from flatten_dict import unflatten

from parsers.parser import Parser
from helpers.asset_loader import AssetLoader

al = AssetLoader()


class ZettleParser:  # Parser
    # @staticmethod
    def intakt_type(self):
        return "Zettle"

    def utc_to_cet(datetime):
        return

    def cet_to_utc(datetime):
        return

    def get_short_utskott(self, name):
        return name.split("-")[0].strip().lower()

    def entire_purchase_discount(self, date, sales, purchase):
        short_utskott = self.get_short_utskott(purchase["products"][0]["name"])
        all_same = True
        for product in purchase["products"][1:]:
            if not short_utskott == self.get_short_utskott(product["name"]):
                all_same = False
                break

        utskott_name = al.utskott_accounts[short_utskott]["name"]
        if all_same:
            total_discount = 0
            for discount in purchase["discounts"]:
                total_discount += discount["value"]
            sale_key = "_".join([utskott_name, date, "discounts"])
            if sale_key in sales:
                sales[sale_key]["unit_price"] -= total_discount
            else:
                sales[sale_key] = {
                    "name": "Rabatt",
                    "quantity": 1,
                    "unit_price": -total_discount,
                    "account": 3000,
                }
        else:
            print("------------------")
            print("all products are not the same...")
            print(purchase)
            print("------------------")

        return sales

    # @staticmethod
    def parse_help(self, sales, data):
        for purchase in data["purchases"]:
            # amount = purchase["amount"]  # in öre
            timestamp = purchase["timestamp"]
            date = dateutil.parser.isoparse(timestamp).strftime("%Y-%m-%d")

            if "discounts" in purchase and len(purchase["discounts"]) > 0:
                sales = self.entire_purchase_discount(date, sales, purchase)
                print("sales now")
                print(sales)

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

                short_utskott = product_name.split("-")[0].strip().lower()
                if "donation" in product_name and not short_utskott == "c1":
                    short_utskott = "c1"
                if not short_utskott in al.utskott_accounts:
                    print("-----------------------")
                    print(f"{product_name} and {short_utskott}")
                    print(f"No utskott found for\n{product}\t{quantity=}\t{unit_price=}")
                    print("-----------------------\n")
                    with open("err_products.txt", "a") as f:
                        f.write("-----------------------\n")
                        f.write(str(product))
                        f.write("\n")
                        f.write(str(purchase))
                        f.write("\n")
                        f.write("-----------------------\n")
                        f.close()
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

        return sales

    # @staticmethod
    def parse(
        self,
        data,
        time_delta,
        start_date: datetime,
        end_date: datetime,
    ):
        sales = {}

        data = ZettleParser().get_data(start_date, end_date)
        while len(data["purchases"]) > 0:
            sales = ZettleParser().parse_help(sales, data)
            data = ZettleParser().get_data(
                start_date, end_date, last_pur_hash=data["lastPurchaseHash"]
            )

        def delimiter_splitter(key):
            return key.split("_")

        sales = {key: sales[key] for key in sorted(sales)}
        return unflatten(sales, splitter=delimiter_splitter)

    def set_cred():
        return

    # @staticmethod
    def get_data(self, start_date: datetime, end_date: datetime, last_pur_hash=None):
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

        start = datetime.combine(start_date, time(0, 0)).isoformat()

        if end_date is None:
            end_date = start_date + timedelta(days=1)
        else:
            # end_date = datetime.combine(end_date, time(23, 59))
            end_date = end_date + timedelta(days=1)  # time is at 00:00
        end = end_date.isoformat()

        print(f"{start=}, {end=}")
        if last_pur_hash is None:
            r = zettle.get(
                f"https://purchase.izettle.com/purchases/v2?startDate={start}&endDate={end}&descending=true"
            )
        else:
            r = zettle.get(
                f"https://purchase.izettle.com/purchases/v2?startDate={start}&endDate={end}&lastPurchaseHash={last_pur_hash}&descending=true"
            )

        return r.json(encoding="utf-16")
