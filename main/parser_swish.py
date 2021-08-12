import sys,json

def parse(divisor=';'):
	title=input()
	col_headers=input().strip().split(divisor)
	ind_date=col_headers.index('Bokfdag')
	ind_product=col_headers.index('Meddelande')
	ind_price=col_headers.index('Belopp')

	values={}
	utskottParser = {'c' : 'café'}
	for lines in sys.stdin:
		vals=lines.strip().split(divisor)

		# TODO:
		# does not work, look how it works in zettle
		date=vals[ind_date]
		utskottAndQuantity,product=vals[ind_product].split()
		utskott,quantity = utskottAndQuantity.split('-')
		utskott = utskottParser[utskott]
		price=float(".".join(vals[ind_price].split(',')))

		# assume:
		# c-2 something
		if utskott in values:
			if date in values[utskott]:
				if product in values[utskott][date]:
					values[utskott][date][product]['quantity']+=quantity
				else:
					values[utskott][date][product]={'quantity': quantity, 'price': price}
			else:
				values[utskott][date] = {product: {'quantity': quantity, 'price': price}}
		else:
			values[utskott]={date:{product: {'quantity': quantity, 'price': price}}}

	return(values)

if __name__ == "__main__":
	data=parse()
	filename='values.json'
	with open(filename, 'w', encoding='utf8') as file:
		file.write(json.dumps(data, indent=2, ensure_ascii=False))
