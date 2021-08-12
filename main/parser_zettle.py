import json

infile = "..\\Zettle-Sales-By-Product-Report-20210522.csv"
outfile = "zettle_sales.json"
date = ""
utskott = ""
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

        for line in lines[:-1]:
            name = line[inds[0]]
            nbr_sold = line[inds[1]]
            amount_sold = line[inds[2]]
