from vulnpy.trigger import rand
from tests.trigger.base_test import BaseTriggerTest


class BaseRandomTest(BaseTriggerTest):
    @property
    def exception_input(self):
        return []


# The return values in these tests are always the same, because
# we use the user's input as the seed


class TestRandom(BaseRandomTest):
    @property
    def trigger_func(self):
        return rand.do_random

    @property
    def good_input(self):
        return "my-seed1", "0.9353490848502687"


class TestRandint(BaseRandomTest):
    @property
    def trigger_func(self):
        return rand.do_randint

    @property
    def good_input(self):
        return "my-seed2", "72"


class TestRandrange(BaseRandomTest):
    @property
    def trigger_func(self):
        return rand.do_randrange

    @property
    def good_input(self):
        return "my-seed3", "50"


class TestUniform(BaseRandomTest):
    @property
    def trigger_func(self):
        return rand.do_uniform

    @property
    def good_input(self):
        return "my-seed4", "6.239853530761573"
