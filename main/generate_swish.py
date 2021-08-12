import json
from datetime import datetime

master={
  "cafe":
    {"name": "Love Barany", "stilid": "lo5050ba-s"},
  "sex":
    {"name": "Marie Ask Uggla", "stilid": "ma"}
}

def gen_tex(utskott, date_amounts):
    global master
    name=master[utskott]['name']
    name=master[utskott]['stilid']
    today=datetime.now().strftime('%Y-%m-%d')

    sum=0

    packages="""\documentclass{article}
    \usepackage[utf8]{inputenc}
    \usepackage[a4paper, margin=0.8in]{geometry}
    \usepackage{palatino}
    \usepackage{graphicx}
    \usepackage{longtable}
    """

    commands_1 = """\newcommand{\skapad}{%s}
    \newcommand{\kostnadsstalle}{%s}
    \newcommand{\typ}{%s}
    \newcommand{\datum}{%s}
    \newcommand{\summa}{%s kr}
    \newcommand{\namn}{%s}
    \newcommand{\stilid}{%s}
    """ % (today, utskott, "Swish", date, sum, name, stilid)

    commands_2 = """\newcommand{\beskrivning}{Försäljning av varor i Cafe}
    \newcommand{\fordelning}{3000 & Försäljning & 4500 \\}
    \newcommand{\varor}{Bil & 3000 & 1 & 4500 & 4500 \\}
    """

    rest = ""
    return packages+commands_1+commands_2+rest

if __name__ == "__name__":
    filename="values.json"
    with open(filename) as file:
        data=json.load(file)
        file.close()

    for utskott,values in data.items():
        tex = gen_tex(utskott, values)



    rest = """\begin{document}
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
