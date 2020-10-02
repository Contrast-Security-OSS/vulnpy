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


class TestHashlibSHA1(BaseHashTest):
    @property
    def trigger_func(self):
        return hash.do_hashlib_sha1

    @property
    def good_input(self):
        return "hashme", "fb78992e561929a6967d5328f49413fa99048d06"


class TestHashlibNew(BaseHashTest):
    @property
    def trigger_func(self):
        return hash.do_hashlib_new

    @property
    def good_input(self):
        return (
            "hashme",
            "02208b9403a87df9f4ed6b2ee2657efaa589026b4cce9accc8e8a5bf3d693c86",
        )
