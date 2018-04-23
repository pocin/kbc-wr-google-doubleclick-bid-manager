from wrdbm.client import DBMWriter
from pathlib import Path

def main(datadir, credentials, dry_run):
    client = DBMWriter(**credentials)
    path_lineitems_in = Path(datadir) / 'in/tables/' / 'line_items.csv'
    path_lineitems_out = Path(datadir) / 'out/tables/' / 'line_items_status.csv'
    client.process_lineitems(path_lineitems_in, path_lineitems_out, dry_run=dry_run)
