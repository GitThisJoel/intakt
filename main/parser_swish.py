import sys,json
utskott_code={"c": "cafe", "s": "sex"}
def parse(utskott,divisor=';'):
	title=input()
	col_headers=input().strip().split(divisor)
	ind_date=col_headers.index('Bokfdag')
	ind_article=col_headers.index('Meddelande')
	ind_price=col_headers.index('Belopp')

	values={}
	for lines in sys.stdin:
		vals=lines.strip().split(divisor)

		# TODO:
		# does not work, look how it works in zettle
		date="".join(vals[ind_date].split())
		article="".join(vals[ind_article].split())
		price="".join(vals[ind_price].split())

		# assume:
		# c-2 something
		quantity=0
		utskott=utskott_code[article.split('-')[0]]
		if utskott in values:
			if date in values[utskott]:
				if article in values[utskott][date]:
					values[utskott][date][article]['quantity']+=quantity
				else:
					values[utskott][date][article]={'quantity': quantity, 'price': price}
			else:
				values[utskott][date] = {article: {'quantity': quantity, 'price': price}}
		else:
			values[utskott]={date:{article: {'quantity': quantity, 'price': price}}}

	return(values)

if __name__ == "__main__":
	data=parse('cafe')
	filename='values.json'
	with open(filename, 'w', encoding='utf8') as file:
		file.write(json.dumps(data, indent=2, ensure_ascii=False))
