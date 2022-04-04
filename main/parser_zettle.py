import json
from sys import prefix
from account import account_of

# date = "2022-02-11"
date = input()

infile = "../csv/" + date + ".csv"
outfile = "zettle_sales.json"
utskott_dict = {
    "s": "sex",
    "c": "cafe",
    "d": "dshop",
    "a": "aktu",
    "n": "noll",
    "dc": "dchip",
    "m": "medalj",
}

if __name__ == "__main__":
    line_skips = 6
    # with open(infile, encoding="utf-8") as f:
    with open(infile, encoding="unicode_escape") as f:
        i = 0
        lines = []
        for line in f:
            lines.append(line.split(";"))
        lines = lines[line_skips:]

        im_titels = [
            "Namn",
            "Antal sålda",
            "Sålt belopp (SEK)",
            "Antal returnerade",
            "Totalt inkl. moms (SEK)",
        ]

        titles = [l.strip() for l in lines.pop(0)]
        inds = []
        for t in im_titels:
            inds.append(titles.index(t))

        zettle_values = {}
        for line in lines[:-1]:
            prefix_product = line[inds[0]].split("-")
            prefix = prefix_product[0].strip()
            product = "-".join(prefix_product[1:])

            if len(prefix) == 1:
                utskott = utskott_dict[prefix.lower()]
            else:
                if prefix == "dc":
                    utskott = utskott_dict[prefix.lower()]
                else:
                    utskott = utskott_dict[prefix[:-1].lower()]
            account = account_of(prefix)

            print(line)
            if line[inds[3]] != "":
                if line[inds[1]] != "":
                    nbr_sold = float(line[inds[1]].replace(",", ".")) + float(
                        line[inds[3]].replace(".", ",")
                    )
                    total_amount = float(line[inds[4]].replace(",", "."))
                else:
                    nbr_sold = float(line[inds[3]].replace(".", ","))
                    total_amount = float(".".join(line[inds[4]].split(",")))
            else:
                nbr_sold = float(".".join(line[inds[1]].split(",")))
                total_amount = float(".".join(line[inds[2]].split(",")))

            if nbr_sold == 0:
                price_per_item = 0
            else:
                price_per_item = total_amount / abs(nbr_sold)

            product_name = product.strip().capitalize()
            if (
                product_name == "Dricka"
                or product_name == "Matlåda"
                or product_name == "Sötsaker"
                or product_name == "Pubmat"
                or product_name == "Övrigt"
                or product_name == "Whisky"
                or product_name == "Mackor"
                or product_name == "Snacks"
            ):
                product_name += " " + line[1]
                print(product_name)

            if product_name == "Donation":
                account = 3020

            summary = {
                product_name: {
                    "quantity": nbr_sold,
                    "price": price_per_item,
                    "account": account,
                }
            }

            if utskott in zettle_values:
                if date in zettle_values[utskott]:
                    zettle_values[utskott][date][product_name] = {
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
    print(lines[-1])
