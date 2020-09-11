import pytest

from vulnpy.trigger import get_trigger


def test_get_trigger_does_not_exist():
    with pytest.raises(AttributeError) as exc:
        get_trigger(pytest, "nope")

    assert "do_nope" in str(exc)
