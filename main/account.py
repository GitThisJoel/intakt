import json

account_files = "main/accounts.json"
with open(account_files) as f:
    accounts = json.load(f)
    f.close()


def account_of(id):
    global accounts
    try:
        return accounts[id]["account"]
    except Exception as e:
        return 3000 
