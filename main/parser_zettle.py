import json
from sys import prefix
from account import account_of

infile = "../Zettle-Sales-By-Product-Report-20210823.csv"
outfile = "zettle_sales.json"
date = "2021-10-23"
utskott_dict = {"s": "sex", "c": "cafe", "d": "aktu", "n": "noll"}

if __name__ == "__main__":
    line_skips = 6
    with open(infile, encoding="unicode_escape") as f:
        i = 0
        lines = []
        for line in f:
            lines.append(line.split(";"))
        lines = lines[line_skips:]

        im_titels = ["Namn", "Antal sålda", "Sålt belopp (SEK)"]
        titles = lines.pop(0)
        inds = []
        for t in im_titels:
            inds.append(titles.index(t))

        zettle_values = {}
        for line in lines[:-1]:
            prefix_product = line[inds[0]].split("-")
            prefix = prefix_product[0]
            product = "-".join(prefix_product[1:])

            if len(prefix) == 1:
                utskott = utskott_dict[prefix]
            else:
                utskott = utskott_dict[prefix[:-1]]
            account = account_of(prefix)

            nbr_sold = float(".".join(line[inds[1]].split(",")))
            total_amount = float(".".join(line[inds[2]].split(",")))
            price_per_item = total_amount / nbr_sold

            summary = {
                product.capitalize(): {
                    "quantity": nbr_sold,
                    "price": price_per_item,
                    "account": account,
                }
            }

            if utskott in zettle_values:
                if date in zettle_values[utskott]:
                    zettle_values[utskott][date][product.capitalize()] = {
                        "quantity": nbr_sold,
                        "price": price_per_item,
                        "account": account,
                    }
                else:
                    zettle_values[utskott][date] = summary
            else:
                zettle_values[utskott] = {date: summary}

    with open(outfile, "w") as f:
        out = json.dumps({"zettle": zettle_values}, indent=2, ensure_ascii=False)
        # print(out)
        f.write(out)
        f.close()
