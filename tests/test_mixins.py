
from revision.mixins import DotDictMixin

def test_dot_notation():
    dic = DotDictMixin({
        "test_key": "test_value"
    })

    assert dic.test_key == "test_value"
    assert dic['test_key'] == "test_value"

    assert dic.test == None
    try:
        dic['test']
        assert False
    except KeyError:
        pass

def test_nested_notation_access():
    dic = DotDictMixin({
        "test_list": [
            "list_item_1"
        ],
        "test_dict": {
            "dict_item_key": "dict_item_val"
        }
    })

    assert isinstance(dic.test_list, list)
    assert len(dic.test_list) == 1
    for item in dic.test_list:
        assert item == "list_item_1"

    assert isinstance(dic.test_dict, dict)
    assert len(dic.test_dict) == 1
    assert "dict_item_key" in dic.test_dict
    assert dic.test_dict.dict_item_key == "dict_item_val"
