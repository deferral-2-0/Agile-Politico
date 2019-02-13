

from app.api.v1.utils import get_all_items, get_specific_item


def test_invalid_model_type_on_getting_all_items():
    assert(get_all_items(None, "notpresent")) == []


def test_invalid_model_type_on_getting_specific_item():
    assert(get_specific_item(None, "dsd", "notpresent")) == []
