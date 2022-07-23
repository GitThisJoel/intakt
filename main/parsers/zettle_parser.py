# Used to retreive Zettle purchase data using their API.


# Used to generate the JSON-object from the Zettle API respnose.
import sys, os

from datetime import datetime
from datetime import timedelta
from requests_oauthlib import OAuth2Session
import json

from parsers.parser import Parser


class ZettleParser(Parser):
    @staticmethod
    def parse(data, time_delta):
        pass

    @staticmethod
    def get_data(start_date: datetime, end_date: datetime):
        access_file = os.path.dirname(os.path.realpath(__file__)) + "/../credentials/access.json"
        with open(access_file) as f:
            access_cred = json.load(f)
            f.close()

        client_id = access_cred["client_id"]
        client_secret = access_cred["client_secret"]
        redirect_uri = "https://httpbin.org/get"

        authorization_base_url = "https://oauth.zettle.com/authorize"
        token_url = "https://oauth.zettle.com/token"
        scope = ["READ:PURCHASE"]

        zettle = OAuth2Session(client_id, scope=scope, redirect_uri=redirect_uri)
        authorization_url, _ = zettle.authorization_url(authorization_base_url)

        # TODO: can this be done without human interaction?
        redirect_response = input(authorization_url + "\n")

        zettle.fetch_token(
            token_url,
            include_client_id=True,
            client_secret=client_secret,
            authorization_response=redirect_response,
        )

        if end_date is None:
            end_date = start_date + timedelta(days=1)

        r = zettle.get(
            f"https://purchase.izettle.com/purchases/v2?startDate={start_date.isoformat()}&endDate={end_date.isoformat()}&descending=true"
        )

        return r.json()
