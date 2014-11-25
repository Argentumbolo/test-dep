import re
import db

def parse_interest_test_data(filename):
    rows = [re.split(r'[,;:]', row) for row in open(filename) if row.strip()]
    res = []
    for row in rows:
        day_of_entry = row[0].strip()
        from_amount = float(row[1])
        one_day_interest = float(row[2])
        res.append((day_of_entry, from_amount, one_day_interest))
    return res

def main():
    itest = parse_interest_test_data('percents_table.csv')
    db.add_interest_plan_points(itest)
    
    for balance in (2.5, 25, 250, 2500, 250000, 2500000):
        for date in ('2014-11-20', '2015-01-17', '2015-04-13', '2015-05-15'):
            print date, balance, db.get_interest_amount(date, balance)
    
    

if __name__ == '__main__':
    db.connect("a.dbt")
    main()
