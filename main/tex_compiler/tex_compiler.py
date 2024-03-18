import os
import json
import inspect

from dataclasses import dataclass, asdict
from datetime import date

from helpers.asset_loader import AssetLoader
from helpers.path_handler import tex_dir

al = AssetLoader()


@dataclass
class TexCommands:
    skapad: str
    kostnadsstalle: str
    typ: str
    datum: str
    summa: str
    namn: str
    stilid: str
    beskrivning: str
    fordelning: str
    varor: str

    def __str__(self):
        kw = asdict(self)
        s = ""
        for k, w in kw.items():
            s += "\\newcommand{\\" + str(k) + "}{" + str(w) + "}\n"
        return s


class TexCompiler:
    def __init__(
        self, sales_fp, intakt_type, output_fp, keep_tex, zettle_fee_mode=False
    ):
        with open(sales_fp, "r") as f:
            self.sales = json.load(f)
            f.close()

        self.intakt_type = intakt_type
        _skeleton_file_name = "zettleavgift.tex" if zettle_fee_mode else "intakt.tex"
        self.intakt_skeleton = tex_dir() / _skeleton_file_name

        self.today = date.today().isoformat()

        self.output_fp = output_fp
        self.keep_tex = keep_tex
        self.zettle_fee_mode = zettle_fee_mode

    def _conv_to_crown(self, x):
        s = str(x)
        return s[:-2] + "," + s[-2:]

    def _beskrivningfordelning_fordelning_sum(self, sales):
        summa = 0
        fordelning = ""
        varor = ""

        acc_map = {}

        for _, sale in sorted(sales.items(), key=lambda x: x[0].lower()):
            name = (
                sale["name"]
                .replace("\\", "\\textbackslash")
                .replace("&", "\&")
                .replace("$", "\$")
            )
            quantity = sale["quantity"]
            account = sale["account"]
            unit_price = sale["unit_price"]
            tot = quantity * unit_price

            summa += tot
            if self.zettle_fee_mode:
                varor += (
                    " & ".join((name, str(account), self._conv_to_crown(tot))) + "\\\\"
                )
            else:
                varor += (
                    " & ".join(
                        (
                            name,
                            str(account),
                            str(quantity),
                            self._conv_to_crown(unit_price),
                            self._conv_to_crown(tot),
                        )
                    )
                    + "\\\\"
                )
            if account in acc_map:
                acc_map[account] += tot
            else:
                acc_map[account] = tot

        for acc, sales in sorted(acc_map.items()):
            fordelning += f"{acc} & {al.account_description[str(acc)]} & {self._conv_to_crown(sales)}\\\\"

        return self._conv_to_crown(summa), fordelning, varor

    def _prepend_commands(self):
        cmds = str(self.tex_commands)
        with open(self.intakt_skeleton, "r") as skel_f:
            tex_skeleton = skel_f.read()
        with open(self.tex_file, "w") as temp_f:
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
                self.tex_file = tex_dir() / f"{utskott}{date_str}.tex"

                summa, fordelning, varor = self._beskrivningfordelning_fordelning_sum(
                    sales
                )

                self.tex_commands = TexCommands(
                    **{
                        "skapad": self.today,
                        "kostnadsstalle": master["proper_name"],
                        "typ": self.intakt_type,
                        "datum": date,
                        "summa": summa,
                        "namn": master["name"],
                        "stilid": master["stilid"],
                        "beskrivning": master["description"],
                        "fordelning": fordelning,
                        "varor": varor,
                    }
                )

                self._prepend_commands()

                os.system(
                    "&&".join(
                        [
                            f"pdflatex -output-directory=intaktsrakningar {self.tex_file}",
                            f"rm intaktsrakningar/{utskott}{date_str}.log",
                            f"rm intaktsrakningar/{utskott}{date_str}.aux",
                            f"rm {self.tex_file}" if not self.keep_tex else "true",
                        ]
                    )
                )

        if self.output_fp is not None:
            os.system(f"pdfjam intaktsrakningar/*.pdf -o {self.output_fp}")

        return
