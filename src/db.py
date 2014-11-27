import sqlite3

_db = None

def _create_all():
    global _db
    _db.execute("CREATE TABLE IF NOT EXISTS interest_plan (\n"
                "    day_of_entry     DATE NOT NULL,\n"
                "    from_amount      REAL NOT NULL,\n"
                "    one_day_interest REAL NOT NULL,\n"
                "    PRIMARY KEY(day_of_entry, from_amount)\n"
                ")")
    _db.execute("CREATE TABLE IF NOT EXISTS deposits (\n"
                "    id                    INTEGER PRIMARY KEY ASC,\n"
                "    account               TEXT UNIQUE NOT NULL,\n"
                "    create_date           DATE NOT NULL,\n"
                "    balance               REAL NOT NULL,\n" # REAL for simplicity, look strategy of rounding.
                "    capitalization_period INTEGER\n"        # NULL: withot capitalization; 0: monthly; >0: period in days.
                ")")
    _db.execute("CREATE TABLE IF NOT EXISTS interest (\n"
                "    id         INTEGER PRIMARY KEY ASC,\n"
                "    account_id INTEGER NOT NULL,\n"
                "    amount     REAL,\n"
                "    FOREIGN KEY(account_id) REFERENCES deposits(id)\n"
                ")")

def connect(dbname):
    global _db
    _db = sqlite3.connect(dbname)
    _create_all()

def close():
    global _db
    _db.close()

# values is list of tuples (day_of_entry, from_amount, one_day_interest)
def add_interest_plan_points(values):
    global _db
    cur = _db.cursor()
    cur.executemany("INSERT OR REPLACE\n"
                    "INTO interest_plan(day_of_entry, from_amount, one_day_interest)\n"
                    "VALUES(?, ?, ?)", values)
    cur.close()
    _db.commit()

def add_new_deposit(account, create_date, balance, capitalization_period):
    global _db
    cur = _db.cursor()
    cur.executemany("INSERT\n"
                    "INTO deposits(account, create_date, balance, capitalization_period)\n"
                    "VALUES(?, ?, ?, ?)", [account, create_date, balance, capitalization_period])
    cur.close()
    _db.commit()

def get_interest_amount(date, balance):
    global _db
    interest = _db.execute("SELECT ODI\n"
                           "FROM ( SELECT interest_plan.day_of_entry      as PDE,\n"
                           "              interest_plan.from_amount       as PFA,\n"
                           "              interest_plan.one_day_interest  as ODI\n"
                           "       FROM interest_plan\n"
                           "       WHERE PDE <= :date AND PFA <= :balance\n"
                           "       GROUP BY PFA\n"
                           "       ORDER BY PDE ASC\n"
                           "     )\n"
                           "ORDER BY PFA DESC\n"
                           "LIMIT 1",
                           {'date': date, 'balance': balance}).fetchone()[0]
    return float(interest)

#connect("a.dbt")
#close()
