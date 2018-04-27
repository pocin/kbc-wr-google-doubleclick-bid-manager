"""extractor
"""
from wrdbm.client import DBMClient
import ijson

class DBMExtractor(DBMClient):
    def download_lineitems(self, outpath, filter_type, filter_ids=None):
        ok_filter_types = {"ADVERTISER_ID", "INSERTION_ORDER_ID", "LINE_ITEM_ID"}
        if filter_type not in ok_filter_types:
            err = ("when downloading lineitems, 'filterType' must be one of '{}', "
                   "not '{}'".format(ok_filter_types, filter_type))
            raise ValueError(err)

        payload = {
            "filterType": filter_type,
        }
        if filter_ids:
            payload["filterIds"] = filter_ids

        with open(outpath, 'wb') as out:
            for chunk in self.post_stream("/lineitems/downloadlineitems", json=payload):
                out.write(chunk)
        return outpath

    def clean_lineitems_response(self, inpath, outpath):
        with open(inpath) as inf, open(outpath) as outf:
            ijson.items(inf, 'lineitems')

