

from app.api.utils import get_all_items


def test_invalid_model_type_on_getting_all_items():
    assert(get_all_items(None, "notpresent")) == []
