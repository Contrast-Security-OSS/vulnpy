import mock
import os
import pytest

from vulnpy.trigger import ssrf
from tests.trigger.base_test import BaseTriggerTest


class BaseSsrfTest(BaseTriggerTest):
    """All SSRF triggers catch their exceptions"""

    @property
    def exception_input(self):
        return None

    def test_exception(self):
        pass

    def test_exception_caught(self):
        self.trigger_func(self.exception_input)


class BaseUrlopenTest(BaseSsrfTest):
    @property
    def good_input(self):
        return "http://example.com", 200


class TestLegacyUrlopen(BaseUrlopenTest):
    @property
    def trigger_func(self):
        return ssrf.do_legacy_urlopen


class TestUrlopenStr(BaseUrlopenTest):
    @property
    def trigger_func(self):
        return ssrf.do_urlopen_str


class TestUrlopenObj(BaseUrlopenTest):
    @property
    def trigger_func(self):
        return ssrf.do_urlopen_obj


class BaseHttpconnectionUrlTest(BaseSsrfTest):
    @property
    def good_input(self):
        return ssrf.TRUSTED_URL, 200


class TestHttpconnectionRequestUrl(BaseHttpconnectionUrlTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpconnection_request_url


class TestHttpconnectionPutrequestUrl(BaseHttpconnectionUrlTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpconnection_putrequest_url


class BaseHttpconnectionMethodTest(BaseSsrfTest):
    @property
    def good_input(self):
        return ssrf.TRUSTED_METHOD, 200


class TestHttpconnectionRequestMethod(BaseHttpconnectionMethodTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpconnection_request_method


class TestHttpconnectionPutrequestMethod(BaseHttpconnectionMethodTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpconnection_putrequest_method


class TestHttpconnectionInit(BaseSsrfTest):
    @property
    def good_input(self):
        return ssrf.TRUSTED_HOST, 200

    @property
    def trigger_func(self):
        return ssrf.do_httpconnection_init


# HTTPS tests raise an internal exception because we haven't figured out how
# to properly mock the socket connection without crashing python inside of
# the ssl module. These tests do still call each trigger, however, so they're
# sufficient for unit testing purposes.


class BaseHttpsconnectionUrlTest(BaseSsrfTest):
    @property
    def good_input(self):
        return ssrf.TRUSTED_URL, ssrf.EXCEPTION_CODE


class TestHttpsconnectionRequestUrl(BaseHttpsconnectionUrlTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_request_url


class TestHttpsconnectionPutrequestUrl(BaseHttpsconnectionUrlTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_putrequest_url


class BaseHttpsconnectionMethodTest(BaseSsrfTest):
    @property
    def good_input(self):
        return ssrf.TRUSTED_METHOD, ssrf.EXCEPTION_CODE


class TestHttpsconnectionRequestMethod(BaseHttpsconnectionMethodTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_request_method


class TestHttpsconnectionPutrequestMethod(BaseHttpsconnectionMethodTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_putrequest_method


class TestHttpsconnectionInit(BaseSsrfTest):
    @property
    def good_input(self):
        return ssrf.TRUSTED_HOST, ssrf.EXCEPTION_CODE

    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_init


@pytest.fixture(scope="class")
def unmock_connection():
    """
    Enable a real SSRF request for just one test.
    """
    with mock.patch.dict(
        os.environ, {"VULNPY_REAL_SSRF_REQUESTS": "any-nonzero-value"}
    ):
        yield


@pytest.mark.usefixtures("unmock_connection")
class TestUrlopenStrUnmocked(BaseUrlopenTest):
    @property
    def trigger_func(self):
        return ssrf.do_urlopen_str
