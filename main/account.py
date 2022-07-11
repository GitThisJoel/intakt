import json

# from account import account_of
# account = account_of(prefix)

account_files = "assets/accounts.json"
with open(account_files) as f:
    accounts = json.load(f)
    f.close()


def account_of(id):
    global accounts
    try:
        return accounts[id]["account"]
    except Exception as e:
        # Should an exception be raised here instead?
        return 3000
