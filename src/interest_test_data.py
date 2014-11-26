import re
from os.path import splitext


def _parse_csv(filename):
    rows = [re.split(r'[,;]', row) for row in open(filename) if row.strip()]
    res = []
    for row in rows:
        day_of_entry = row[0].strip()
        from_amount = float(row[1])
        one_day_interest = float(row[2])
        res.append((day_of_entry, from_amount, one_day_interest))
    return res

def _parse_xls(filename):
    import xlrd
    
    res = []
    book = xlrd.open_workbook(filename, formatting_info = True)
    sheet = book.sheet_by_index(0)
    for nrow in xrange(sheet.nrows):
        row = sheet.row_values(nrow)
        if len(row) == 3 and row[0]:
            res.append((row[0], float(row[1]), float(row[2])))
    return res

def parse(filename):
    ext = splitext(filename)[1]
    if ext == '.csv':
        return _parse_csv(filename)
    elif ext == '.xls':
        return _parse_xls(filename)
    else:
        raise Exception("File format <{0}> not supported.".format(ext))
