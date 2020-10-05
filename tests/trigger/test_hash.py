from vulnpy.trigger import hash
from tests.trigger.base_test import BaseTriggerTest


class BaseHashTest(BaseTriggerTest):
    @property
    def exception_input(self):
        return None


class TestHashlibMD5(BaseHashTest):
    @property
    def trigger_func(self):
        return hash.do_hashlib_md5

    @property
    def good_input(self):
        return "hashme", "533f6357e0210e67d91f651bc49e1278"


class BaseSHA1Test(BaseHashTest):
    @property
    def good_input(self):
        return "hashme", "fb78992e561929a6967d5328f49413fa99048d06"


class TestHashlibSHA1(BaseSHA1Test):
    @property
    def trigger_func(self):
        return hash.do_hashlib_sha1


class TestHashlibNew(BaseSHA1Test):
    @property
    def trigger_func(self):
        return hash.do_hashlib_new
