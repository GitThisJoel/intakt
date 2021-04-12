import parser
vals=r'''
\newcommand{\skapad}{2021-02-01}
\newcommand{\kostnadsstalle}{Sektionen}
\newcommand{\typ}{Swish}
\newcommand{\namn}{Joel Bäcker}
\newcommand{\stilid}{jo4383ba-s}

'''
def cmds(date, purchases):

t=parser.parse()
for k in t:

s=r'''
\newcommand{\datum}{2021-02-01}
\newcommand{\summa}{4500 kr}
\newcommand{\beskrivning}{Försäljning av bil}
\newcommand{\fordelning}{3000 & Försäljning & 4500 \\}
\newcommand{\varor}{Bil & 3000 & 1 & 4500 & 4500 \\}
'''
