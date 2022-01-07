import pytest

from vulnpy.utils.utils_string import ensure_binary, ensure_str


class TestStringManipulation(object):
    @pytest.mark.parametrize("val", [b"test", "i'm string"])
    def test_ensure_binary(self, val):
        if not isinstance(val, (bytes, str)):
            pass
        binary_data = ensure_binary(val)

        assert isinstance(binary_data, bytes)

    @pytest.mark.parametrize("val", [b"test", "i'm string", 123])
    def test_ensure_string(self, val):
        if not isinstance(val, (bytes, str)):
            with pytest.raises(TypeError) as e:
                ensure_str(val)
                assert f"not expecting type {type(val)}" == e.value
        else:
            text_data = ensure_str(val)
            assert isinstance(text_data, str)
