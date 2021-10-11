import sys, json
from account import account_of


def parse(divisor=";"):
    title = input()
    col_headers = input().strip().split(divisor)
    ind_date = col_headers.index("Bokfdag")
    ind_product = col_headers.index("Meddelande")
    ind_price = col_headers.index("Belopp")
    values = {}
    utskottParser = {"c": "cafe", "s": "sex", "n": "noll", "dc": "dchip"}

    total_price = 0
    for lines in sys.stdin:
        vals = lines.strip().split(divisor)

        date = vals[ind_date]
        prefix, product_quantity = vals[ind_product].split("-")
        utskott = utskottParser[prefix]

        pq = product_quantity.split()
        if pq[0].isnumeric():
            quantity = int(pq[0])
            product = " ".join(pq[1:])
        elif pq[-1].isnumeric():
            quantity = int(pq[-1])
            product = " ".join(pq[:-1])
        else:
            quantity = 1
            product = " ".join(pq)

        price = float(vals[ind_price].replace(",", "."))
        total_price += price * quantity
        if product == "Läsk":
            product += " " + str(price)

        print(f"{price}\t {product}\t {quantity}")
        # assume:
        # c-2 something
        # or
        # c-Prodname 2
        price /= quantity
        if utskott in values:
            if date in values[utskott]:
                if product in values[utskott][date]:
                    values[utskott][date][product]["quantity"] += quantity
                else:
                    values[utskott][date][product] = {
                        "quantity": quantity,
                        "price": price,
                        "account": account_of(prefix),
                    }
            else:
                values[utskott][date] = {
                    product: {
                        "quantity": quantity,
                        "price": price,
                        "account": account_of(prefix),
                    }
                }
        else:
            values[utskott] = {
                date: {
                    product: {
                        "quantity": quantity,
                        "price": price,
                        "account": account_of(prefix),
                    }
                }
            }
    print(total_price)
    return values


if __name__ == "__main__":
    data = parse()
    filename = "values.json"
    with open(filename, "w", encoding="utf8") as file:
        file.write(json.dumps({"Swish": data}, indent=2, ensure_ascii=False))
        file.close()
