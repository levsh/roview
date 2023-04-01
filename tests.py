import pytest
from roview import rodict, rolist, roset, roview


def test_roview():
    class Obj:
        def __init__(self):
            self.x = 1

    obj = Obj()

    with pytest.raises(ValueError, match=r"'enabled_attrs' or 'disabled_attrs' should be not empty"):
        ro_obj = roview(obj)

    with pytest.raises(ValueError, match=r"Only one of \('enabled_attrs', 'disabled_attrs'\) are allowed, not both"):
        ro_obj = roview(obj, enabled_attrs=["__getattr__"], disabled_attrs=["__getattr__"])

    ro_obj = roview(obj, enabled_attrs=["__getattr__"])
    assert ro_obj.x == 1
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_obj.x = 0
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_obj.y = 0
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_obj.__dict__["x"] = 0


def test_rolist():
    lst = [5, 10, 0, [777]]
    ro_list = rolist(lst)

    assert ro_list.__class__.__name__ == "listROView"
    assert isinstance(ro_list, list)
    assert id(ro_list.__original__) == id(lst)
    assert ro_list == lst

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.append(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.clear()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.extend([1])
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.insert(0, 1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.pop(0)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.remove(5)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.reverse()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.sort()

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list += [1]
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list.foo = None

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        append = ro_list.append
        append(123)

    with pytest.raises(AttributeError):
        ro_list.foo

    assert 5 in ro_list
    assert ro_list.copy() == lst
    assert type(ro_list.copy()) == list
    assert str(ro_list) == "[5, 10, 0, [777]]"

    assert list(ro_list) == lst
    assert type(list(ro_list)) == list

    with pytest.raises(AttributeError, match=r"'list' object has no attribute '__dict__'"):
        ro_list.__dict__

    with pytest.raises(AttributeError, match=r"'listROView' object has no attribute 'foo'"):
        object.__setattr__(ro_list, "foo", True)

    assert rolist([1, 2, 3]) == rolist([1, 2, 3])
    assert rolist([1, 2, 3]) != rolist([3, 2, 1])
    assert (rolist([1, 2, 3]) == rolist([3, 2, 1])) is False


def test_rodict():
    dct = {"5": 5, "10": 10}
    ro_dict = rodict(dct)

    assert ro_dict.__class__.__name__ == "dictROView"
    assert isinstance(ro_dict, dict)
    assert id(ro_dict.__original__) == id(dct)
    assert ro_dict == dct

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict.clear()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict.pop("5")
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict.popitem()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict.setdefault("100", 100)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict.update({"100": 100})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        del ro_dict["5"]
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict["100"] = 100

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict.foo = None

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        update = ro_dict.update
        update({"100": 100})

    with pytest.raises(AttributeError):
        ro_dict.foo

    assert "5" in ro_dict
    assert ro_dict.copy() == dct
    assert type(ro_dict.copy()) == dict
    assert str(ro_dict) == "{'5': 5, '10': 10}"

    with pytest.raises(AttributeError, match=r"'dict' object has no attribute '__dict__'"):
        ro_dict.__dict__

    with pytest.raises(AttributeError, match=r"'dictROView' object has no attribute 'foo'"):
        object.__setattr__(ro_dict, "foo", True)

    assert rodict({"a": "A"}) == rodict({"a": "A"})
    assert rodict({"a": "A"}) != rodict({"b": "B"})
    assert (rodict({"a": "A"}) == rodict({"b": "B"})) is False


def test_roset():
    s = {0, 1, 2}
    ro_set = roset(s)

    assert ro_set.__class__.__name__ == "setROView"
    assert isinstance(ro_set, set)
    assert id(ro_set.__original__) == id(s)
    assert ro_set == s

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.add(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.clear()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.difference_update({1})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.discard(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.intersection_update({1})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.pop()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.remove(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.symmetric_difference_update({1})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_set.update({1})

    with pytest.raises(AttributeError):
        ro_set.foo

    assert 0 in ro_set
    assert ro_set.copy() == s
    assert type(ro_set.copy()) == set
    assert str(ro_set) == "{0, 1, 2}"

    with pytest.raises(AttributeError, match=r"'set' object has no attribute '__dict__'"):
        ro_set.__dict__

    with pytest.raises(AttributeError, match=r"'setROView' object has no attribute 'foo'"):
        object.__setattr__(ro_set, "foo", True)

    assert roset({1, 2, 3}) == roset({1, 2, 3})
    assert roset({1, 2, 3}) == roset({3, 2, 1})
    assert (roset({1, 2, 3}) != roset({3, 2, 1})) is False


def test_nested():
    lst = [[1]]

    ro_list = rolist(lst)
    ro_list[0].clear()
    assert lst[0] == []

    ro_list = rolist(lst, nested=True)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_list[0].clear()

    dct = {"a": {"b": "b"}}

    ro_dict = rodict(dct)
    ro_dict["a"].clear()
    assert ro_dict["a"] == {}

    ro_dict = rodict(dct, nested=True)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        ro_dict["a"].clear()
