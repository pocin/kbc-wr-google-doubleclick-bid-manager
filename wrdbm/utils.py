def strip_json_tags(inpath, outpath):
    """the input json looks like this
    '{"lineItems": "actual,csv\ncontents,yes"}'
    so this function skips the first and last json string
    """
    offset_beginning = 15
    offset_tail = -2

    chunksize = 1024
    with open(inpath, 'r') as inf, open(outpath, 'w') as outf:
        # skip the first '{"lineItems": "' characters
        inf.seek(offset_beginning)
        while True:
            chunk = inf.read(chunksize)
            if len(chunk) < chunksize:
                # we are at the end and need to strip the "} characters
                outf.write(chunk[:offset_tail])
                break
            else:
                outf.write(chunk)
    return outpath
