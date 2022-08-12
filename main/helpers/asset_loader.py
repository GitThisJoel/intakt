import sys, os, inspect
import json

class AssetLoader():

    def __init__(self):
        self._asset_directory = os.path.dirname(os.path.realpath(inspect.getfile(self.__class__))) +  "/../assets/"
        self.load_assets()

    def _read_file(fp):
        with open(fp, "r") as f:
            content = json.load(f)
        f.close()
        return content

    def load_assets(self):
        account_description_fp = self._asset_directory + "account_description.json"
        accounts_fp = self._asset_directory + "accounts.json"
        masters_fp = self._asset_directory + "masters.json"

        self.account_description = read_file(account_description_fp)
        self.accounts = read_file(accounts_fp)
        self.masters = read_file(masters_fp)

