import csv
import pytest
from wrdbm.utils import strip_json_tags

def test_cleaning_lineitems_json(tmpdir):

    infile = tmpdir.join("lineitems_input.json")
    infile.write('{"lineItems": "columnA,columnB\nvalue,value2"}')
    outfile = tmpdir.join("outfile.csv")

    strip_json_tags(infile.strpath, outfile.strpath)

    with open(outfile.strpath) as inf:
        reader = csv.DictReader(inf)
        first_line = next(reader)
        assert first_line['columnA'] == 'value'
        assert first_line['columnB'] == 'value2'
        assert len(first_line.keys()) == 2
        with pytest.raises(StopIteration):
            next(reader)


