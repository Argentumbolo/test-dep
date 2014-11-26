import re
import db
import interest_test_data


def main(filename):
    itest = interest_test_data.parse(filename)
    db.add_interest_plan_points(itest)
    
    for balance in (2.5, 25, 250, 2500, 250000, 2500000):
        for date in ('2014-11-20', '2015-01-17', '2015-04-13', '2015-05-15'):
            print date, balance, db.get_interest_amount(date, balance)


if __name__ == '__main__':
    db.connect("a.dbt")
    # main('percents_table.xls')
    main('percents_table.csv')
