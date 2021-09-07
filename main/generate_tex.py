import json
from datetime import datetime

master = {
    "cafe": {
        "proper_name": "Cafémästeriet",
        "name": "Love Barany",
        "stilid": "lo5050ba-s",
    },
    "sex": {
        "proper_name": "Sexmästeriet",
        "name": "Marie Ask Uggla",
        "stilid": "ma4525as-s",
    },
    "aktu": {
        "proper_name": "Aktivitetsutskottet",
        "name": "Sean Jentz",
        "stilid": "se5362je-s",
    },
}

with open("account_details.json", "r") as f:
    accout_details = json.load(f)
    f.close()


def gen_tex(utskott, date, sales, pay_type):
    global master
    global accout_details

    name = master[utskott]["name"]
    stilid = master[utskott]["stilid"]
    proper_name = master[utskott]["proper_name"]

    today = datetime.now().strftime("%Y-%m-%d")

    packages = r"""\documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage[a4paper, margin=0.8in]{geometry}
    \usepackage{palatino}
    \usepackage{graphicx}
    \usepackage{longtable}
    """

    total = 0
    varor = r"\newcommand{\varor}{"
    account_report = {}
    print(sales)
    for product, info in sales.items():
        print(product)
        quantity = info["quantity"]
        price_per_product = info["price"]  # float(".".join(info["price"].split(",")))
        account = info["account"]
        total += quantity * price_per_product

        if account in account_report:
            account_report[account] += total
        else:
            account_report[account] = total

        varor += (
            f"{product.capitalize()} & {account} & {quantity} & {price_per_product} & {total}"
            + r"\\"
        )

    varor += "}"
    commands_1 = r"""\newcommand{\skapad}{%s}
    \newcommand{\kostnadsstalle}{%s}
    \newcommand{\typ}{%s}
    \newcommand{\datum}{%s}
    \newcommand{\summa}{%s kr}
    \newcommand{\namn}{%s}
    \newcommand{\stilid}{%s}
    """ % (
        today,
        proper_name,
        pay_type.capitalize(),
        date,
        total,
        name,
        stilid,
    )

    if utskott == "cafe":
        description = r"""\newcommand{\beskrivning}{Försäljning av varor i Café}"""
    elif utskott == "sex":
        description = r"""\newcommand{\beskrivning}{Sexmästeri verksamhet}"""
    elif utskott == "aktu":
        description = (
            r"""\newcommand{\beskrivning}{Försäljning av varor i Aktivitetsutskottet}"""
        )
    else:
        description = r"""\newcommand{\beskrivning}{Försäljning}"""

    fordelning = r"\newcommand{\fordelning}{"
    for acc, s in account_report.items():
        fordelning += f"{acc} & {accout_details[str(acc)]} & {s}" + r"\\"
    fordelning += "}"

    rest = r"""\begin{document}
    \hspace{-0.3in}
    \begin{tabular}{p{1.0in}p{3.5in}p{2in}}
    \includegraphics[width=0.8in]{D-symbol.pdf} &
    \vspace{-1in}
    {\large \uppercase{D-sektionen inom TLTH}} \newline \newline
    {\Huge \textsf{\textbf{Intäktsräkning}}}
    \newline \newline
    {\large \typ}&
    \vspace{-1in}
    Skapad: \newline
    \skapad \newline
    \end{tabular}

    \vspace{0.5in}
    \hspace{-0.3in}
    \begin{tabular}{|p{1.4in}|p{0.9in}|}
        \multicolumn{2}{l}{Intäktsuppgifter} \\
        \hline
        {\footnotesize Kostnadsställe} \newline \textbf{\kostnadsstalle}&
        {\footnotesize Datum} \newline \textbf{\datum} \\
        \hline
        \multicolumn{2}{|p{2.3in}|}{{\footnotesize Summa} \newline \textbf{\summa}} \\
        \hline
    \end{tabular}
    \hspace{0.1in}
    \begin{tabular}{|p{1.3in}|p{0.9in}|p{1.1in}|}
        \multicolumn{3}{l}{Kontaktperson} \\
        \hline
        \multicolumn{2}{|p{2.2in}|}{{\footnotesize Namn} \newline \textbf{\namn}}
          &
         {\footnotesize STIL-ID} \newline \textbf{\stilid} \\
         \hline
         \multicolumn{3}{p{3.3in}}{{\footnotesize \quad} \newline \textbf{\quad}}
    \end{tabular}

    \subsection*{Beskrivning}
    \beskrivning

    \subsection*{Fördelning}
    \begin{tabular}{p{0.6in}p{2in}r}
        Konto & Beskrivning& Belopp (kr)\\ \hline
        \fordelning
    \end{tabular}

    \subsection*{Varor}
    \begin{longtable}[l]{llrrr}
        Vara & Konto & Antal (st) & Styckpris (kr/st) & Belopp (kr) \\ \hline
        \varor
    \end{longtable}

    \subsection*{Attestering}
    \begin{tabular}{|p{2.5in}|}
        \hline
        {\footnotesize Datum} \newline \\
        \hline
        {\footnotesize Underskrift} \newline \newline\\
        \hline
        {\footnotesize Namn} \newline \textbf{\namn} \\
        \hline
    \end{tabular}
    \end{document}
    """
    return packages + commands_1 + description + fordelning + varor + rest


if __name__ == "__main__":
    filename = "values.json"
    with open(filename) as file:
        sale_report = json.load(file)
        file.close()

    today = datetime.now().strftime("%Y-%m-%d")
    nbr = 1
    for pay_type, data in sale_report.items():
        for utskott, values in data.items():
            for date, sales in values.items():
                tex = gen_tex(utskott, date, sales, pay_type)

                filename = "tex/" + today + "_" + str(nbr) + ".tex"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(tex)
                    f.close
                nbr += 1
