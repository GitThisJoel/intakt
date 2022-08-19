import os
from dataclasses import dataclass, asdict
from datetime import date
import json
import inspect

from helpers.asset_loader import AssetLoader

al = AssetLoader()


@dataclass
class TexCommands:
    skapad: str
    kostnadsstalle: str
    typ: str
    datum: str
    summa: str
    namn: str
    stillid: str
    beskrivning: str
    fordelning: str
    varor: str

    def __str__(self):
        kw = asdict(self)
        s = ""
        for k, w in kw.items():
            s += "\\newcommand{" + str(k) + "}{" + str(w) + "}\n"
        return s


class TexCompiler:
    def __init__(self, sales_fp, intakt_type):
        with open(sales_fp, "r") as f:
            self.sales = json.load(f)
            f.close()

        self.intakt_type = intakt_type
        self.intakt_skeleton = (
            os.path.dirname(os.path.realpath(inspect.getfile(self.__class__))) + "/intakt.tex"
        )
        self.today = date.today().isoformat()

    def _beskrivningfordelning_fordelning_sum(self, sales):
        summa = 0
        fordelning = ""
        varor = ""

        acc_map = {}

        for _, sale in sales.items():
            tot = sale["quantity"] * sale["unit_price"]
            name = sale["name"]
            account = sale["account"]
            unit_price = sale["unit_price"]

            summa += tot
            varor += f"{name} & {account} & {unit_price} & {tot}\\\\"
            if account in acc_map:
                acc_map[account] += tot
            else:
                acc_map[account] = tot

        for acc, sales in acc_map.items():
            fordelning += f"{acc} & {al.account_description[str(acc)]} & {sales}\\\\"

        return summa, fordelning, varor

    def _prepend_commands(self):
        cmds = str(self.tex_commands)
        with open(self.tex_file, "w") as temp_f:
            with open(self.intakt_skeleton, "r") as skel_f:
                tex_skeleton = skel_f.read()
                skel_f.close()
            temp_f.seek(0)
            temp_f.write(cmds)
            temp_f.write(tex_skeleton)
            temp_f.truncate()
            temp_f.close()

    def compile_all(self) -> None:

        for utskott, date_sales in self.sales.items():
            master = al.masters[utskott]
            for date, sales in date_sales.items():
                date_str = date.replace("-", "_")
                self.tex_file = (
                    os.path.dirname(os.path.realpath(inspect.getfile(self.__class__)))
                    + f"/{utskott}{date_str}.tex"
                )

                summa, fordelning, varor = self._beskrivningfordelning_fordelning_sum(sales)

                self.tex_commands = TexCommands(
                    **{
                        "skapad": self.today,
                        "kostnadsstalle": master["proper_name"],
                        "typ": self.intakt_type,
                        "datum": date,
                        "summa": summa,
                        "namn": master["name"],
                        "stillid": master["stilid"],
                        "beskrivning": master["description"],
                        "fordelning": fordelning,
                        "varor": varor,
                    }
                )

                self._prepend_commands()

                os.system(
                    f"pdflatex -output-directory=intaktsrakningar {self.tex_file} && rm {self.tex_file}"
                )
