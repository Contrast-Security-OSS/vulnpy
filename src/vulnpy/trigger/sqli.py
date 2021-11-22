import sqlite3

SELECT_ALL = "SELECT * FROM Character"


def _db_reset():
    db_connection = sqlite3.connect(":memory:", check_same_thread=False)
    db_connection.executescript(
        """
        DROP TABLE IF EXISTS Character;
        CREATE TABLE Character(value, count);
        INSERT INTO Character VALUES
            ('a', '3'),('b', '5'),('c', '1')
        """
    )
    db_connection.commit()
    return db_connection


def _execute(db_func):
    try:
        db_connection = _db_reset()
        cursor = db_connection.cursor()
        db_func(cursor)
        all_rows = cursor.execute(SELECT_ALL)
        return ";".join([",".join(row) for row in all_rows])
    except Exception:
        return "error"


EXECUTE_QUERY_FMT = "INSERT INTO Character VALUES ('{}', '1')"


def do_sqlite3_execute(user_input):
    def execute(cursor):
        sql = EXECUTE_QUERY_FMT.format(user_input)
        cursor.execute(sql)

    return _execute(execute)


EXECUTEMANY_QUERY_FMT = "INSERT INTO Character VALUES ('{}', ?)"


def do_sqlite3_executemany(user_input):
    def executemany(cursor):
        sql = EXECUTEMANY_QUERY_FMT.format(user_input)
        cursor.executemany(sql, [("1")])

    return _execute(executemany)


EXECUTESCRIPT_QUERY_FMT = "INSERT INTO Character VALUES ('{}', '1'); SELECT 0"


def do_sqlite3_executescript(user_input):
    def executescript(cursor):
        sql = EXECUTESCRIPT_QUERY_FMT.format(user_input)
        return cursor.executescript(sql)

    return _execute(executescript)
