# Use to generate the JSON-object from the Zettle API respnose.
import json
import os
import sys
import time
from datetime import datetime, timedelta

import dateutil.parser
import requests
from dateutil.tz import tzlocal
from flatten_dict import unflatten
from helpers.asset_loader import AssetLoader
from helpers.path_handler import credentials_dir
from parsers.parser import Parser

al = AssetLoader()


class ZettleParser:  # Parser
    def __init__(self):
        self.auth_token = None

    def intakt_type(self):
        return "Zettle"

    def get_new_auth_token(self):
        access_file_path = credentials_dir() / "access.json"
        with open(access_file_path) as access_file:
            access_json = json.load(access_file)

        token_response = requests.post(
            "https://oauth.zettle.com/token",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=f"grant_type={access_json['grant_type']}&client_id={access_json['client_id']}&assertion={access_json['assertion']}",
        )

        if token_response.ok:
            response_json = token_response.json()
            self.auth_token = response_json["access_token"]
            response_json["expires_at"] = time.time() + response_json["expires_in"]

            saved_token_file_path = credentials_dir() / "last_used_zettle_token.json"
            with open(saved_token_file_path, "w") as saved_token_file:
                json.dump(response_json, saved_token_file)
        else:
            print(
                f"error, could not get auth token. http response: {token_response.status_code} {token_response.reason}"
            )
            sys.exit(1)

    def set_auth_token(self):
        saved_token_file_path = credentials_dir() / "last_used_zettle_token.json"

        try:
            with open(saved_token_file_path) as saved_token_file:
                saved_token_obj = json.load(saved_token_file)

            if time.time() < saved_token_obj["expires_at"]:
                self.auth_token = saved_token_obj["access_token"]
                return

        except FileNotFoundError:
            pass

        self.get_new_auth_token()

    def get_data_block(self, start, end, last_purpurchase_hash=None):
        self.set_auth_token()

        if last_purpurchase_hash is None:
            r = requests.get(
                f"https://purchase.izettle.com/purchases/v2?startDate={start}&endDate={end}&descending=true",
                headers={"Authorization": f"Bearer {self.auth_token}"},
            )
        else:
            r = requests.get(
                f"https://purchase.izettle.com/purchases/v2?startDate={start}&endDate={end}&lastPurchaseHash={last_purpurchase_hash}&descending=true",
                headers={"Authorization": f"Bearer {self.auth_token}"},
            )

        return r.json()

    def get_fees(self, start, end):
        self.set_auth_token()

        start, end = self.create_limits(start, end)

        transactions = []

        r = requests.get(
            f"https://finance.izettle.com/v2/accounts/LIQUID/transactions?start={start}&end={end}&includeTransactionType=PAYMENT_FEE",
            headers={"Authorization": f"Bearer {self.auth_token}"},
        )

        while r.json():
            transactions += r.json()
            r = requests.get(
                f"https://finance.izettle.com/v2/accounts/LIQUID/transactions?start={start}&end={end}&includeTransactionType=PAYMENT_FEE&offset={len(transactions)}",
                headers={"Authorization": f"Bearer {self.auth_token}"},
            )

        dates = {}
        for transaction in transactions:
            date = transaction["timestamp"].split("T")[0]
            if date in dates:
                dates[date][date]["unit_price"] += transaction["amount"]
            else:
                dates[date] = {
                    date: {
                        "name": "Zettle avgift",
                        "quantity": 1,
                        "unit_price": transaction["amount"],
                        "account": 6540,
                    }
                }

        return {"skatt": dates}

    def create_limits(self, start_date: datetime, end_date: datetime):
        start = start_date.strftime("%Y-%m-%dT%H:%M")

        if end_date is None:
            end_date = start_date + timedelta(days=1)
        else:
            end_date = end_date + timedelta(days=1)
        end = end_date.strftime("%Y-%m-%dT%H:%M")

        return start, end

    def date_utc_to_swe(self, utc_dt: datetime):
        dt = utc_dt.astimezone(tzlocal())
        return dt.strftime("%Y-%m-%d")

    def get_short_utskott(self, name):
        return name.split("-")[0].strip().lower()

    def entire_purchase_discount(self, date: datetime, sales, purchase):
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
            sale_key = "_".join(
                [
                    utskott_name,
                    self.date_utc_to_swe(date),
                    "discounts",
                ]
            )
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

    def extract_data(self, sales, data):
        for purchase in data["purchases"]:
            # amount = purchase["amount"]  # in öre
            timestamp = purchase["timestamp"]
            date = dateutil.parser.isoparse(timestamp)
            str_date = date.strftime("%Y-%m-%dT%H:%M")

            if "discounts" in purchase and len(purchase["discounts"]) > 0:
                sales = self.entire_purchase_discount(date, sales, purchase)

            for product in purchase["products"]:
                if "name" not in product:
                    product_name = "UNKNOWN"
                    if product["type"] == "CUSTOM_AMOUNT":
                        # IF YOU SELL A PRODUCT USING CUSTOM AMOUNT, I WISH YOU AN UNPLEASANT DAY
                        # WORST REGARDS!
                        product_name = "CUSTOM AMOUNT"
                else:
                    product_name = product["name"]

                unit_price = product["unitPrice"]
                quantity = int(product["quantity"])

                short_utskott = self.get_short_utskott(product_name)

                if "donation" in product_name and not short_utskott == "c1":
                    short_utskott = "c1"

                if not short_utskott in al.utskott_accounts:
                    print("-----------------------")
                    print("Zettle date:", str_date)
                    print(f"{product_name} and {short_utskott}")
                    print(
                        f"No utskott found for\n{product}\t{quantity=}\t{unit_price=}"
                    )
                    print("-----------------------\n")
                    with open("err_products.txt", "a") as f:
                        f.write("-----------------------\n")
                        f.write(f"zettle date: {str_date}")
                        f.write("\n")
                        f.write(str(product))
                        f.write("\n")
                        f.write(str(purchase))
                        f.write("\n")
                        f.write("-----------------------\n\n")
                        f.close()
                    short_utskott = "sk"

                if short_utskott == "sk":
                    print(product_name.split("-"))
                if len(product_name.split("-")) > 1:
                    product_name = product_name.split("-", maxsplit=1)[1].strip()
                utskott_account = al.utskott_accounts[short_utskott]
                account = utskott_account["account"]
                utskott_name = utskott_account["name"]

                product_name_index = product_name + str(unit_price)

                sale_key = "_".join(
                    [
                        utskott_name,
                        self.date_utc_to_swe(date),
                        product_name_index,
                    ]
                )
                if short_utskott == "sk":
                    print("skatt")
                    print(f"{product_name=}")
                    print(f"{unit_price=}")
                    print(f"{sale_key=}")
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

    def get_sales(
        self,
        time_delta,
        start_date: datetime,
        end_date: datetime,
    ):
        start, end = self.create_limits(start_date, end_date)
        print(f"{start=}, {end=}")

        sales = {}
        last_purchase_hash = None

        data = self.get_data_block(start, end, last_purpurchase_hash=None)
        while len(data["purchases"]) > 0:
            sales = self.extract_data(sales, data)

            last_purchase_hash = data["lastPurchaseHash"]
            data = self.get_data_block(
                start, end, last_purpurchase_hash=last_purchase_hash
            )

        def delimiter_splitter(key):
            return key.split("_")

        sales = {key: sales[key] for key in sorted(sales)}
        return unflatten(sales, splitter=delimiter_splitter)
