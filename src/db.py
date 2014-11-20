import sqlite3

_db = None

def _create_all():
    global _db
    _db.execute("CREATE TABLE IF NOT EXISTS [percents] ("
                "    [day_of_entry]     DATE NOT NULL,"
                "    [from_amount]      REAL NOT NULL,"
                "    [one_day_interest] REAL NOT NULL,"
                "    PRIMARY KEY(day_of_entry, from_sum)"
                ")")
    _db.execute("CREATE TABLE IF NOT EXISTS [deposits] ("
                "    [id]                    INTEGER PRIMARY KEY ASC,"
                "    [account]               TEXT UNIQUE NOT NULL,"
                "    [create_date]           DATE NOT NULL,"
                "    [balance]               REAL NOT NULL," # REAL for simplicity, look [strategy of rounding].
                "    [capitalization_period] INTEGER"        # NULL: withot capitalization; 0: monthly; >0: period in days.
                ")")
    _db.execute("CREATE TABLE IF NOT EXISTS [interest] (    "
                "    [id] INTEGER PRIMARY KEY ASC,"
                "    [account_id] INTEGER NOT NULL,"
                "    [amount] REAL,"
                "    FOREIGN KEY(account_id) REFERENCES [deposits](id)"
                ")")

def connect(dbname):
    global _db
    _db = sqlite3.connect(dbname)
    _create_all()

def close():
    global _db
    _db.close()

def get_interest_amount(date, balance):
    global _db
    _db.execute("SELECT day_of_entry as doe, one_day_interest as odi GROUP BY ")
    

connect("a.dbt")
close()
