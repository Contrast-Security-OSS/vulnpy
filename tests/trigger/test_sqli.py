from vulnpy.trigger import sqli
from tests.trigger.base_test import BaseTriggerTest


class BaseSqliTest(BaseTriggerTest):
    """All SQLi triggers catch their exceptions"""

    @property
    def exception_input(self):
        return "invalid ' sql"

    def test_exception(self):
        pass

    def test_exception_caught(self):
        assert self.trigger_func(self.exception_input) == "error"

    @property
    def good_input(self):
        return "d', '4'),('e", "a,3;b,5;c,1;d,4;e,1"


class TestSqliteExecute(BaseSqliTest):
    @property
    def trigger_func(self):
        return sqli.do_sqlite3_execute


class TestSqliteExecutemany(BaseSqliTest):
    @property
    def trigger_func(self):
        return sqli.do_sqlite3_executemany


class TestSqliteExecutescript(BaseSqliTest):
    @property
    def trigger_func(self):
        return sqli.do_sqlite3_executescript
