import json
from account import account_of

infile = "Zettle-Sales-By-Product-Report-20210522.csv"
outfile = "zettle_sales.json"
date = "2021"
utskott_dict = {"s": "sex", "c": "cafe"}


if __name__ == "__main__":
    line_skips = 6
    with open(infile, encoding="utf-8") as f:
        i = 0
        lines = []
        for line in f:
            lines.append(line.split(";"))
        while i < line_skips:
            lines.pop(0)
            i += 1

        im_titels = ["Namn", "Antal sålda", "Sålt belopp (SEK)"]
        titles = lines.pop(0)
        inds = []
        for t in im_titels:
            inds.append(titles.index(t))

        articles = []
        for line in lines[:-1]:
            prefix, product = line[inds[0]].split("-")
            print(prefix[:-1])
            print(account_of(prefix))
            account = -1

            nbr_sold = float(".".join(line[inds[1]].split(",")))
            total_amount = float(".".join(line[inds[2]].split(",")))
            price_per_item = total_amount / nbr_sold

            articles.append(
                {
                    product.capitalize(): {
                        "quantity": nbr_sold,
                        "price": price_per_item,
                        "account": account,
                    }
                }
            )

    with open(outfile, "w") as f:
        out = json.dumps({date: articles}, indent=2, ensure_ascii=False)
        # print(out)
        # f.write(out)
        f.close()
