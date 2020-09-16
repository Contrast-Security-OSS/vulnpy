import pickle
from six import PY2

from vulnpy.trigger import deserialization
from tests.trigger.base_test import BaseTriggerTest


class BasePickleTest(object):
    @property
    def good_input(self):
        return "cos\nsystem\n(S'echo hacked'\ntR.", 0

    @property
    def exception_input(self):
        return "bad"

    @property
    def exception_raised(self):
        if PY2:
            return IndexError
        return pickle.UnpicklingError


class TestPickleLoad(BasePickleTest, BaseTriggerTest):
    @property
    def trigger_func(self):
        return deserialization.do_pickle_load


class TestPickleLoads(BasePickleTest, BaseTriggerTest):
    @property
    def trigger_func(self):
        return deserialization.do_pickle_loads


class BaseYamlTest(object):
    @property
    def good_input(self):
        return '!!python/object/apply:subprocess.Popen [["echo", "Hello World"]]', None

    @property
    def exception_input(self):
        return " Foo: !Ref bar"

    def test_exception(self):
        pass

    def test_exception_caught(self):
        self.trigger_func(self.exception_input)


class TestYamlLoad(BaseYamlTest, BaseTriggerTest):
    @property
    def trigger_func(self):
        return deserialization.do_yaml_load


class TestYamlLoadAll(BaseYamlTest, BaseTriggerTest):
    @property
    def trigger_func(self):
        return deserialization.do_yaml_load_all
