from glob import glob
import os.path as path
import re

#def _

def parse(dirname):
    if path.isdir(dirname):
        flist = glob(path.join(dirname, '????-????-????-????'))
        accounts = []
        for file in flist:
            dlist = [re.split(r'[,;]', item) for item in open(file).readlines()[1:]]
            one_res = {'account': path.split(file)[1],
                       'create_date': None,
                       'close_date': None,
                       'capitalization': None,
                       'operations': []} # {'date': 'XXXX-XX-XX', 'amount': float(+-XXXX.XX)}
            for row in dlist:
                operation = row[0].strip()
                if operation == '@':
                    one_res['create_date'] = row[1].strip()
                    one_res['account'] = float(row[2])
                    if len(row) > 3 and row[3].strip():
                        one_res['capitalization'] = int(row[3])
                elif operation == '#':
                    one_res['close_date'] = row[1].strip()
                elif operation in '+-':
                    one_res['operations'].append({
                                           'date' : row[1].strip(),
                                           'add'  : float(row[0].strip() + row[2].strip())
                                           })
                else:
                    raise Exception("Undefined option <{0}> in file <{1}>.".format(operation, file))
            accounts.append(one_res)
        return accounts
