import pytest

from roview import ro_dict, ro_list, ro_set, roview


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
    rolst = ro_list(lst)

    assert rolst.__class__.__name__ == "listROView"
    assert isinstance(rolst, list)
    assert id(rolst.__original__) == id(lst)
    assert rolst == lst

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.append(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.clear()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.extend([1])
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.insert(0, 1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.pop(0)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.remove(5)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.reverse()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.sort()

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst += [1]
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst.foo = None

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        append = rolst.append
        append(123)

    with pytest.raises(AttributeError):
        rolst.foo

    assert 5 in rolst
    assert rolst.copy() == lst
    assert type(rolst.copy()) == list
    assert str(rolst) == "[5, 10, 0, [777]]"

    assert list(rolst) == lst
    assert type(list(rolst)) == list

    with pytest.raises(AttributeError, match=r"'list' object has no attribute '__dict__'"):
        rolst.__dict__

    with pytest.raises(AttributeError, match=r"'listROView' object has no attribute 'foo'"):
        object.__setattr__(rolst, "foo", True)


def test_rodict():
    dct = {"5": 5, "10": 10}
    rodct = ro_dict(dct)

    assert rodct.__class__.__name__ == "dictROView"
    assert isinstance(rodct, dict)
    assert id(rodct.__original__) == id(dct)
    assert rodct == dct

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct.clear()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct.pop("5")
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct.popitem()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct.setdefault("100", 100)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct.update({"100": 100})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        del rodct["5"]
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct["100"] = 100

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct.foo = None

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        update = rodct.update
        update({"100": 100})

    with pytest.raises(AttributeError):
        rodct.foo

    assert "5" in rodct
    assert rodct.copy() == dct
    assert type(rodct.copy()) == dict
    assert str(rodct) == "{'5': 5, '10': 10}"

    with pytest.raises(AttributeError, match=r"'dict' object has no attribute '__dict__'"):
        rodct.__dict__

    with pytest.raises(AttributeError, match=r"'dictROView' object has no attribute 'foo'"):
        object.__setattr__(rodct, "foo", True)


def test_roset():
    s = {0, 1, 2}
    roset = ro_set(s)

    assert roset.__class__.__name__ == "setROView"
    assert isinstance(roset, set)
    assert id(roset.__original__) == id(s)
    assert roset == s

    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.add(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.clear()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.difference_update({1})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.discard(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.intersection_update({1})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.pop()
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.remove(1)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.symmetric_difference_update({1})
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        roset.update({1})

    with pytest.raises(AttributeError):
        roset.foo

    assert 0 in roset
    assert roset.copy() == s
    assert type(roset.copy()) == set
    assert str(roset) == "{0, 1, 2}"

    with pytest.raises(AttributeError, match=r"'set' object has no attribute '__dict__'"):
        roset.__dict__

    with pytest.raises(AttributeError, match=r"'setROView' object has no attribute 'foo'"):
        object.__setattr__(roset, "foo", True)


def test_nested():
    lst = [[1]]

    rolst = ro_list(lst)
    rolst[0].clear()
    assert lst[0] == []

    rolst = ro_list(lst, nested=True)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rolst[0].clear()

    dct = {"a": {"b": "b"}}

    rodct = ro_dict(dct)
    rodct["a"].clear()
    assert rodct["a"] == {}

    rodct = ro_dict(dct, nested=True)
    with pytest.raises(AttributeError, match=r"Attribute '.*' is not enabled"):
        rodct["a"].clear()
