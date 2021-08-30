import sys,json
from account import account_of

def parse(divisor=';'):
	title=input()
	col_headers=input().strip().split(divisor)
	ind_date=col_headers.index('Bokfdag')
	ind_product=col_headers.index('Meddelande')
	ind_price=col_headers.index('Belopp')

	values={}
	utskottParser = {'c' : 'café', 's': 'sex'}
	for lines in sys.stdin:
		vals=lines.strip().split(divisor)

		date=vals[ind_date]
		utskottAndQuantity,product=vals[ind_product].split()
		product = product.lower()
		prefix,quantity = utskottAndQuantity.split('-')
		quantity = int(quantity)
		utskott = utskottParser[prefix]
		price=float(".".join(vals[ind_price].split(',')))

		# assume:
		# c-2 something
		if utskott in values:
			if date in values[utskott]:
				if product in values[utskott][date]:
					values[utskott][date][product]['quantity']+=quantity
				else:
					values[utskott][date][product]={'quantity': quantity, 'price': price, 'account': account_of(prefix)}
			else:
				values[utskott][date] = {product: {'quantity': quantity, 'price': price, 'account': account_of(prefix)}}
		else:
			values[utskott]={date:{product: {'quantity': quantity, 'price': price, 'account': account_of(prefix)}}}

	return(values)

if __name__ == "__main__":
	data=parse()
	filename='values.json'
	with open(filename, 'w', encoding='utf8') as file:
		file.write(json.dumps(data, indent=2, ensure_ascii=False))
