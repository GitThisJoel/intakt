import json
from path_handler import main_dir


class AssetLoader:
    def __init__(self):
        self._asset_directory = main_dir() / "assets"
        self.load_assets()

    def _read_file(self, fp):
        with open(fp, "r") as f:
            content = json.load(f)
        f.close()
        return content

    def load_assets(self):
        account_description_fp = self._asset_directory / "account_description.json"
        utskptt_accounts_fp = self._asset_directory / "utskott_accounts.json"
        masters_fp = self._asset_directory / "masters.json"

        self.account_description = self._read_file(account_description_fp)
        self.utskott_accounts = self._read_file(utskptt_accounts_fp)
        self.masters = self._read_file(masters_fp)
