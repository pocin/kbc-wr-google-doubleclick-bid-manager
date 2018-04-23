"""
Helper stuff

"""
import csv
import datetime
import requests
import logging
from urllib.parse import urljoin

class DBMClient:
    def __init__(self, client_id, client_secret, refresh_token, version='v1'):
        self.client_id = client_id
        self.client_secret = client_secret
        self.refresh_token = refresh_token
        self._access_token = None
        self.version = version
        self.root_url = 'https://www.googleapis.com/doubleclickbidmanager/{}/'.format(version)

    @property
    def access_token(self):
        if self._access_token is None:
            logging.debug("Authenticating...")
            url = 'https://accounts.google.com/o/oauth2/token'
            data = {
                'refresh_token': self.refresh_token,
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'grant_type': 'refresh_token'
            }
            resp = requests.post(url, data=data)
            try:
                resp.raise_for_status()
            except Exception as e:
                logging.exception(resp.text)
                raise
            else:
                self._access_token = resp.json()['access_token']
        return self._access_token

    def _auth_request(self, method, endpoint, **requests_kwargs):
        url = urljoin(self.root_url, endpoint.lstrip('/'))
        headers = {'Authorization': "Bearer {}".format(self.access_token)}
        resp = requests.request(method, url, headers=headers, **requests_kwargs)
        try:
            resp.raise_for_status()
        except requests.HTTPError as e:
            logging.exception(resp.text)
            raise
        else:
            return resp.json()
    def post(self, endpoint, json):
        return self._auth_request("POST", endpoint, json=json)

class DBMWriter(DBMClient):
    def upload_lineitems(self, items, dry_run=True):
        payload = {'lineItems': items, 'dryRun': dry_run}
        return self.post('/lineitems/uploadlineitems', json=payload)

    @staticmethod
    def lineitems_response_to_csv(
            resp_json,
            outpath='/data/out/files/line_items_status.json'):
        logging.info("Serializing job status to csv")
        errors = resp_json['uploadStatus']['errors']
        if errors:
            raise ValueError("couldn't upload lineitems: %s", errors)
        try:
            first_row = resp_json['uploadStatus']['rowStatus'][0]
        except IndexError:
            logging.info("No rows in the input lineitems csv!")
            return None
        with open(outpath, 'w') as outf:
            writer = csv.DictWriter(outf, fieldnames=first_row.keys())
            writer.writeheader()
            writer.writerow(first_row)
            for row in resp_json['uploadStatus']['rowStatus'][1:]:
                writer.writerow(row)

        return outpath

    def process_lineitems(self, path_in, path_out, dry_run=True):
        """
        Read csv, make request, log response to csv

        """
        logging.info("Processing %s with dry_run=%s", path_in, dry_run)
        with open(path_in, 'r') as fin:
            csv_items = csv.reader(fin).read()
        resp = self.upload_lineitems(items=csv_items, dry_run=dry_run)

        logging.info("Serializing status to %s", path_out)
        true_outpath = DBMWriter.lineitems_response_to_csv(resp, path_out)
        return true_outpath

