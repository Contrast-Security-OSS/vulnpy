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


class TestHttpsconnectionRequestUrl(BaseHttpconnectionUrlTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_request_url


class TestHttpsconnectionPutrequestUrl(BaseHttpconnectionUrlTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_putrequest_url


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


class TestHttpsconnectionRequestMethod(BaseHttpconnectionMethodTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_request_method


class TestHttpsconnectionPutrequestMethod(BaseHttpconnectionMethodTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_putrequest_method


class BaseHttpconnectionInitTest(BaseSsrfTest):
    @property
    def good_input(self):
        return ssrf.TRUSTED_HOST, 200


class TestHttpconnectionInit(BaseHttpconnectionInitTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpconnection_init


class TestHttpsconnectionInit(BaseHttpconnectionInitTest):
    @property
    def trigger_func(self):
        return ssrf.do_httpsconnection_init
