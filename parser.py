import sys
def parse():
	input()
	titles=input().strip().split(',')
	values={}
	for lines in sys.stdin:
		vals=lines.strip().split(',')
		date=vals[5]
		# entry={}
		# entry['Bokfdag']=vals[5]
		# entry['Belopp']=vals[10]
		amount=vals[10]
		if date in values:
			values[date].append(amount)
		else:
			values[date]=[amount]
	return(values)
