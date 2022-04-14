import json
from requests_oauthlib import OAuth2Session

access_file = "access_2.json"
with open(access_file) as f:
    access_cred = json.load(f)
    f.close()

client_id = access_cred['client_id']
client_secret = access_cred['client_secret']
redirect_uri="https://httpbin.org/get"

url = "https://purchase.izettle.com/purchases/v2"

authorization_base_url = "https://oauth.zettle.com/authorize"
token_url = "https://oauth.zettle.com/token"
scope = ["READ:PURCHASE"]

zettle = OAuth2Session(client_id, 
        scope=scope, 
        redirect_uri=redirect_uri)

authrization_url, state = zettle.authorization_url(authorization_base_url)

print(authrization_url, state)

redirect_response = input()

print(client_id)

ret = zettle.fetch_token(token_url,
        include_client_id=True, 
        client_secret=client_secret, 
        authorization_response=redirect_response
    )

r = zettle.get("https://purchase.izettle.com/purchases/v2?limit=50&descending=true")
print(r)




