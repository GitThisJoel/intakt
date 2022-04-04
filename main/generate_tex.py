import json
from datetime import datetime

total_costs = 0
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
    "dshop": {
        "proper_name": "D-shopen",
        "name": "Sean Jentz",
        "stilid": "se5362je-s",
    },
    "noll": {
        "proper_name": "Nollningsutksottet",
        "name": "Linus Åbrink",
        "stilid": "li1304ab-s",
    },
    "dchip": {
        "proper_name": "D-chip",
        "name": "Ellen Petersen",
        "stilid": "el3775pe-s",
    },
    "medalj": {
        "proper_name": "Medaljelele",
        "name": "Michaela Ljungstrand",
        "stilid": "me4300lj-s",
    },
}

master = {
    "cafe": {
        "proper_name": "Cafémästeriet",
        "name": "Sofia Tatidis",
        "stilid": "so2107ta-s",
    },
    "sex": {
        "proper_name": "Sexmästeriet",
        "name": "Sebastian Malmström",
        "stilid": "se4872ma-s",
    },
    "aktu": {
        "proper_name": "Aktivitetsutskottet",
        "name": "Alex Gustafsson",
        "stilid": "al6414gu-s",
    },
    "dshop": {
        "proper_name": "D-shopen",
        "name": "Alex Gustafsson",
        "stilid": "al6414gu-s",
    },
    "noll": {
        "proper_name": "Nollningsutksottet",
        "name": "Victor Winkelmann",
        "stilid": "vi6253wi-s",
    },
    "dchip": {
        "proper_name": "D-chip",
        "name": "Klara Tjernström",
        "stilid": "kl4257tj-s",
    },
    "medalj": {
        "proper_name": "Medaljelele",
        "name": "Axel Rosenqvist",
        "stilid": "ax3833ro-s",
    },
}


with open("account_details.json", "r") as f:
    accout_details = json.load(f)
    f.close()


def get_str_rep(n):
    if int(n) == n:
        str_n = str(int(n))
    else:
        str_n = str(n).replace(".", ",")
    return str_n


def gen_tex(utskott, date, sales, pay_type):
    global master
    global accout_details
    global total_costs

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

    for product, info in sales.items():

        quantity = info["quantity"]
        price_per_product = info["price"]  # float(".".join(info["price"].split(",")))
        account = info["account"]
        total += abs(quantity) * price_per_product
        total_for_prodcut = abs(quantity) * price_per_product

        if account in account_report:
            account_report[account] += total_for_prodcut
        else:
            account_report[account] = total_for_prodcut

        varor += (
            f"{product.strip().capitalize()} & {account} & {get_str_rep(quantity)} & {get_str_rep(price_per_product)} & {get_str_rep(total_for_prodcut)}"
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
        get_str_rep(total),
        name,
        stilid,
    )

    if utskott == "cafe":
        description = r"""\newcommand{\beskrivning}{Försäljning av varor i Café}"""
    elif utskott == "sex":
        # TODO: write name of event
        description = r"""\newcommand{\beskrivning}{Sexmästeriets verksamhet}"""
    elif utskott == "aktu":
        description = (
            r"""\newcommand{\beskrivning}{Försäljning av varor i Aktivitetsutskottet}"""
        )
    else:
        description = r"""\newcommand{\beskrivning}{Försäljning}"""

    fordelning = r"\newcommand{\fordelning}{"
    for acc, s in account_report.items():
        fordelning += f"{acc} & {accout_details[str(acc)]} & {get_str_rep(s)}" + r"\\"
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
    print(utskott, total, account_report)
    total_costs += total
    return packages + commands_1 + description + fordelning + varor + rest


if __name__ == "__main__":
    filename = "zettle_sales.json"
    # filename = "values.json"
    with open(filename) as file:
        sale_report = json.load(file)
        file.close()

    # today = datetime.now().strftime("%Y-%m-%d")
    nbr = 1
    for pay_type, data in sale_report.items():
        for utskott, values in data.items():
            for date, sales in values.items():
                tex = gen_tex(utskott, date, sales, pay_type)

                filename = "tex/" + utskott + "_" + date + "_" + str(nbr) + ".tex"
                with open(filename, "w", encoding="utf-8") as f:
                    f.write(tex)
                    f.close
                nbr += 1
    print(total_costs)
