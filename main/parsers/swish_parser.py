# Used to generate the JSON-object from a swish report.

from flatten_dict import unflatten
from helpers.asset_loader import AssetLoader

al = AssetLoader()


class SwishParser:
    def intakt_type(self):
        return "Swish"

    def parse(self, input_fp, utskott_filter=""):
        sales = {}

        with open(input_fp, "r", encoding="iso8859-1") as f:
            raw_data = f.readlines()

        titles = raw_data[1].split("\t")
        print(titles)
        index_dict = {
            "date": titles.index("Transdag"),
            "product": titles.index("Meddelande"),
            "price": titles.index("Belopp"),
        }

        for sale in raw_data[2:]:
            sale_info = sale.split("\t")
            date = sale_info[index_dict["date"]]
            product = sale_info[index_dict["product"]]
            price = int(100 * float(sale_info[index_dict["price"]].replace(",", ".")))

            short_utskott = product.split("-")[0].strip().lower()
            if short_utskott not in al.utskott_accounts:
                print("error, product do not have a utskott")
                print(sale)
                print("defaults to skatt")
                print("-------")
                short_utskott = "sk"

            if len(product.split("-")) > 1:
                product_name = "".join(product.split("-")[1:])
            elif short_utskott == "sk":
                product_name = product

            utskott_account = al.utskott_accounts[short_utskott]
            account = utskott_account["account"]
            utskott_name = utskott_account["name"]

            if utskott_filter and utskott_name != utskott_filter:
                continue

            product_name_index = product_name + str(price)

            sale_key = "_".join([utskott_name, date, product_name_index])
            if sale_key in sales:
                sales[sale_key]["quantity"] += 1
            else:
                sales[sale_key] = {
                    "name": product_name,
                    "quantity": 1,
                    "unit_price": price,
                    "account": account,
                }
        return sales

    def get_sales(self, input_fp, time_delta, utskott_filter=""):
        sales = self.parse(input_fp, utskott_filter)

        def delimiter_splitter(key):
            return key.split("_")

        sales = {key: sales[key] for key in sorted(sales)}
        return unflatten(sales, splitter=delimiter_splitter)
