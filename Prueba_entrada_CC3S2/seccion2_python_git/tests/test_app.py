import pytest
from app.app import summarize


def test_summarize_ok():
    nums = ["1", "2", "3"]
    resultado = summarize(nums)
    assert resultado["count"] == 3
    assert resultado["sum"] == 6.0
    assert resultado["avg"] == 2.0


def test_summarize_lista_vacia():
    with pytest.raises(ValueError):
        summarize([])


def test_summarize_con_no_numericos():
    with pytest.raises(ValueError):
        summarize(["1", "a", "3"])
