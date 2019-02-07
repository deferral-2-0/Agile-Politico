
from app.api.utils import is_valid_string, is_valid_int


def test_is_valid_string_with_empty_string():
    assert(is_valid_string("")) == False


def test_is_valid_string_with_string():
    assert(is_valid_string("tev")) == True


def test_is_valid_string_with_int():
    assert(is_valid_string(122)) == False


def test_is_valid_int_with_int():
    assert(is_valid_int(12)) == True


def test_is_valid_int_with_string():
    assert(is_valid_int("dfee")) == False


def test_is_valid_int_with_0():
    assert(is_valid_int(0)) == True
