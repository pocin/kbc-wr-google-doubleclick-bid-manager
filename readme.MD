# Keboola writer for Google Doubleclick Bid Manager
---
[![Build Status](https://travis-ci.org/pocin/kbc-wr-google-doubleclick-bid-manager.svg?branch=master)](https://travis-ci.org/pocin/kbc-wr-google-doubleclick-bid-manager)
---


Uses this endpoint https://developers.google.com/bid-manager/v1/lineitems/uploadlineitems for uploading line items in CSV format.

# Config

In the table input mapping create a table `/data/in/tables/line_items.csv`
It will be uploaded as is to the dcm

`config.json` 
```javascript
{
    "write": {
        "lineItems": {
            "dryRun": true
        }
    }
}
```

Set `dryRun` to `true` to get upload status without actually persisting the line items. Setting to `false` will do, well, a dry run.

The writer produces a table (overwritten on each run) `/data/out/tables/line_items_status.csv` with a report on failures and successes.

# Development

create `.env` file based on `.env_template` in the root of this repo.

https://developers.google.com/api-client-library/python/apis/doubleclickbidmanager/v1
https://github.com/googleads/googleads-bidmanager-examples/blob/master/python/util.py
